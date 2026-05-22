#!/usr/bin/env python3
"""
convert_v1.py — One-time tool to upgrade v1 (Claude-generated) modules to ELDT NOW v2 standard.
Fixes: REGISTRY slugs/nav, missing audio engine (1.1.6 & 1.1.7), href paths,
       adds Progress.saveState/loadState/resetModule, state persistence, reset button,
       module counter CSS, time tracker, toc-reset CSS, media support.
"""

import re, os

# ── Canonical REGISTRY (no folder property, correct slugs, root-relative nav) ─
REGISTRY = '[{"num":1,"slug":"orientation","unit":"1.1.1","title":"Orientation","file":"ELDT_1.1.1_Orientation.html","group":"A1.1 — Basic Operation","status":"built"},{"num":2,"slug":"control-systems-dashboard","unit":"1.1.2","title":"Control Systems/Dashboard","file":"ELDT_1.1.2_ControlSystemsDashboard.html","group":"A1.1 — Basic Operation","status":"built"},{"num":3,"slug":"pretrip-posttrip-inspections","unit":"1.1.3","title":"Pre- and Post-Trip Inspections","file":"ELDT_1.1.3_PrePostTripInspections.html","group":"A1.1 — Basic Operation","status":"built"},{"num":4,"slug":"basic-control","unit":"1.1.4","title":"Basic Control","file":"ELDT_1.1.4_BasicControl.html","group":"A1.1 — Basic Operation","status":"built"},{"num":5,"slug":"shifting-operating-transmissions","unit":"1.1.5","title":"Shifting/Operating Transmissions","file":"ELDT_1.1.5_ShiftingOperatingTransmissions.html","group":"A1.1 — Basic Operation","status":"built"},{"num":6,"slug":"backing-and-docking","unit":"1.1.6","title":"Backing and Docking","file":"ELDT_1.1.6_BackingAndDocking.html","group":"A1.1 — Basic Operation","status":"built"},{"num":7,"slug":"coupling-and-uncoupling","unit":"1.1.7","title":"Coupling and Uncoupling","file":"ELDT_1.1.7_CouplingAndUncoupling.html","group":"A1.1 — Basic Operation","status":"built"},{"num":8,"slug":"visual-search","unit":"1.2.1","title":"Visual Search","file":"ELDT_1.2.1_VisualSearch.html","group":"A1.2 — Safe Operating Procedures","status":"pending"},{"num":9,"slug":"communication","unit":"1.2.2","title":"Communication","file":"ELDT_1.2.2_Communication.html","group":"A1.2 — Safe Operating Procedures","status":"pending"},{"num":10,"slug":"distracted-driving","unit":"1.2.3","title":"Distracted Driving","file":"ELDT_1.2.3_DistractedDriving.html","group":"A1.2 — Safe Operating Procedures","status":"pending"},{"num":11,"slug":"speed-management","unit":"1.2.4","title":"Speed Management","file":"ELDT_1.2.4_SpeedManagement.html","group":"A1.2 — Safe Operating Procedures","status":"pending"},{"num":12,"slug":"space-management","unit":"1.2.5","title":"Space Management","file":"ELDT_1.2.5_SpaceManagement.html","group":"A1.2 — Safe Operating Procedures","status":"pending"},{"num":13,"slug":"night-operation","unit":"1.2.6","title":"Night Operation","file":"ELDT_1.2.6_NightOperation.html","group":"A1.2 — Safe Operating Procedures","status":"pending"},{"num":14,"slug":"extreme-driving-conditions","unit":"1.2.7","title":"Extreme Driving Conditions","file":"ELDT_1.2.7_ExtremeDrivingConditions.html","group":"A1.2 — Safe Operating Procedures","status":"pending"},{"num":15,"slug":"hazard-perception","unit":"1.3.1","title":"Hazard Perception","file":"ELDT_1.3.1_HazardPerception.html","group":"A1.3 — Advanced Operating Practices","status":"pending"},{"num":16,"slug":"skid-control-recovery","unit":"1.3.2","title":"Skid Control/Recovery","file":"ELDT_1.3.2_SkidControlRecovery.html","group":"A1.3 — Advanced Operating Practices","status":"pending"},{"num":17,"slug":"railroad-highway-grade-crossings","unit":"1.3.3","title":"Railroad-Highway Grade Crossings","file":"ELDT_1.3.3_RailroadHighwayGradeCrossings.html","group":"A1.3 — Advanced Operating Practices","status":"pending"},{"num":18,"slug":"identification-diagnosis-malfunctions","unit":"1.4.1","title":"Identification and Diagnosis of Malfunctions","file":"ELDT_1.4.1_IdentificationDiagnosisMalfunctions.html","group":"A1.4 — Vehicle Systems and Reporting Malfunctions","status":"pending"},{"num":19,"slug":"roadside-inspections","unit":"1.4.2","title":"Roadside Inspections","file":"ELDT_1.4.2_RoadsideInspections.html","group":"A1.4 — Vehicle Systems and Reporting Malfunctions","status":"pending"},{"num":20,"slug":"maintenance","unit":"1.4.3","title":"Maintenance","file":"ELDT_1.4.3_Maintenance.html","group":"A1.4 — Vehicle Systems and Reporting Malfunctions","status":"pending"},{"num":21,"slug":"handling-documenting-cargo","unit":"1.5.1","title":"Handling and Documenting Cargo","file":"ELDT_1.5.1_HandlingDocumentingCargo.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":22,"slug":"environmental-compliance","unit":"1.5.2","title":"Environmental Compliance Issues","file":"ELDT_1.5.2_EnvironmentalComplianceIssues.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":23,"slug":"hours-of-service","unit":"1.5.3","title":"Hours of Service Requirements","file":"ELDT_1.5.3_HoursOfServiceRequirements.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":24,"slug":"fatigue-wellness","unit":"1.5.4","title":"Fatigue and Wellness Awareness","file":"ELDT_1.5.4_FatigueAndWellnessAwareness.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":25,"slug":"post-crash-procedures","unit":"1.5.5","title":"Post-Crash Procedures","file":"ELDT_1.5.5_PostCrashProcedures.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":26,"slug":"external-communications","unit":"1.5.6","title":"External Communications","file":"ELDT_1.5.6_ExternalCommunications.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":27,"slug":"whistleblower-coercion","unit":"1.5.7","title":"Whistleblower/Coercion","file":"ELDT_1.5.7_WhistleblowerCoercion.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":28,"slug":"trip-planning","unit":"1.5.8","title":"Trip Planning","file":"ELDT_1.5.8_TripPlanning.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":29,"slug":"drugs-alcohol","unit":"1.5.9","title":"Drugs/Alcohol","file":"ELDT_1.5.9_DrugsAlcohol.html","group":"A1.5 — Non-Driving Activities","status":"pending"},{"num":30,"slug":"medical-requirements","unit":"1.5.10","title":"Medical Requirements","file":"ELDT_1.5.10_MedicalRequirements.html","group":"A1.5 — Non-Driving Activities","status":"pending"}]'

# ── Audio engine (extracted from 1.1.5) — injected into incomplete files ──────
AUDIO_ENGINE = '''
// ============ AUDIO ============
function startAudio(text){
  stopAudio();
  currentNarrationText=text;
  audioElapsed=0;
  isComplete=false;
  isPlaying=true;
  setAudioControlPlaying();
  if(USE_MP3){
    const path=AUDIO_BASE_PATH+'slide_'+String(currentSlide).padStart(2,'0')+'.mp3';
    currentAudio=new Audio(path);
    estimatedDuration=text.length/14;
    currentAudio.play().catch(()=>onAudioComplete(false));
    currentAudio.addEventListener('ended',()=>onAudioComplete(false));
    currentAudio.addEventListener('error',()=>onAudioComplete(false));
    audioPlayStart=Date.now();
    startProgressTimer();
  } else {
    playTTS(text,0);
  }
}
function playTTS(text,startFraction){
  window.speechSynthesis.cancel();
  const words=text.split(' ');
  const startWord=Math.floor(startFraction*words.length);
  const slicedText=words.slice(startWord).join(' ');
  const utter=new SpeechSynthesisUtterance(slicedText);
  utter.rate=0.95;utter.lang='en-US';
  currentUtterance=utter;
  estimatedDuration=(text.length/14)*(1-startFraction);
  audioPlayStart=Date.now();
  startProgressTimer();
  utter.onend=()=>{if(isPlaying)onAudioComplete(false);};
  utter.onerror=()=>{if(isPlaying)onAudioComplete(false);};
  window.speechSynthesis.speak(utter);
}
function startProgressTimer(){
  clearInterval(audioTimerInterval);
  audioTimerInterval=setInterval(()=>{
    if(!isPlaying)return;
    const elapsed=audioElapsed+(Date.now()-audioPlayStart)/1000;
    const pct=Math.min(100,Math.round((elapsed/estimatedDuration)*100));
    const bar=document.getElementById('audioProgress');
    if(bar)bar.style.width=pct+'%';
    if(elapsed>=estimatedDuration){onAudioComplete(false);}
  },500);
}
function stopAudio(){
  clearInterval(audioTimerInterval);
  window.speechSynthesis.cancel();
  if(currentAudio){currentAudio.pause();currentAudio=null;}
  currentUtterance=null;
  isPlaying=false;
}
function togglePlayPause(){if(isPlaying){pauseAudio();}else{resumeAudio();}}
function pauseAudio(){
  audioElapsed+=(Date.now()-audioPlayStart)/1000;
  clearInterval(audioTimerInterval);
  if(USE_MP3&&currentAudio){currentAudio.pause();}
  else{window.speechSynthesis.cancel();}
  isPlaying=false;
  setAudioControlPaused();
}
function resumeAudio(){
  if(isComplete)return;
  isPlaying=true;
  audioPlayStart=Date.now();
  if(USE_MP3&&currentAudio){currentAudio.play();startProgressTimer();}
  else{const frac=audioElapsed/(estimatedDuration||1);playTTS(currentNarrationText,Math.min(frac,0.99));}
  setAudioControlPlaying();
}
function setAudioControlPlaying(){
  const btn=document.getElementById('audioBtn');const lbl=document.getElementById('audioBtnLabel');
  if(btn){btn.innerHTML=ICON_PAUSE;btn.disabled=false;btn.setAttribute('aria-label','Pause narration');}
  if(lbl){lbl.textContent='Playing';lbl.className='audio-btn-label playing';}
}
function setAudioControlPaused(){
  const btn=document.getElementById('audioBtn');const lbl=document.getElementById('audioBtnLabel');
  if(btn){btn.innerHTML=ICON_PLAY;btn.disabled=false;btn.setAttribute('aria-label','Resume narration');}
  if(lbl){lbl.textContent='Paused';lbl.className='audio-btn-label paused';}
}
function setAudioControlDone(){
  const btn=document.getElementById('audioBtn');const lbl=document.getElementById('audioBtnLabel');
  if(btn){btn.innerHTML=ICON_DONE;btn.disabled=true;btn.setAttribute('aria-label','Narration complete');}
  if(lbl){lbl.textContent='Complete';lbl.className='audio-btn-label complete';}
}
function onAudioComplete(skipUnlock){
  clearInterval(audioTimerInterval);
  isPlaying=false;isComplete=true;
  const bar=document.getElementById('audioProgress');
  if(bar)bar.style.width='100%';
  setAudioControlDone();
  if(!skipUnlock){
    const nextBtn=document.getElementById('nextBtn');
    if(nextBtn)nextBtn.disabled=false;
  }
}
'''

# ── Extra CSS to add before @media ─────────────────────────────────────────────
EXTRA_CSS = (
    '.module-counter{font-family:\'Barlow Condensed\',sans-serif;font-size:12px;font-weight:700;'
    'letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.6);white-space:nowrap;'
    'margin-left:auto;padding-right:4px}\n'
    '.module-counter strong{color:var(--accent);font-weight:700}\n'
    '.toc-reset{display:block;width:100%;background:none;border:none;'
    'border-top:1px solid var(--border);padding:12px 16px;'
    'font-family:\'Barlow Condensed\',sans-serif;font-size:12px;letter-spacing:1.5px;'
    'text-transform:uppercase;color:var(--muted);cursor:pointer;text-align:left;'
    'transition:color .15s,background .15s}\n'
    '.toc-reset:hover{color:var(--danger);background:var(--light)}\n'
    '.slide-media{padding:0 0 24px;display:flex;flex-direction:column;gap:18px}\n'
    '.slide-figure{margin:0;display:flex;flex-direction:column;gap:8px}\n'
    '.slide-img{width:100%;max-height:480px;object-fit:contain;border-radius:6px;border:1px solid var(--border);background:#f7f9fb}\n'
    '.slide-video-wrap{position:relative;width:100%;background:#000;border-radius:6px;overflow:hidden;border:1px solid var(--border)}\n'
    '.slide-video{width:100%;display:block;max-height:480px}\n'
    '.video-replay-btn{position:absolute;bottom:10px;right:10px;background:rgba(13,27,42,.75);color:#fff;'
    'border:none;padding:5px 12px;border-radius:4px;font-family:\'Barlow Condensed\',sans-serif;'
    'font-size:12px;letter-spacing:1.5px;text-transform:uppercase;cursor:pointer;transition:background .15s}\n'
    '.video-replay-btn:hover{background:var(--accent);color:#000}\n'
    '.slide-figure figcaption{font-size:13px;color:var(--muted);font-style:italic;text-align:center;padding:0 8px}'
)

# ── renderMediaHTML function ────────────────────────────────────────────────────
RENDER_MEDIA_FN = """
function renderMediaHTML(s){
  if(!s.image && !s.video) return '';
  let out = '<div class="slide-media">';
  if(s.image){
    const src = typeof s.image === 'string' ? s.image : s.image.src;
    const cap = (typeof s.image === 'object' && s.image.caption) ? s.image.caption : '';
    out += '<figure class="slide-figure">'
         + '<img class="slide-img" src="' + src + '" alt="' + (cap||'') + '" loading="lazy">'
         + (cap ? '<figcaption>' + cap + '</figcaption>' : '')
         + '</figure>';
  }
  if(s.video){
    const src = typeof s.video === 'string' ? s.video : s.video.src;
    const poster = (typeof s.video === 'object' && s.video.poster) ? ' poster="' + s.video.poster + '"' : '';
    const cap = (typeof s.video === 'object' && s.video.caption) ? s.video.caption : '';
    out += '<figure class="slide-figure">'
         + '<div class="slide-video-wrap">'
         + '<video class="slide-video" controls playsinline' + poster + '>'
         + '<source src="' + src + '" type="video/mp4">'
         + 'Your browser does not support video playback.</video>'
         + '<button class="video-replay-btn" onclick="this.previousElementSibling.currentTime=0;this.previousElementSibling.play()">&#x21BA; Replay</button>'
         + '</div>'
         + (cap ? '<figcaption>' + cap + '</figcaption>' : '')
         + '</figure>';
  }
  out += '</div>';
  return out;
}
"""

# ── Active-time tracker ────────────────────────────────────────────────────────
TIMER_SNIPPET = """
// ── Active-time tracker ──────────────────────────────────────────────────────
(function(){
  let _start = Date.now(), _accum = 0;
  function _flush(){
    const secs = Math.round(_accum + (Date.now() - _start) / 1000);
    _accum = 0; _start = Date.now();
    if(secs < 1) return;
    const data = Progress._load();
    if(!data[CURRENT_MODULE_SLUG]) data[CURRENT_MODULE_SLUG] = {};
    data[CURRENT_MODULE_SLUG].timeSpent = (data[CURRENT_MODULE_SLUG].timeSpent || 0) + secs;
    Progress._save(data);
  }
  document.addEventListener('visibilitychange', () => {
    if(document.visibilityState === 'hidden'){ _flush(); }
    else { _start = Date.now(); }
  });
  window.addEventListener('beforeunload', _flush);
  setInterval(_flush, 30000);
})();
"""

# ── resetThisModule function ───────────────────────────────────────────────────
RESET_FN = """
function resetThisModule(){
  if(confirm('Reset all progress for this module? Your quiz score and completed slides will be cleared.')){
    Progress.resetModule(CURRENT_MODULE_SLUG);
    window.location.reload();
  }
}
"""

# ── State-save helpers (added to showSlide and showWelcome) ───────────────────
# These wrap completedSlides persistence into localStorage
SAVE_STATE_FN = """
function _saveState(){
  try{
    const arr = Array.from(completedSlides);
    Progress.saveState(CURRENT_MODULE_SLUG, {completedSlides: arr, currentSlide, view});
  }catch(e){}
}
function _restoreState(){
  try{
    const st = Progress.loadState(CURRENT_MODULE_SLUG);
    if(st && Array.isArray(st.completedSlides)){
      st.completedSlides.forEach(i => completedSlides.add(i));
    }
  }catch(e){}
}
"""

# ── Module info map ────────────────────────────────────────────────────────────
MODULES = [
    {
        'file': 'ELDT_1.1.5_ShiftingOperatingTransmissions.html',
        'slug_old': 'shifting',
        'slug_new': 'shifting-operating-transmissions',
        'num': 5,
        'has_audio': True,
    },
    {
        'file': 'ELDT_1.1.6_BackingAndDocking.html',
        'slug_old': 'backing',
        'slug_new': 'backing-and-docking',
        'num': 6,
        'has_audio': False,
    },
    {
        'file': 'ELDT_1.1.7_CouplingAndUncoupling.html',
        'slug_old': 'coupling-uncoupling',
        'slug_new': 'coupling-and-uncoupling',
        'num': 7,
        'has_audio': False,
    },
]

def log(label, msg):
    status = 'FIXED' if msg != 'already present' else 'SKIP'
    print(f'  {status:<6} {label}')

def replace_once(html, old, new, label):
    if old not in html:
        print(f'  WARN   {label} (anchor not found)')
        return html
    if new in html:
        print(f'  SKIP   {label} (already present)')
        return html
    print(f'  FIXED  {label}')
    return html.replace(old, new, 1)

def process(m):
    filepath = m['file']
    print(f'\n{"─"*55}')
    print(f'Processing: {filepath}')
    print(f'{"─"*55}')

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace REGISTRY (full replacement of old REGISTRY line)
    html = re.sub(r'const REGISTRY\s*=\s*\[.*?\];', f'const REGISTRY = {REGISTRY};', html, flags=re.DOTALL)
    print('  FIXED  REGISTRY (canonical slugs, no folder paths, root nav)')

    # 2. Fix CURRENT_MODULE_SLUG
    html = replace_once(html,
        f"const CURRENT_MODULE_SLUG = '{m['slug_old']}';",
        f"const CURRENT_MODULE_SLUG = '{m['slug_new']}';",
        'CURRENT_MODULE_SLUG')
    # Also handle minified version
    html = replace_once(html,
        f"const CURRENT_MODULE_SLUG='{m['slug_old']}';",
        f"const CURRENT_MODULE_SLUG='{m['slug_new']}';",
        'CURRENT_MODULE_SLUG (minified)')

    # 3. Fix logo/footer hrefs: ../index.html → ./index.html
    html = html.replace('href="../index.html"', 'href="./index.html"')
    print('  FIXED  href paths (../index.html → ./index.html)')

    # 4. Fix dropdown navigation: '../'+m.folder+'/'+m.file → './'+m.file
    html = html.replace(
        "window.location.href='../'+m.folder+'/'+m.file;",
        "window.location.href='./'+m.file;"
    )
    html = html.replace(
        'window.location.href=\'../\'+m.folder+\'/\'+m.file;',
        "window.location.href='./'+m.file;"
    )
    # v2 template uses link.href assignment instead of window.location.href
    html = html.replace(
        "link.href = '../' + m.folder + '/' + m.file;",
        "link.href = './' + m.file;"
    )
    html = html.replace(
        "link.href='../'+m.folder+'/'+m.file;",
        "link.href='./'+m.file;"
    )
    # v2 compact inline: a.href='../'+m.folder+'/'+m.file;
    html = html.replace(
        "a.href='../'+m.folder+'/'+m.file;",
        "a.href='./'+m.file;"
    )
    # Fix Back-to-Home link in showResults (../index.html → ./index.html)
    html = html.replace("href=\"../index.html\"", "href=\"./index.html\"")
    html = html.replace("href='../index.html'", "href='./index.html'")
    print('  FIXED  dropdown nav (folder-relative → root-relative)')

    # 5. Fix results "Continue" link — v1 style (nextMod, btn-continue)
    html = html.replace(
        "'<a class=\"btn-continue\" href=\"../'+nextMod.folder+'/'+nextMod.file+'\">'",
        "'<a class=\"btn-continue\" href=\"./'+nextMod.file+'\">'",
    )
    # v2 style (nextModule, btn btn-next)
    html = html.replace(
        "'<a class=\"btn btn-next\" href=\"../'+nextModule.folder+'/'+nextModule.file+'\">'",
        "'<a class=\"btn btn-next\" href=\"./'+nextModule.file+'\">'",
    )
    # v2 style with spaces around + operators
    html = html.replace(
        "'<a class=\"btn btn-next\" href=\"../' + nextModule.folder + '/' + nextModule.file + '\">'",
        "'<a class=\"btn btn-next\" href=\"./' + nextModule.file + '\">'",
    )
    print('  FIXED  results Continue link (folder-relative → root-relative)')

    # 6. Upgrade Progress object: add saveState, loadState, resetModule
    if 'saveState(' not in html:
        old_progress_end = '  isUnlocked(slug,registry){const data=this._load();const idx=registry.findIndex(m=>m.slug===slug);if(idx===-1)return false;if(idx===0)return true;for(let i=0;i<idx;i++){if(!data[registry[i].slug]||!data[registry[i].slug].completed)return false;}return true;}\n};'
        new_progress_end = ('  isUnlocked(slug,registry){const data=this._load();const idx=registry.findIndex(m=>m.slug===slug);if(idx===-1)return false;if(idx===0)return true;for(let i=0;i<idx;i++){if(!data[registry[i].slug]||!data[registry[i].slug].completed)return false;}return true;},\n'
            '  saveState(slug,state){try{localStorage.setItem(this.KEY+\'_state_\'+slug,JSON.stringify(state));}catch(e){}},\n'
            '  loadState(slug){try{return JSON.parse(localStorage.getItem(this.KEY+\'_state_\'+slug)||\'null\');}catch(e){return null;}},\n'
            '  resetModule(slug){const data=this._load();delete data[slug];this._save(data);try{localStorage.removeItem(this.KEY+\'_state_\'+slug);}catch(e){}}\n'
            '};')
        html = replace_once(html, old_progress_end, new_progress_end, 'Progress.saveState/loadState/resetModule')
        # Also try the version without trailing \n
        if 'saveState(' not in html:
            old2 = '  isUnlocked(slug,registry){const data=this._load();const idx=registry.findIndex(m=>m.slug===slug);if(idx===-1)return false;if(idx===0)return true;for(let i=0;i<idx;i++){if(!data[registry[i].slug]||!data[registry[i].slug].completed)return false;}return true;}};'
            new2 = ('  isUnlocked(slug,registry){const data=this._load();const idx=registry.findIndex(m=>m.slug===slug);if(idx===-1)return false;if(idx===0)return true;for(let i=0;i<idx;i++){if(!data[registry[i].slug]||!data[registry[i].slug].completed)return false;}return true;},'
                '  saveState(slug,state){try{localStorage.setItem(this.KEY+\'_state_\'+slug,JSON.stringify(state));}catch(e){}},\n'
                '  loadState(slug){try{return JSON.parse(localStorage.getItem(this.KEY+\'_state_\'+slug)||\'null\');}catch(e){return null;}},\n'
                '  resetModule(slug){const data=this._load();delete data[slug];this._save(data);try{localStorage.removeItem(this.KEY+\'_state_\'+slug);}catch(e){}}\n'
                '};')
            html = replace_once(html, old2, new2, 'Progress.saveState/loadState/resetModule (minified)')
    else:
        print('  SKIP   Progress methods (already present)')

    # 7. Add module counter CSS and other extras before @media
    if '.module-counter{' not in html:
        media_query = '@media(max-width:680px)'
        html = replace_once(html, media_query,
            EXTRA_CSS + '\n' + media_query,
            'Module counter + toc-reset + media CSS')
    else:
        print('  SKIP   Extra CSS (already present)')

    # 8. Add module counter span to header (before </header>)
    if 'id="moduleCounter"' not in html:
        html = replace_once(html, '</header>',
            '  <span class="module-counter" id="moduleCounter"></span>\n</header>',
            'Module counter span in header')
    else:
        print('  SKIP   Module counter span (already present)')

    # 9. Add module counter JS to init()
    if 'moduleCounter' not in html or 'el.innerHTML = \'Module' not in html:
        old_init = f"Progress.markStarted(CURRENT_MODULE_SLUG);"
        new_init = (f"Progress.markStarted(CURRENT_MODULE_SLUG);\n"
                    f"  const _mod = REGISTRY.find(m => m.slug === CURRENT_MODULE_SLUG);\n"
                    f"  if(_mod){{ const el = document.getElementById('moduleCounter'); if(el) el.innerHTML = 'Module <strong>' + _mod.num + '</strong> of 33'; }}")
        html = replace_once(html, old_init, new_init, 'Module counter JS in init()')

    # 10. Add state save/restore helpers if missing
    if '_saveState' not in html:
        html = replace_once(html,
            'function init(){',
            SAVE_STATE_FN + '\nfunction init(){',
            '_saveState/_restoreState helpers')
    else:
        print('  SKIP   _saveState/_restoreState (already present)')

    # 11. Hook _restoreState into init() and _saveState into advanceSlide
    if '_restoreState()' not in html:
        html = replace_once(html,
            'buildTOC();\n  showWelcome();',
            '_restoreState();\n  buildTOC();\n  showWelcome();',
            '_restoreState call in init()')
        html = replace_once(html,
            'function advanceSlide(idx){\n  completedSlides.add(idx);',
            'function advanceSlide(idx){\n  completedSlides.add(idx);\n  _saveState();',
            '_saveState call in advanceSlide()')
    else:
        print('  SKIP   _restoreState call (already present)')

    # 12. Inject audio engine (1.1.6 and 1.1.7 are missing it)
    if not m['has_audio'] and 'function startAudio(' not in html:
        html = replace_once(html, '\n// ============ BOOT ============\ninit();',
            AUDIO_ENGINE + '\n// ============ BOOT ============\ninit();',
            'Audio engine injection')
        # Fallback: before init();
        if 'function startAudio(' not in html:
            html = html.replace('\ninit();\n</script>', AUDIO_ENGINE + '\ninit();\n</script>', 1)
            print('  FIXED  Audio engine injection (fallback)')
    else:
        if m['has_audio']:
            print('  SKIP   Audio engine (already complete in source)')

    # 13. Add resetThisModule function before init()
    if 'resetThisModule' not in html:
        html = html.replace('\n// ============ BOOT ============\ninit();',
            RESET_FN + '\n// ============ BOOT ============\ninit();', 1)
        if 'resetThisModule' not in html:
            # fallback for files without BOOT comment
            html = html.replace('\ninit();\n</script>', RESET_FN + '\ninit();\n</script>', 1)
        print('  FIXED  resetThisModule function')
    else:
        print('  SKIP   resetThisModule (already present)')

    # 14. Add reset button to sidebar HTML
    if 'toc-reset' not in html:
        html = replace_once(html,
            '<div id="tocList"></div>\n  </aside>',
            '<div id="tocList"></div>\n    <button class="toc-reset" onclick="resetThisModule()">&#x21BA; Reset This Module</button>\n  </aside>',
            'Reset button in sidebar')
        if 'toc-reset' not in html:
            html = replace_once(html,
                '<div id="tocList"></div></aside>',
                '<div id="tocList"></div><button class="toc-reset" onclick="resetThisModule()">&#x21BA; Reset This Module</button></aside>',
                'Reset button in sidebar (minified)')
    else:
        print('  SKIP   Reset button (already present)')

    # 15. Add time tracker before init();
    if 'Active-time tracker' not in html:
        html = html.replace('\n// ============ BOOT ============\ninit();',
            TIMER_SNIPPET + '\n// ============ BOOT ============\ninit();', 1)
        if 'Active-time tracker' not in html:
            html = html.replace('\ninit();\n</script>', TIMER_SNIPPET + '\ninit();\n</script>', 1)
        print('  FIXED  Active-time tracker')
    else:
        print('  SKIP   Active-time tracker (already present)')

    # 16. Add renderMediaHTML before // ============ AUDIO
    if 'renderMediaHTML' not in html:
        html = html.replace('// ============ AUDIO ============',
            RENDER_MEDIA_FN + '\n// ============ AUDIO ============', 1)
        if 'renderMediaHTML' not in html:
            html = html.replace('\ninit();\n</script>', RENDER_MEDIA_FN + '\ninit();\n</script>', 1)
        print('  FIXED  renderMediaHTML function')
    else:
        print('  SKIP   renderMediaHTML (already present)')

    # 17. Inject renderMediaHTML into showSlide content HTML (after slide-content div)
    if '"+renderMediaHTML(s)+"' not in html and 'renderMediaHTML(s)+' not in html:
        html = html.replace(
            "'<div class=\"slide-content\">'+s.contentHTML+'</div>'+",
            "'<div class=\"slide-content\">'+s.contentHTML+'</div>'+renderMediaHTML(s)+",
        )
        print('  FIXED  renderMediaHTML call in showSlide')
    else:
        print('  SKIP   renderMediaHTML call (already present)')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✓ Written: {filepath}')

    # 18. Update REGISTRY status in other built files
    update_registry_status(m['slug_new'])

def update_registry_status(slug):
    targets = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    updated = []
    for t in targets:
        with open(t, 'r', encoding='utf-8') as f:
            content = f.read()
        old = f'"slug":"{slug}","unit":"1.1.{slug.split("-")[0] if False else "?"}","'
        # Use regex to find and replace status for this slug
        new_content, n = re.subn(
            rf'("slug":"{re.escape(slug)}"[^}}]*?"status":)"pending"',
            r'\1"built"',
            content
        )
        if n > 0:
            with open(t, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated.append(t)
    if updated:
        print(f'  FIXED  REGISTRY status → "built" in: {", ".join(updated)}')
    else:
        print(f'  SKIP   REGISTRY status (no updates needed)')

if __name__ == '__main__':
    for m in MODULES:
        if os.path.exists(m['file']):
            process(m)
        else:
            print(f'  WARN   File not found: {m["file"]}')
    print('\n✓ All done.')
