#!/usr/bin/env python3
"""
fix_module.py — ELDT NOW Module Integration Tool
Usage:  python3 fix_module.py <filename.html>
Example: python3 fix_module.py ELDT_1.1.5_ShiftingOperatingTransmissions.html

Applies every required change to a newly uploaded module file and
updates the REGISTRY status across all existing files in the directory.
"""

import re
import sys
import os
import glob

# ── Snippets ──────────────────────────────────────────────────────────────────

TOC_RESET_CSS = (
    '.toc-reset{display:block;width:100%;background:none;border:none;'
    'border-top:1px solid var(--border);padding:12px 18px;'
    "font-family:'Barlow Condensed',sans-serif;font-size:12px;letter-spacing:1.5px;"
    'text-transform:uppercase;color:var(--muted);cursor:pointer;text-align:left;'
    'transition:color .15s,background .15s}\n'
    '.toc-reset:hover{color:var(--danger);background:var(--light)}'
)

MODULE_COUNTER_CSS = (
    ".module-counter{font-family:'Barlow Condensed',sans-serif;font-size:12px;"
    'font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--accent);'
    'white-space:nowrap;margin-left:auto;padding-right:4px}'
)

MODULE_COUNTER_HTML_OLD = '</header>'
MODULE_COUNTER_HTML_NEW = '  <span class="module-counter" id="moduleCounter"></span>\n</header>'

MODULE_COUNTER_JS_OLD = '  buildDropdown();'
MODULE_COUNTER_JS_NEW = (
    "  const _mod = REGISTRY.find(m => m.slug === CURRENT_MODULE_SLUG);\n"
    "  if(_mod){ const el = document.getElementById('moduleCounter');"
    " if(el) el.innerHTML = 'Module <strong>' + _mod.num + '</strong> of 33'; }\n"
    "  buildDropdown();"
)

RESET_MODULE_OLD = (
    "  loadState(slug){ try { return JSON.parse(localStorage.getItem"
    "(this.KEY + '_state_' + slug) || 'null'); } catch(e){ return null; } }\n"
    "};"
)
RESET_MODULE_NEW = (
    "  loadState(slug){ try { return JSON.parse(localStorage.getItem"
    "(this.KEY + '_state_' + slug) || 'null'); } catch(e){ return null; } },\n"
    "  resetModule(slug){\n"
    "    const data = this._load();\n"
    "    delete data[slug];\n"
    "    this._save(data);\n"
    "    try { localStorage.removeItem(this.KEY + '_state_' + slug); } catch(e){}\n"
    "  }\n"
    "};"
)

RESET_FN_OLD = (
    "function saveCurrentState(){\n"
    "  Progress.saveState(CURRENT_MODULE_SLUG,"
    " { currentSlide, viewMode, unlockStatus: unlockStatus.slice() });\n"
    "}"
)
RESET_FN_NEW = (
    "function saveCurrentState(){\n"
    "  Progress.saveState(CURRENT_MODULE_SLUG,"
    " { currentSlide, viewMode, unlockStatus: unlockStatus.slice() });\n"
    "}\n\n"
    "function resetThisModule(){\n"
    "  if(confirm('Reset all progress for this module?"
    " Your quiz score and completed slides will be cleared.')){\n"
    "    Progress.resetModule(CURRENT_MODULE_SLUG);\n"
    "    window.location.reload();\n"
    "  }\n"
    "}"
)

RESET_BTN_OLD = (
    '    <div class="toc-quiz" id="tocQuiz" onclick="tryStartQuiz()">\n'
    '      <div class="toc-check"></div>\n'
    '      <span>Knowledge Check</span>\n'
    '    </div>\n'
    '  </aside>'
)
RESET_BTN_NEW = (
    '    <div class="toc-quiz" id="tocQuiz" onclick="tryStartQuiz()">\n'
    '      <div class="toc-check"></div>\n'
    '      <span>Knowledge Check</span>\n'
    '    </div>\n'
    '    <button class="toc-reset" onclick="resetThisModule()">&#x21BA; Reset This Module</button>\n'
    '  </aside>'
)

TIMER_OLD = 'window.addEventListener(\'DOMContentLoaded\', init);'
TIMER_NEW = (
    "// ── Active-time tracker ──────────────────────────────────────────────────────\n"
    "(function(){\n"
    "  let _start = Date.now(), _accum = 0;\n"
    "  function _flush(){\n"
    "    const secs = Math.round(_accum + (Date.now() - _start) / 1000);\n"
    "    _accum = 0; _start = Date.now();\n"
    "    if(secs < 1) return;\n"
    "    const data = Progress._load();\n"
    "    if(!data[CURRENT_MODULE_SLUG]) data[CURRENT_MODULE_SLUG] = {};\n"
    "    data[CURRENT_MODULE_SLUG].timeSpent = (data[CURRENT_MODULE_SLUG].timeSpent || 0) + secs;\n"
    "    Progress._save(data);\n"
    "  }\n"
    "  document.addEventListener('visibilitychange', () => {\n"
    "    if(document.visibilityState === 'hidden'){ _flush(); }\n"
    "    else { _start = Date.now(); }\n"
    "  });\n"
    "  window.addEventListener('beforeunload', _flush);\n"
    "  setInterval(_flush, 30000);\n"
    "})();\n\n"
    "window.addEventListener('DOMContentLoaded', init);"
)

MEDIA_CSS_LINES = (
    '.slide-media{padding:0 40px 24px;display:flex;flex-direction:column;gap:18px}\n'
    '.slide-figure{margin:0;display:flex;flex-direction:column;gap:8px}\n'
    '.slide-img{width:100%;max-height:480px;object-fit:contain;border-radius:6px;border:1px solid var(--border);background:#f7f9fb}\n'
    '.slide-video-wrap{position:relative;width:100%;background:#000;border-radius:6px;overflow:hidden;border:1px solid var(--border)}\n'
    '.slide-video{width:100%;display:block;max-height:480px}\n'
    ".video-replay-btn{position:absolute;bottom:10px;right:10px;background:rgba(13,27,42,.75);color:#fff;border:none;padding:5px 12px;border-radius:4px;font-family:'Barlow Condensed',sans-serif;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;cursor:pointer;transition:background .15s}\n"
    '.video-replay-btn:hover{background:var(--accent);color:#000}\n'
    '.slide-figure figcaption{font-size:13px;color:var(--muted);font-style:italic;text-align:center;padding:0 8px}'
)

RENDER_MEDIA_FN = (
    "function renderMediaHTML(s){\n"
    "  if(!s.image && !s.video) return '';\n"
    "  let out = '<div class=\"slide-media\">';\n"
    "  if(s.image){\n"
    "    const src = typeof s.image === 'string' ? s.image : s.image.src;\n"
    "    const cap = (typeof s.image === 'object' && s.image.caption) ? s.image.caption : '';\n"
    "    out += '<figure class=\"slide-figure\">'\n"
    "         + '<img class=\"slide-img\" src=\"' + src + '\" alt=\"' + (cap||'') + '\" loading=\"lazy\">'\n"
    "         + (cap ? '<figcaption>' + cap + '</figcaption>' : '')\n"
    "         + '</figure>';\n"
    "  }\n"
    "  if(s.video){\n"
    "    const src = typeof s.video === 'string' ? s.video : s.video.src;\n"
    "    const poster = (typeof s.video === 'object' && s.video.poster) ? ' poster=\"' + s.video.poster + '\"' : '';\n"
    "    const cap = (typeof s.video === 'object' && s.video.caption) ? s.video.caption : '';\n"
    "    out += '<figure class=\"slide-figure\">'\n"
    "         + '<div class=\"slide-video-wrap\">'\n"
    "         + '<video class=\"slide-video\" controls playsinline' + poster + '>'\n"
    "         + '<source src=\"' + src + '\" type=\"video/mp4\">'\n"
    "         + 'Your browser does not support video playback.</video>'\n"
    "         + '<button class=\"video-replay-btn\" onclick=\"this.previousElementSibling.currentTime=0;this.previousElementSibling.play()\">&#x21BA; Replay</button>'\n"
    "         + '</div>'\n"
    "         + (cap ? '<figcaption>' + cap + '</figcaption>' : '')\n"
    "         + '</figure>';\n"
    "  }\n"
    "  out += '</div>';\n"
    "  return out;\n"
    "}\n"
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def apply_fix(html, check_marker, old, new, label, log):
    if check_marker in html:
        log.append(('SKIP', label, 'already present'))
        return html
    if old in html:
        html = html.replace(old, new, 1)
        log.append(('FIXED', label, ''))
    else:
        log.append(('WARN', label, 'anchor text not found — fix manually'))
    return html


def fix_hrefs(html, log):
    matches = re.findall(r'href="\.\./[^/]+/[^"]+\.html"', html)
    if not matches:
        log.append(('SKIP', 'Broken href paths', 'none found or already fixed'))
        return html
    html = re.sub(r'href="\.\./[^/]+/([^"]+\.html)"', r'href="./\1"', html)
    log.append(('FIXED', 'Broken href paths', f'{len(matches)} replaced'))
    return html


def get_slug(html):
    m = re.search(r"const CURRENT_MODULE_SLUG\s*=\s*'([^']+)'", html)
    return m.group(1) if m else None


def update_registry_status(slug, skip_file, log):
    pattern = r'(\{"num":\d+,"slug":"' + re.escape(slug) + r'"[^}]*?"status":")pending(")'
    updated = []
    for filepath in sorted(glob.glob('*.html')):
        if os.path.abspath(filepath) == os.path.abspath(skip_file):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = re.sub(pattern, r'\1built\2', content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated.append(filepath)
    if updated:
        for fp in updated:
            log.append(('FIXED', f'REGISTRY status in {fp}', 'pending → built'))
    else:
        log.append(('SKIP', 'REGISTRY status updates', 'no other files needed updating'))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 fix_module.py <filename.html>')
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f'ERROR: File not found: {filepath}')
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    log = []

    # Apply all fixes
    html = fix_hrefs(html, log)

    html = apply_fix(html, 'module-counter{',
        '.toc-quiz .toc-check{border-color:var(--border)}',
        MODULE_COUNTER_CSS + '\n.toc-quiz .toc-check{border-color:var(--border)}',
        '.module-counter CSS', log)

    html = apply_fix(html, 'toc-reset{',
        '.toc-quiz.unlocked .toc-check::before{content:"★";font-size:11px}',
        '.toc-quiz.unlocked .toc-check::before{content:"★";font-size:11px}\n' + TOC_RESET_CSS,
        '.toc-reset CSS', log)

    html = apply_fix(html, 'id="moduleCounter"',
        MODULE_COUNTER_HTML_OLD,
        MODULE_COUNTER_HTML_NEW,
        'Module counter span in <header>', log)

    html = apply_fix(html, "REGISTRY.find(m => m.slug === CURRENT_MODULE_SLUG)",
        MODULE_COUNTER_JS_OLD,
        MODULE_COUNTER_JS_NEW,
        'Module counter JS in init()', log)

    html = apply_fix(html, 'resetModule(slug)',
        RESET_MODULE_OLD,
        RESET_MODULE_NEW,
        'Progress.resetModule() method', log)

    html = apply_fix(html, 'function resetThisModule()',
        RESET_FN_OLD,
        RESET_FN_NEW,
        'resetThisModule() function', log)

    html = apply_fix(html, 'onclick="resetThisModule()"',
        RESET_BTN_OLD,
        RESET_BTN_NEW,
        'Reset button in sidebar', log)

    html = apply_fix(html, 'Active-time tracker',
        TIMER_OLD,
        TIMER_NEW,
        'Active-time tracker IIFE', log)

    html = apply_fix(html, 'slide-media{',
        '.data-table td.bad{color:var(--danger);font-weight:700}',
        '.data-table td.bad{color:var(--danger);font-weight:700}\n' + MEDIA_CSS_LINES,
        'Media CSS (.slide-media, .slide-video-wrap, etc.)', log)

    html = apply_fix(html, '.slide-media{padding:0 24px',
        '  .slide-nav{padding:16px 24px}',
        '  .slide-nav{padding:16px 24px}\n  .slide-media{padding:0 24px 20px}',
        'Mobile media CSS', log)

    html = apply_fix(html, 'function renderMediaHTML',
        'function renderSlide(i){',
        RENDER_MEDIA_FN + '\nfunction renderSlide(i){',
        'renderMediaHTML() function', log)

    html = apply_fix(html, 'renderMediaHTML(s)',
        '    <div class="slide-content">${s.contentHTML}</div>\n    <div class="narration-box">',
        '    <div class="slide-content">${s.contentHTML}</div>\n    ${renderMediaHTML(s)}\n    <div class="narration-box">',
        'renderMediaHTML call in renderSlide', log)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    # Update REGISTRY status in other files
    slug = get_slug(html)
    if slug:
        update_registry_status(slug, filepath, log)
    else:
        log.append(('WARN', 'CURRENT_MODULE_SLUG', 'not found — REGISTRY not updated'))

    # Report
    print(f'\nELDT NOW — Module Integration Fix')
    print(f'File : {filepath}')
    if slug:
        print(f'Slug : {slug}')
    print('─' * 55)
    for status, label, note in log:
        suffix = f'  ({note})' if note else ''
        print(f'  {status:<5}  {label}{suffix}')

    warns = [l for l in log if l[0] == 'WARN']
    print('─' * 55)
    if warns:
        print(f'  {len(warns)} warning(s) — check items marked WARN manually.')
    else:
        print('  All steps completed with no warnings.')
    print()


if __name__ == '__main__':
    main()
