# ELDT NOW — Project Overview

## What This Is

A 33-module FMCSA-compliant CDL Entry-Level Driver Training (ELDT) theory course. Pure static HTML/CSS/JS served by a lightweight Python HTTP server. No build step, no framework, no database — everything runs directly in the browser.

GitHub repo: https://github.com/jzulfi61-glitch/ELDTNOW

---

## How It Runs

```
python3 server.py       # starts on port 5000, no-cache headers
```

`server.py` serves all files from the project root. Every module file is self-contained.

---

## File Structure

```
/
├── index.html                         Course home — module grid + progress bar
├── server.py                          No-cache HTTP server (port 5000)
├── MODULE_TEMPLATE.html               Annotated master template for new modules
├── MODULE_CHECKLIST.md                Checklist for adding new modules
│
├── ELDT_1.1.1_Orientation.html        Module 1   ─┐
├── ELDT_1.1.2_ControlSystemsDashboard.html  Mod 2 │
├── ELDT_1.1.3_PrePostTripInspections.html   Mod 3 │
├── ELDT_1.1.4_BasicControl.html             Mod 4 │ Built (19 of 33)
├── ELDT_1.1.5_ShiftingOperatingTransmissions.html Mod 5│
├── ELDT_1.1.6_BackingAndDocking.html        Mod 6 │
├── ELDT_1.1.7_CouplingAndUncoupling.html    Mod 7 │
├── ELDT_1.2.1_VisualSearch.html             Mod 8 │
├── ELDT_1.2.2_Communication.html            Mod 9 │
├── ELDT_1.2.3_DistractedDriving.html        Mod 10│
├── ELDT_1.2.4_SpeedManagement.html          Mod 11│
├── ELDT_1.2.5_SpaceManagement.html          Mod 12│
├── ELDT_1.2.6_NightOperation.html           Mod 13│
├── ELDT_1.2.7_ExtremeDrivingConditions.html Mod 14│
├── ELDT_1.3.1_HazardPerception.html         Mod 15│
├── ELDT_1.3.2_SkidControlRecovery.html      Mod 16│
├── ELDT_1.3.3_RailroadHighwayGradeCrossings.html Mod 17│
├── ELDT_1.4.1_IdentificationDiagnosisMalfunctions.html Mod 18│
├── ELDT_1.4.2_RoadsideInspections.html      Mod 19─┘
│
└── _tools/
    └── fix_module.py                  Patch helper for externally-generated modules
```

Modules 20–33 are pending (listed in the REGISTRY but no file built yet).

---

## Architecture

### Self-Contained Modules

Every `ELDT_*.html` file is a complete standalone page:
- **Slides** — `const slides = [...]` array; each object has `section`, `sectionLabel`, `title`, `contentHTML`, `narration`, and optional `audioUrl`, `image`, `video`
- **Quiz** — `const quizData = [...]` — exactly 15 questions, 80% pass threshold (12/15)
- **Audio** — browser TTS by default; set `USE_MP3 = true` and add `.mp3` files for professional narration; per-slide `audioUrl` also supported
- **Progress** — `localStorage`-based. Key `eldtnow_progress` stores completion/score. Key `eldtnow_progress_state_{slug}` stores slide position mid-module

### Unlock Chain

Module N is locked until Module N−1 is passed at 80%+. Module 1 is always unlocked. The REGISTRY embedded in every file drives this.

### REGISTRY

Every module file and `index.html` embeds the same 33-entry REGISTRY array. When a new module is built, its status changes from `"pending"` to `"built"` in all files. The array controls the dropdown nav, lock states, and the "Continue →" links.

---

## Adding a New Module (Modules 20–33)

1. Copy `MODULE_TEMPLATE.html` → rename to `ELDT_X.X.X_TopicName.html`
2. Fill in the 6 marked change points (title, nav label, welcome screen, slug, slides, quiz)
3. Update `CURRENT_MODULE_SLUG` to match the slug in the REGISTRY
4. Update REGISTRY in **all** existing module files + `index.html`: change this module's `"status":"pending"` → `"status":"built"`
5. Verify with the `MODULE_CHECKLIST.md` checklist
6. Push to GitHub via the Python urllib API (use `GITHUB_TOKEN` secret)

---

## GitHub Pushes

Uses Python `urllib` with the GitHub Contents API (no git CLI — restricted in this environment).

```python
# Pattern: GET sha → PUT contents
TOKEN = os.environ.get("GITHUB_TOKEN")
# GET: https://api.github.com/repos/jzulfi61-glitch/ELDTNOW/contents/{filename}
# PUT: same URL with {"message":..., "content": base64, "sha": existing_sha}
```

---

## Module Variants (internal note)

Two formatting variants exist from early development. Both are fully functional:
- **Variant A** (Mods 1–7): multi-line JS config, `renderMediaHTML` as a named function
- **Variant B** (Mods 8–19): compact single-line config, same features

All new modules should use **MODULE_TEMPLATE.html** which is Variant A style.

---

## User Preferences

- All module HTML files must stay in the project root (cross-module links are root-relative)
- REGISTRY must be kept in sync across all module files whenever a new module is added
- Quiz always has exactly 15 questions; pass threshold always 80% (12/15)
- No folders for module files — flat root structure is intentional
