# ELDT NOW — New Module Integration Checklist

When a new module HTML file is uploaded to the root directory, run the auto-fix script first, then use the verification checklist below to confirm it worked.

---

## Step 1 — Run the fix script

```bash
python3 fix_module.py ELDT_1.1.5_ShiftingOperatingTransmissions.html
```

The script prints `FIXED`, `SKIP`, or `WARN` for each step:
- **FIXED** — change was applied
- **SKIP** — already present, nothing to do
- **WARN** — anchor text not found; apply that step manually using the reference below

---

## Step 2 — Verify in browser

Open the module and confirm each item:

- [ ] "MODULE X OF 33" counter appears in the top-right corner of the header
- [ ] "↺ Reset This Module" button appears at the bottom of the Course Outline sidebar
- [ ] Clicking the ELDT NOW logo returns to `index.html`
- [ ] The All 33 Modules dropdown links open the correct files
- [ ] Completing the quiz shows a "Continue →" link pointing to the correct next module
- [ ] On the dashboard (`index.html`) the new module card shows as available, not locked/pending

---

## Manual Fix Reference

Use these only when the script reports WARN for a step.

---

### 1 · Fix broken href paths

**Find pattern:** `href="../[any-folder]/[filename].html"`  
**Replace with:** `href="./[filename].html"`  
Locations: logo link, dropdown module links, quiz "Continue" button, dashboard CTA.

---

### 2 · Add `.module-counter` CSS

**Find:**
```
.toc-quiz .toc-check{border-color:var(--border)}
```
**Insert before it:**
```css
.module-counter{font-family:'Barlow Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--accent);white-space:nowrap;margin-left:auto;padding-right:4px}
```

---

### 3 · Add `.toc-reset` CSS

**Find:**
```
.toc-quiz.unlocked .toc-check::before{content:"★";font-size:11px}
```
**Insert after it:**
```css
.toc-reset{display:block;width:100%;background:none;border:none;border-top:1px solid var(--border);padding:12px 18px;font-family:'Barlow Condensed',sans-serif;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);cursor:pointer;text-align:left;transition:color .15s,background .15s}
.toc-reset:hover{color:var(--danger);background:var(--light)}
```

---

### 4 · Add module counter `<span>` in header

**Find:** `</header>`  
**Replace with:**
```html
  <span class="module-counter" id="moduleCounter"></span>
</header>
```

---

### 5 · Add module counter JS inside `init()`

**Find:** `  buildDropdown();`  
**Replace with:**
```js
  const _mod = REGISTRY.find(m => m.slug === CURRENT_MODULE_SLUG);
  if(_mod){ const el = document.getElementById('moduleCounter'); if(el) el.innerHTML = 'Module <strong>' + _mod.num + '</strong> of 33'; }
  buildDropdown();
```

---

### 6 · Add `resetModule` method to Progress object

**Find:**
```
  loadState(slug){ try { return JSON.parse(localStorage.getItem(this.KEY + '_state_' + slug) || 'null'); } catch(e){ return null; } }
};
```
**Replace with:**
```js
  loadState(slug){ try { return JSON.parse(localStorage.getItem(this.KEY + '_state_' + slug) || 'null'); } catch(e){ return null; } },
  resetModule(slug){
    const data = this._load();
    delete data[slug];
    this._save(data);
    try { localStorage.removeItem(this.KEY + '_state_' + slug); } catch(e){}
  }
};
```

---

### 7 · Add `resetThisModule()` function

**Find** the closing `}` of `saveCurrentState()` and **insert after it:**
```js
function resetThisModule(){
  if(confirm('Reset all progress for this module? Your quiz score and completed slides will be cleared.')){
    Progress.resetModule(CURRENT_MODULE_SLUG);
    window.location.reload();
  }
}
```

---

### 8 · Add Reset button in sidebar

**Find:**
```html
    <div class="toc-quiz" id="tocQuiz" onclick="tryStartQuiz()">
      <div class="toc-check"></div>
      <span>Knowledge Check</span>
    </div>
  </aside>
```
**Replace with:**
```html
    <div class="toc-quiz" id="tocQuiz" onclick="tryStartQuiz()">
      <div class="toc-check"></div>
      <span>Knowledge Check</span>
    </div>
    <button class="toc-reset" onclick="resetThisModule()">↺ Reset This Module</button>
  </aside>
```

---

### 9 · Add active-time tracker

**Find:** `window.addEventListener('DOMContentLoaded', init);`  
**Replace with:**
```js
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

window.addEventListener('DOMContentLoaded', init);
```

---

### 10 · Update REGISTRY status in all other files

The script handles this automatically. If done manually: in every other `.html` file (all existing modules + `index.html`), find the REGISTRY entry for this module's slug and change `"status":"pending"` to `"status":"built"`.

---

## localStorage keys (for reference)

| Key | Contents |
|-----|----------|
| `eldtnow_progress` | JSON object — completion record for all 33 modules |
| `eldtnow_progress_state_{slug}` | JSON object — slide position, unlock status, view mode for one module |
