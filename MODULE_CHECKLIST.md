# ELDT NOW — New Module Checklist

Use this when adding the remaining 2 modules (29–30) or any bonus modules.

---

## Step 1 — Create the file

Copy `MODULE_TEMPLATE.html` and rename it:

```
ELDT_X.X.X_TopicName.html
```

Example: `ELDT_1.4.3_EmergencyEquipment.html`

---

## Step 2 — Fill in the 6 change points

The template marks every spot with `← CHANGE THIS`:

| # | What | Where in file |
|---|---|---|
| ① | `<title>` tag | `<head>` |
| ② | Header nav label | `<strong>UNIT X.X.X</strong> Topic Name` |
| ③ | Welcome screen | Eyebrow, h1, subtitle, objectives list |
| ④ | `CURRENT_MODULE_SLUG` | Must match the slug in the REGISTRY |
| ⑤ | `const slides = [...]` | Replace all 6 example slides with real content |
| ⑥ | `const quizData = [...]` | Replace placeholder questions with 15 real ones |

**Quiz rules:** exactly 15 questions, 4 options each, `ans` is zero-based index (0=A, 1=B, 2=C, 3=D).

---

## Step 3 — Update REGISTRY status in all files

Change `"status":"pending"` → `"status":"built"` for this module's slug in:

- Every existing `ELDT_*.html` file (all existing modules)
- `index.html`

The simplest way is a one-liner find/replace on the slug:

```python
# Example — run from project root
import re, glob
SLUG = 'your-module-slug'
pat = r'("slug":"' + SLUG + r'"[^}]+"status":")pending(")'
for f in glob.glob('*.html'):
    h = open(f).read()
    new = re.sub(pat, r'\1built\2', h)
    if new != h:
        open(f, 'w').write(new)
        print('updated', f)
```

Or use `_tools/fix_module.py` if the module was built externally (not from the template):

```bash
python3 _tools/fix_module.py ELDT_X.X.X_TopicName.html
```

---

## Step 4 — Browser verification

Open the new module and confirm:

- [ ] `Module X of 30` counter appears in the header (top right)
- [ ] `↺ Reset This Module` button appears at the bottom of the sidebar
- [ ] Narration plays and the progress bar fills for each slide
- [ ] Each slide's Next button is locked until narration completes
- [ ] All 15 quiz questions display and score correctly
- [ ] Passing (80%+) shows "You Passed!" and a **Continue to Module X+1 →** link
- [ ] Failing shows a Retake option
- [ ] The 30-module dropdown lists this module in the correct position
- [ ] `index.html` shows this module as unlocked (not locked/pending) once previous module is passed

---

## Step 5 — Push to GitHub

```python
import os, json, base64, urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN")
REPO  = "jzulfi61-glitch/ELDTNOW"

def push(fname):
    with open(fname, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/contents/{fname}",
        headers={"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req) as r:
            sha = json.loads(r.read()).get("sha")
    except:
        sha = None
    data = {"message": f"feat: add {fname}", "content": content}
    if sha: data["sha"] = sha
    req2 = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/contents/{fname}",
        data=json.dumps(data).encode(), method="PUT",
        headers={"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req2) as r:
        print("OK", fname)
```

Push both the new module file and all updated files in one batch.

---

## Slide content reference

### Available `contentHTML` CSS classes

```
<p class="emphasis">          highlighted callout (gold left border)
<p class="footnote">          small grey italic footnote
<ul class="check-list">       green checkmark bullet list
<div class="callout">         blue info box
<div class="callout warning"> orange warning box
<div class="stat-grid">       responsive stat cards
<div class="two-col">         two-column card layout
<div class="formula-box">     dark formula display
<table class="data-table">    styled data table
```

### Optional slide fields

```js
"audioUrl": "https://…"                    // per-slide ElevenLabs URL
"image": "images/file.jpg"                 // shorthand
"image": {"src": "…", "caption": "…"}     // with caption
"video": "video/file.mp4"                  // shorthand
"video": {"src":"…","poster":"…","caption":"…"}
```

---

## localStorage keys

| Key | Contents |
|-----|----------|
| `eldtnow_progress` | Completion record for all 30 modules |
| `eldtnow_progress_state_{slug}` | Slide position + unlock status for one module |
