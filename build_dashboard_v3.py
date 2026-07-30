"""
JEE Intelligence Dashboard v3 — Premium Minimal SaaS Style
Builds a self-contained index.html from final_data.json.

Design philosophy:
- Linear / Vercel / Stripe Dashboard aesthetic
- White + Slate neutrals + 1 restrained Indigo accent
- 1 font family (Inter)
- Subtle borders, no shadows except hover
- Generous spacing, calm hierarchy
- No glassmorphism, glow, gradients, animations
"""

import json
import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "raw_data", "final_data.json")
OUT_PATH = os.path.join(HERE, "index.html")


def esc(s):
    return html.escape(s) if s else ""


# ──────────────────────────────────────────────────────────
#  Load + transform data
# ──────────────────────────────────────────────────────────
def load_data():
    with open(DATA_PATH) as f:
        d = json.load(f)

    meta = d["metadata"]
    chapters = d["chapter_rankings"]
    patterns = d["patterns"]
    trends = d["trends"]
    questions = d["questions"]

    # Index by subject
    subjects = {}
    for c in chapters:
        subjects.setdefault(c["subject"], []).append(c)

    # Add trends lookup
    trends_by_chapter = {}
    for t in trends:
        key = (t["subject"], t["chapter"])
        trends_by_chapter[key] = t

    # Add chapter stats lookup
    ch_stats = d["chapter_stats"]

    return {
        "meta": meta,
        "chapters": chapters,
        "subjects": subjects,
        "patterns": patterns,
        "trends": trends,
        "trends_by_chapter": trends_by_chapter,
        "ch_stats": ch_stats,
        "questions": questions,
    }


# ──────────────────────────────────────────────────────────
#  Embed data as JSON for client-side JS
# ──────────────────────────────────────────────────────────
def embed_data(data):
    return json.dumps({
        "meta": data["meta"],
        "chapters": data["chapters"],
        "subjects": data["subjects"],
        "patterns": data["patterns"],
        "trends_by_chapter": {
            f"{s}/{c}": t
            for (s, c), t in data["trends_by_chapter"].items()
        },
        "ch_stats": data["ch_stats"],
        "questions": data["questions"],
    }, separators=(",", ":"))


# ──────────────────────────────────────────────────────────
#  CSS — minimal, premium, SaaS-grade
# ──────────────────────────────────────────────────────────
CSS = """
:root {
  /* Surfaces */
  --bg: #F8FAFC;            /* slate-50 */
  --surface: #FFFFFF;
  --surface-hover: #F1F5F9; /* slate-100 */

  /* Borders */
  --border: #E2E8F0;        /* slate-200 */
  --border-strong: #CBD5E1; /* slate-300 */

  /* Text */
  --text: #0F172A;          /* slate-900 */
  --text-secondary: #475569;/* slate-600 */
  --text-muted: #94A3B8;    /* slate-400 */

  /* Single accent — restrained indigo */
  --accent: #4F46E5;
  --accent-hover: #4338CA;
  --accent-bg: #EEF2FF;
  --accent-text: #4338CA;

  /* Semantic — muted, not loud */
  --success: #059669;
  --success-bg: #ECFDF5;
  --warning: #D97706;
  --warning-bg: #FEF3C7;
  --danger: #DC2626;
  --danger-bg: #FEE2E2;

  /* Layout */
  --max-w: 1280px;
  --nav-h: 56px;
  --radius: 6px;

  /* Spacing — 4px base */
  --sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px;  --sp-4: 16px;
  --sp-5: 20px; --sp-6: 24px; --sp-8: 32px;  --sp-10: 40px;
  --sp-12: 48px; --sp-16: 64px; --sp-20: 80px; --sp-24: 96px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.5;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ── Typography ─────────────────────────────────────── */
h1, h2, h3, h4 {
  font-weight: 600;
  letter-spacing: -0.015em;
  color: var(--text);
}
h1 { font-size: 32px; line-height: 1.2; letter-spacing: -0.025em; font-weight: 700; }
h2 { font-size: 22px; line-height: 1.25; }
h3 { font-size: 17px; line-height: 1.3; font-weight: 600; }
h4 { font-size: 14px; line-height: 1.3; font-weight: 600; color: var(--text-secondary); }

.eyebrow {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
}
.text-sm { font-size: 13px; }
.text-xs { font-size: 12px; }
.text-secondary { color: var(--text-secondary); }
.text-muted { color: var(--text-muted); }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }

/* ── Layout ─────────────────────────────────────────── */
.container {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--sp-6);
}
.page { padding: var(--sp-8) 0 var(--sp-16); }
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--sp-8);
  padding-bottom: var(--sp-6);
  border-bottom: 1px solid var(--border);
}
.page-header-meta {
  display: flex;
  gap: var(--sp-6);
  align-items: center;
}

/* ── Navigation ─────────────────────────────────────── */
.nav {
  height: var(--nav-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--sp-6);
  height: 100%;
  display: flex;
  align-items: center;
  gap: var(--sp-8);
}
.brand {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  font-weight: 600;
  font-size: 15px;
  color: var(--text);
  cursor: pointer;
  text-decoration: none;
}
.brand-mark {
  width: 22px; height: 22px;
  background: var(--accent);
  border-radius: 5px;
  display: grid;
  place-items: center;
  color: white;
  font-weight: 700;
  font-size: 12px;
}
.nav-tabs {
  display: flex;
  gap: var(--sp-1);
  flex: 1;
}
.nav-tab {
  padding: 6px 12px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: color 120ms, background-color 120ms;
}
.nav-tab:hover { color: var(--text); background: var(--surface-hover); }
.nav-tab.active { color: var(--text); background: var(--surface-hover); }
.nav-search {
  position: relative;
}
.nav-search input {
  width: 240px;
  padding: 7px 12px 7px 32px;
  font-size: 13px;
  font-family: inherit;
  color: var(--text);
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  outline: none;
  transition: border-color 120ms, background-color 120ms;
}
.nav-search input:focus { border-color: var(--accent); background: var(--surface); }
.nav-search svg {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.nav-burger {
  display: none;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 6px 10px;
  cursor: pointer;
  color: var(--text);
}

/* ── Buttons ────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background-color 120ms, border-color 120ms;
  text-decoration: none;
}
.btn:hover { background: var(--surface-hover); border-color: var(--border-strong); }
.btn-primary {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}
.btn-primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}
.btn-ghost {
  background: transparent;
  border-color: transparent;
  color: var(--text-secondary);
}
.btn-ghost:hover { background: var(--surface-hover); color: var(--text); }

/* ── Cards ──────────────────────────────────────────── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: var(--sp-6);
  transition: border-color 120ms, box-shadow 120ms;
}
.card-hover:hover {
  border-color: var(--border-strong);
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.06);
  cursor: pointer;
}

/* ── Stats grid ─────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-4);
  margin-bottom: var(--sp-10);
}
.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: var(--sp-5);
}
.stat-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: var(--sp-2);
}
.stat-value {
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: var(--text);
  line-height: 1;
}
.stat-sub {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: var(--sp-2);
}

/* ── Sections ───────────────────────────────────────── */
.section { margin-bottom: var(--sp-12); }
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--sp-5);
}
.section-head h2 { font-size: 18px; font-weight: 600; }
.section-head .hint { font-size: 13px; color: var(--text-muted); }

/* ── Subject switcher (Home) ────────────────────────── */
.subject-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
}
.subject-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: var(--sp-6);
  cursor: pointer;
  transition: border-color 120ms, box-shadow 120ms;
}
.subject-card:hover {
  border-color: var(--border-strong);
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}
.subject-card h3 { margin-bottom: var(--sp-3); }
.subject-card .meta {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  gap: var(--sp-3);
}
.subject-card .meta strong { color: var(--text); font-weight: 600; }

/* ── Top chapters table ─────────────────────────────── */
.list {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.list-row {
  display: grid;
  grid-template-columns: 32px 1fr 80px 80px 80px 32px;
  align-items: center;
  padding: var(--sp-3) var(--sp-5);
  border-top: 1px solid var(--border);
  cursor: pointer;
  transition: background-color 120ms;
}
.list-row:first-child { border-top: none; }
.list-row:hover { background: var(--surface-hover); }
.list-row .rank {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
}
.list-row .name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
}
.list-row .name-sub {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}
.list-row .num {
  font-size: 13px;
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
  text-align: right;
}
.list-row .num strong { color: var(--text); font-weight: 600; }
.list-row .chevron { color: var(--text-muted); justify-self: end; }

/* Sort/Filter */
.toolbar {
  display: flex;
  gap: var(--sp-2);
  align-items: center;
  flex-wrap: wrap;
}
.pills {
  display: flex;
  gap: var(--sp-1);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2px;
}
.pill {
  padding: 4px 10px;
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 120ms, color 120ms;
}
.pill:hover { color: var(--text); }
.pill.active {
  background: var(--text);
  color: white;
}

/* ── Chapter detail page ────────────────────────────── */
.kv-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-4);
  margin-bottom: var(--sp-10);
}
.kv {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: var(--sp-5);
}
.kv .k { font-size: 12px; color: var(--text-muted); margin-bottom: var(--sp-1); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.kv .v { font-size: 20px; font-weight: 600; color: var(--text); }
.kv .v-sub { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }

/* Tag */
.tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 4px;
  background: var(--bg);
  color: var(--text-secondary);
  border: 1px solid var(--border);
}
.tag-accent { background: var(--accent-bg); color: var(--accent-text); border-color: transparent; }
.tag-success { background: var(--success-bg); color: var(--success); border-color: transparent; }
.tag-warning { background: var(--warning-bg); color: var(--warning); border-color: transparent; }
.tag-danger { background: var(--danger-bg); color: var(--danger); border-color: transparent; }

/* Bar (mini chart) */
.bar-row {
  display: grid;
  grid-template-columns: 80px 1fr 50px;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-2) 0;
  font-size: 13px;
}
.bar-row .lbl { color: var(--text-secondary); }
.bar-row .num { font-weight: 600; color: var(--text); text-align: right; font-variant-numeric: tabular-nums; }
.bar-track {
  height: 6px;
  background: var(--bg);
  border-radius: 3px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 3px;
}

/* ── Question detail modal ──────────────────────────── */
.modal-bg {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  z-index: 200;
  display: none;
  align-items: flex-start;
  justify-content: center;
  padding: var(--sp-10) var(--sp-4);
  overflow-y: auto;
}
.modal-bg.open { display: flex; }
.modal {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  width: 100%;
  max-width: 720px;
  margin-bottom: var(--sp-16);
}
.modal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--sp-5) var(--sp-6);
  border-bottom: 1px solid var(--border);
}
.modal-body { padding: var(--sp-6); }
.modal-section { margin-bottom: var(--sp-6); }
.modal-section h4 {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: var(--sp-3);
  font-weight: 600;
}
.q-text {
  font-size: 15px;
  line-height: 1.65;
  color: var(--text);
}
.q-meta {
  display: flex;
  gap: var(--sp-2);
  flex-wrap: wrap;
  margin-bottom: var(--sp-4);
}
.q-answer {
  font-size: 14px;
  color: var(--text-secondary);
  padding: var(--sp-3) var(--sp-4);
  background: var(--bg);
  border-radius: var(--radius);
  border-left: 3px solid var(--accent);
}
.icon-btn {
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius);
  padding: 6px;
  cursor: pointer;
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.icon-btn:hover { background: var(--surface-hover); color: var(--text); }

/* ── Pattern detail ─────────────────────────────────── */
.pattern-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: var(--sp-5);
  margin-bottom: var(--sp-3);
  transition: border-color 120ms;
}
.pattern-card:hover { border-color: var(--border-strong); }
.pattern-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-3);
  margin-bottom: var(--sp-3);
  flex-wrap: wrap;
}
.pattern-meta {
  display: flex;
  gap: var(--sp-2);
  flex-wrap: wrap;
}
.pattern-title { font-size: 14px; font-weight: 500; color: var(--text); margin-bottom: var(--sp-2); }
.pattern-sub { font-size: 12px; color: var(--text-muted); }
.pattern-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-4);
  margin-top: var(--sp-4);
  padding-top: var(--sp-4);
  border-top: 1px solid var(--border);
}

/* ── Empty states ───────────────────────────────────── */
.empty {
  padding: var(--sp-16) var(--sp-6);
  text-align: center;
  color: var(--text-muted);
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: 8px;
}
.empty h4 { color: var(--text-secondary); margin-bottom: var(--sp-2); font-size: 15px; font-weight: 500; }

/* ── Back link ──────────────────────────────────────── */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  font-family: inherit;
  margin-bottom: var(--sp-4);
}
.back-link:hover { color: var(--text); }

/* ── Mobile drawer ──────────────────────────────────── */
.drawer {
  position: fixed;
  inset: 0;
  z-index: 150;
  display: none;
}
.drawer.open { display: block; }
.drawer-bg {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
}
.drawer-panel {
  position: absolute;
  top: 0; left: 0; bottom: 0;
  width: 280px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: var(--sp-5);
}
.drawer-panel .nav-tabs {
  flex-direction: column;
  gap: var(--sp-1);
}
.drawer-panel .nav-tab {
  width: 100%;
  text-align: left;
  padding: 8px 12px;
}

/* ── Responsive ─────────────────────────────────────── */
@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .kv-grid { grid-template-columns: repeat(2, 1fr); }
  .pattern-stats { grid-template-columns: repeat(2, 1fr); }
  .subject-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .nav-tabs { display: none; }
  .nav-burger { display: inline-flex; }
  .nav-search input { width: 160px; }
  .page { padding: var(--sp-6) 0 var(--sp-12); }
  .container { padding: 0 var(--sp-4); }
  .page-header { flex-direction: column; align-items: flex-start; gap: var(--sp-3); }
  .page-header-meta { width: 100%; }
  .list-row {
    grid-template-columns: 28px 1fr 70px 24px;
    gap: var(--sp-2);
  }
  .list-row .num { font-size: 12px; }
  .list-row .num.hide-sm { display: none; }
  h1 { font-size: 24px; }
  .modal { margin: var(--sp-4); }
}
@media (max-width: 480px) {
  .stats-grid, .kv-grid, .pattern-stats { grid-template-columns: 1fr; }
  .nav-search input { width: 140px; }
}
"""


# ──────────────────────────────────────────────────────────
#  HTML shell
# ──────────────────────────────────────────────────────────
HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JEE Intelligence</title>
<meta name="description" content="Strategic JEE preparation intelligence. 414 papers, 10K+ questions, 1,118 repeating patterns.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%234F46E5'/%3E%3Ctext x='50' y='68' font-family='Inter,sans-serif' font-size='60' font-weight='700' fill='white' text-anchor='middle'%3EJ%3C/text%3E%3C/svg%3E">
<style>__CSS__</style>
</head>
<body>

<header class="nav">
  <div class="nav-inner">
    <a class="brand" onclick="go('home')" aria-label="Home">
      <span class="brand-mark">J</span>
      <span>JEE Intelligence</span>
    </a>
    <nav class="nav-tabs" role="navigation">
      <button class="nav-tab active" data-route="home" onclick="go('home')">Overview</button>
      <button class="nav-tab" data-route="physics" onclick="go('physics')">Physics</button>
      <button class="nav-tab" data-route="chemistry" onclick="go('chemistry')">Chemistry</button>
      <button class="nav-tab" data-route="mathematics" onclick="go('mathematics')">Mathematics</button>
      <button class="nav-tab" data-route="patterns" onclick="go('patterns')">Patterns</button>
    </nav>
    <div class="nav-search">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input type="search" id="search" placeholder="Search chapters, patterns…" oninput="onSearch(this.value)">
    </div>
    <button class="nav-burger" onclick="toggleDrawer()" aria-label="Menu">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</header>

<div class="drawer" id="drawer" onclick="if(event.target===this) toggleDrawer()">
  <div class="drawer-bg"></div>
  <div class="drawer-panel">
    <div style="margin-bottom: 24px; font-weight: 600; font-size: 14px;">JEE Intelligence</div>
    <nav class="nav-tabs">
      <button class="nav-tab" data-route="home" onclick="go('home');toggleDrawer()">Overview</button>
      <button class="nav-tab" data-route="physics" onclick="go('physics');toggleDrawer()">Physics</button>
      <button class="nav-tab" data-route="chemistry" onclick="go('chemistry');toggleDrawer()">Chemistry</button>
      <button class="nav-tab" data-route="mathematics" onclick="go('mathematics');toggleDrawer()">Mathematics</button>
      <button class="nav-tab" data-route="patterns" onclick="go('patterns');toggleDrawer()">Patterns</button>
    </nav>
  </div>
</div>

<main id="app" class="container page"></main>

<div class="modal-bg" id="modal" onclick="if(event.target.id==='modal') closeModal()">
  <div class="modal" role="dialog" aria-modal="true">
    <div class="modal-head">
      <div>
        <div class="eyebrow" id="modalEyebrow"></div>
        <h3 id="modalTitle" style="margin-top:4px"></h3>
      </div>
      <button class="icon-btn" onclick="closeModal()" aria-label="Close">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<script>
__DATA_PLACEHOLDER__
__JS__
</script>

</body>
</html>
"""


# ──────────────────────────────────────────────────────────
#  JS — routing + rendering
# ──────────────────────────────────────────────────────────
JS = """
const D = __DATA__;
let state = { route: 'home', subject: null, chapter: null, sortBy: 'roi', filter: 'all' };

function $(s, p=document) { return p.querySelector(s); }
function $$(s, p=document) { return Array.from(p.querySelectorAll(s)); }

function fmt(n) {
  if (n === undefined || n === null) return '—';
  return Number(n).toLocaleString('en-IN');
}
function pct(n) { return (n * 100).toFixed(0) + '%'; }
function cap(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''; }
function esc(s) {
  if (!s) return '';
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
}

// ── Routing ──────────────────────────────────────
function go(route, params={}) {
  state.route = route;
  if (params.subject !== undefined) state.subject = params.subject;
  if (params.chapter !== undefined) state.chapter = params.chapter;
  if (params.reset) { state.subject = null; state.chapter = null; state.sortBy = 'roi'; state.filter = 'all'; }

  $$('.nav-tab').forEach(t => t.classList.toggle('active', t.dataset.route === route));
  window.scrollTo({ top: 0, behavior: 'instant' });
  render();
}

function render() {
  const app = $('#app');
  if (state.route === 'home') app.innerHTML = renderHome();
  else if (['physics','chemistry','mathematics'].includes(state.route)) {
    if (state.chapter) app.innerHTML = renderChapterDetail();
    else app.innerHTML = renderSubject(state.route);
  }
  else if (state.route === 'patterns') app.innerHTML = renderPatterns();
}

// ── Home / Overview ─────────────────────────────
function renderHome() {
  const m = D.meta;
  const totalCh = D.chapters.length;
  const subjects = ['physics','chemistry','mathematics'];
  const subjectMeta = subjects.map(s => ({
    s,
    chapters: D.subjects[s] || [],
    top: (D.subjects[s] || [])[0]
  }));

  return `
    <div class="page-header">
      <div>
        <div class="eyebrow">Overview</div>
        <h1 style="margin-top:6px">Strategic JEE Preparation</h1>
        <p class="text-secondary" style="margin-top:6px; max-width: 56ch; font-size: 14px;">
          Patterns extracted from ${fmt(m.total_papers)} JEE papers (2019–2026).
          Use this to prioritize what to study, not how much.
        </p>
      </div>
      <div class="page-header-meta">
        <span class="tag">Last updated ${new Date().toLocaleDateString('en-IN', {month:'short', year:'numeric'})}</span>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat">
        <div class="stat-label">Papers analyzed</div>
        <div class="stat-value">${fmt(m.total_papers)}</div>
        <div class="stat-sub">2019 – 2026</div>
      </div>
      <div class="stat">
        <div class="stat-label">Questions extracted</div>
        <div class="stat-value">${fmt(m.total_questions)}</div>
        <div class="stat-sub">${fmt(m.total_classified)} classified</div>
      </div>
      <div class="stat">
        <div class="stat-label">Repeating patterns</div>
        <div class="stat-value">${fmt(m.total_patterns)}</div>
        <div class="stat-sub">Cross-year templates</div>
      </div>
      <div class="stat">
        <div class="stat-label">Chapters tracked</div>
        <div class="stat-value">${totalCh}</div>
        <div class="stat-sub">Ranked by ROI</div>
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2>Choose your subject</h2>
        <div class="hint">Each subject ranked by return-on-effort</div>
      </div>
      <div class="subject-grid">
        ${subjectMeta.map(s => `
          <div class="subject-card" onclick="go('${s.s}')">
            <h3>${cap(s.s)}</h3>
            <div class="meta">
              <span><strong>${s.chapters.length}</strong> chapters</span>
              <span>·</span>
              <span>Top: <strong>${s.top ? esc(s.top.chapter) : '—'}</strong></span>
              <span>·</span>
              <span>${s.top ? fmt(s.top.total) : '0'} Qs</span>
            </div>
          </div>
        `).join('')}
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2>Top 10 chapters by ROI</h2>
        <div class="hint">ROI = repeating × total / 100</div>
      </div>
      ${renderChapterList(D.chapters.slice(0, 10))}
    </div>

    <div class="section">
      <div class="section-head">
        <h2>How to use this</h2>
      </div>
      <div class="card">
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 32px;">
          <div>
            <h4 style="margin-bottom:8px">1. Identify high-ROI chapters</h4>
            <p class="text-secondary text-sm">Start with chapters where the same pattern repeats year after year. The questions are essentially free.</p>
          </div>
          <div>
            <h4 style="margin-bottom:8px">2. Practice repeating patterns</h4>
            <p class="text-secondary text-sm">A pattern that has appeared in 4+ years will almost certainly appear again. Don't relearn—rehearse.</p>
          </div>
          <div>
            <h4 style="margin-bottom:8px">3. Skip low-frequency chapters</h4>
            <p class="text-secondary text-sm">Some chapters look important but yield only a few unique questions per year. Save them for last.</p>
          </div>
        </div>
      </div>
    </div>
  `;
}

// ── Subject page (Physics / Chemistry / Maths) ──
function renderSubject(subject) {
  const chapters = (D.subjects[subject] || []).slice();
  const sorted = sortChapters(chapters, state.sortBy);

  return `
    <button class="back-link" onclick="go('home')">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
      Overview
    </button>
    <div class="page-header">
      <div>
        <div class="eyebrow">${cap(subject)}</div>
        <h1 style="margin-top:6px">${chapters.length} chapters</h1>
        <p class="text-secondary" style="margin-top:6px; font-size: 14px;">
          ${fmt(chapters.reduce((a,c)=>a+c.total,0))} questions
          across ${chapters.filter(c=>c.total>0).length} active chapters.
        </p>
      </div>
      <div class="page-header-meta">
        <div class="toolbar">
          <div class="pills">
            <button class="pill ${state.sortBy==='roi'?'active':''}" onclick="setSort('roi')">ROI</button>
            <button class="pill ${state.sortBy==='total'?'active':''}" onclick="setSort('total')">Volume</button>
            <button class="pill ${state.sortBy==='repeat'?'active':''}" onclick="setSort('repeat')">Repeats</button>
            <button class="pill ${state.sortBy==='easy'?'active':''}" onclick="setSort('easy')">Easy %</button>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      ${renderChapterList(sorted)}
    </div>
  `;
}

function setSort(by) {
  state.sortBy = by;
  render();
}

// ── Chapter list ─────────────────────────────────
function sortChapters(arr, by) {
  const a = arr.slice();
  if (by === 'roi') a.sort((x,y) => y.roi_score - x.roi_score);
  else if (by === 'total') a.sort((x,y) => y.total - x.total);
  else if (by === 'repeat') a.sort((x,y) => y.repeat_ratio - x.repeat_ratio);
  else if (by === 'easy') a.sort((x,y) => y.easy_ratio - x.easy_ratio);
  return a;
}

function renderChapterList(chapters) {
  if (!chapters.length) {
    return `<div class="empty"><h4>No chapters found</h4><p>Try a different filter.</p></div>`;
  }
  const subject = state.subject || chapters[0].subject;
  const maxRoi = Math.max(...chapters.map(c => c.roi_score), 1);
  return `
    <div class="list">
      ${chapters.map((c, i) => `
        <div class="list-row" onclick="go('${c.subject}', {chapter: ${JSON.stringify(c.chapter)}})">
          <span class="rank">${String(i+1).padStart(2,'0')}</span>
          <div>
            <div class="name">${esc(c.chapter)}</div>
            <div class="name-sub">${cap(c.subject)} · ${c.sub_topics} sub-topics</div>
          </div>
          <div class="num hide-sm">
            <div>${fmt(c.total)} Qs</div>
          </div>
          <div class="num hide-sm">
            <div><strong>${pct(c.repeat_ratio)}</strong> repeat</div>
          </div>
          <div class="num">
            <div><strong>${c.roi_score.toFixed(1)}</strong> ROI</div>
          </div>
          <div class="chevron">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

// ── Chapter detail page ──────────────────────────
function renderChapterDetail() {
  const c = D.chapters.find(x => x.subject === state.subject && x.chapter === state.chapter);
  if (!c) return `<div class="empty"><h4>Chapter not found</h4></div>`;
  const stats = D.ch_stats[state.subject]?.[state.chapter] || {};
  const trend = D.trends_by_chapter[`${state.subject}/${state.chapter}`];
  const patterns = D.patterns.filter(p => p.subject === state.subject && p.chapter === state.chapter)
                              .sort((a,b) => b.frequency - a.frequency);

  const yearEntries = trend ? Object.entries(trend.year_counts || {}).sort() : [];
  const maxYear = Math.max(...yearEntries.map(([_,n]) => n), 1);

  const diffDist = stats.by_difficulty || {};
  const totalDiff = Object.values(diffDist).reduce((a,b)=>a+b,0) || 1;

  const typeDist = stats.by_question_type || {};
  const maxType = Math.max(...Object.values(typeDist), 1);

  return `
    <button class="back-link" onclick="go('${state.subject}', {reset:true})">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
      ${cap(state.subject)}
    </button>

    <div class="page-header">
      <div>
        <div class="eyebrow">${cap(state.subject)} chapter</div>
        <h1 style="margin-top:6px">${esc(c.chapter)}</h1>
        <p class="text-secondary" style="margin-top:6px; font-size: 14px;">
          ${fmt(c.total)} questions across ${yearEntries.length} years.
          ${c.repeat_ratio > 0.7 ? 'High repeat rate — patterns reliably resurface.' : ''}
        </p>
      </div>
      <div class="page-header-meta">
        <span class="tag tag-accent">ROI ${c.roi_score.toFixed(1)}</span>
        <span class="tag">${pct(c.repeat_ratio)} repeat</span>
      </div>
    </div>

    <div class="kv-grid">
      <div class="kv">
        <div class="k">Total</div>
        <div class="v">${fmt(c.total)}</div>
        <div class="v-sub">questions</div>
      </div>
      <div class="kv">
        <div class="k">Repeating</div>
        <div class="v">${fmt(c.repeating)}</div>
        <div class="v-sub">${pct(c.repeat_ratio)} of total</div>
      </div>
      <div class="kv">
        <div class="k">Easy</div>
        <div class="v">${pct(c.easy_ratio)}</div>
        <div class="v-sub">${fmt(diffDist.Easy || 0)} easy questions</div>
      </div>
      <div class="kv">
        <div class="k">Sub-topics</div>
        <div class="v">${c.sub_topics}</div>
        <div class="v-sub">unique concepts</div>
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2>Yearly volume</h2>
        <div class="hint">Higher bars = more questions that year</div>
      </div>
      <div class="card">
        ${yearEntries.length === 0 ? '<div class="empty"><h4>No year data</h4></div>' :
          yearEntries.map(([y, n]) => `
            <div class="bar-row">
              <div class="lbl">${y}</div>
              <div class="bar-track"><div class="bar-fill" style="width: ${(n/maxYear*100).toFixed(1)}%"></div></div>
              <div class="num">${fmt(n)}</div>
            </div>
          `).join('')
        }
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2>Difficulty</h2>
      </div>
      <div class="card">
        ${Object.entries(diffDist).map(([k, v]) => `
          <div class="bar-row">
            <div class="lbl">${k}</div>
            <div class="bar-track"><div class="bar-fill" style="width: ${(v/totalDiff*100).toFixed(1)}%; background: ${k==='Easy'?'#059669':k==='Medium'?'#D97706':'#DC2626'}"></div></div>
            <div class="num">${pct(v/totalDiff)}</div>
          </div>
        `).join('') || '<div class="empty"><h4>No data</h4></div>'}
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2>Question types</h2>
      </div>
      <div class="card">
        ${Object.entries(typeDist).map(([k, v]) => `
          <div class="bar-row">
            <div class="lbl">${esc(k)}</div>
            <div class="bar-track"><div class="bar-fill" style="width: ${(v/maxType*100).toFixed(1)}%"></div></div>
            <div class="num">${fmt(v)}</div>
          </div>
        `).join('') || '<div class="empty"><h4>No data</h4></div>'}
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <h2>Repeating patterns</h2>
        <div class="hint">${patterns.length} patterns found in this chapter</div>
      </div>
      ${patterns.length === 0 ?
        '<div class="empty"><h4>No patterns catalogued yet</h4><p>Patterns emerge when 3+ similar questions appear across years.</p></div>' :
        patterns.slice(0, 30).map(p => renderPatternCard(p)).join('')
      }
      ${patterns.length > 30 ? `<p class="text-muted text-sm" style="margin-top:16px">Showing 30 of ${patterns.length} patterns.</p>` : ''}
    </div>
  `;
}

function renderPatternCard(p) {
  const yearTxt = (p.years || []).slice(0, 6).join(', ');
  return `
    <div class="pattern-card" onclick='showQuestion(${JSON.stringify(p)})'>
      <div class="pattern-head">
        <div class="pattern-meta">
          <span class="tag tag-accent">${cap(p.subject || state.subject)}</span>
          <span class="tag">${esc(p.sub_topic || p.chapter || '')}</span>
          ${p.difficulty ? `<span class="tag ${p.difficulty==='Easy'?'tag-success':p.difficulty==='Medium'?'tag-warning':'tag-danger'}">${esc(p.difficulty)}</span>` : ''}
        </div>
        <div class="pattern-sub">
          <strong>${p.frequency}</strong> occurrences · ${yearTxt}
        </div>
      </div>
      <div class="pattern-title">${esc(p.core_concept || 'Pattern')}</div>
      <div class="pattern-stats">
        <div>
          <div class="text-xs text-muted" style="text-transform:uppercase; letter-spacing:.06em; margin-bottom:2px;">Type</div>
          <div style="font-weight:500">${esc(p.question_type || '—')}</div>
        </div>
        <div>
          <div class="text-xs text-muted" style="text-transform:uppercase; letter-spacing:.06em; margin-bottom:2px;">Formula</div>
          <div class="mono" style="font-size:12px">${esc(p.key_formula || '—')}</div>
        </div>
        <div>
          <div class="text-xs text-muted" style="text-transform:uppercase; letter-spacing:.06em; margin-bottom:2px;">Trap</div>
          <div style="font-size:13px; color:var(--text-secondary)">${esc(p.common_trap || '—')}</div>
        </div>
        <div>
          <div class="text-xs text-muted" style="text-transform:uppercase; letter-spacing:.06em; margin-bottom:2px;">Years</div>
          <div style="font-weight:500">${(p.years || []).length} unique</div>
        </div>
      </div>
    </div>
  `;
}

// ── Patterns page (cross-subject) ────────────────
function renderPatterns() {
  const all = D.patterns.slice().sort((a,b) => b.frequency - a.frequency);

  return `
    <div class="page-header">
      <div>
        <div class="eyebrow">Patterns</div>
        <h1 style="margin-top:6px">${fmt(all.length)} repeating patterns</h1>
        <p class="text-secondary" style="margin-top:6px; font-size: 14px; max-width:56ch;">
          Question templates that appear in multiple years.
          Higher frequency = more likely to appear again.
        </p>
      </div>
    </div>

    <div class="section">
      ${all.slice(0, 60).map(p => renderPatternCard(p)).join('')}
      ${all.length > 60 ? `<p class="text-muted text-sm" style="margin-top:16px">Showing 60 of ${fmt(all.length)} patterns. Use search to find more.</p>` : ''}
    </div>
  `;
}

// ── Modal (question / pattern detail) ────────────
function showQuestion(p) {
  $('#modalEyebrow').textContent = `${cap(p.subject || '')} · ${esc(p.sub_topic || p.chapter || '')}`;
  $('#modalTitle').textContent = p.core_concept || 'Pattern detail';

  const reps = (p.exams || []).slice(0, 6).join(', ');
  const years = (p.years || []).slice(0, 6).join(', ');

  $('#modalBody').innerHTML = `
    <div class="q-meta">
      ${p.difficulty ? `<span class="tag ${p.difficulty==='Easy'?'tag-success':p.difficulty==='Medium'?'tag-warning':'tag-danger'}">${esc(p.difficulty)}</span>` : ''}
      ${p.question_type ? `<span class="tag">${esc(p.question_type)}</span>` : ''}
      <span class="tag tag-accent">${p.frequency}× occurrences</span>
      <span class="tag">${years}</span>
      <span class="tag">${reps}</span>
    </div>

    <div class="modal-section">
      <h4>Representative question</h4>
      <div class="q-text">${esc(p.representative_question || '—')}</div>
    </div>

    ${p.representative_answer ? `
      <div class="modal-section">
        <h4>Answer</h4>
        <div class="q-answer">${esc(p.representative_answer)}</div>
      </div>
    ` : ''}

    <div class="modal-section">
      <h4>Key formula</h4>
      <div class="mono" style="padding:12px; background:var(--bg); border-radius:6px;">${esc(p.key_formula || '—')}</div>
    </div>

    <div class="modal-section">
      <h4>Common trap</h4>
      <div style="font-size:14px; color:var(--text-secondary); line-height:1.6;">${esc(p.common_trap || '—')}</div>
    </div>

    <div class="modal-section">
      <h4>All years</h4>
      <div style="display:flex; gap:6px; flex-wrap:wrap;">
        ${(p.years || []).map(y => `<span class="tag">${y}</span>`).join('')}
      </div>
    </div>
  `;
  $('#modal').classList.add('open');
}

function closeModal() {
  $('#modal').classList.remove('open');
}

// ── Search ───────────────────────────────────────
function onSearch(q) {
  q = q.trim().toLowerCase();
  if (!q) {
    if (state.route !== 'home') render();
    return;
  }

  const chapterHits = D.chapters.filter(c =>
    c.chapter.toLowerCase().includes(q) ||
    c.subject.toLowerCase().includes(q)
  );
  const patternHits = D.patterns.filter(p =>
    (p.core_concept || '').toLowerCase().includes(q) ||
    (p.sub_topic || '').toLowerCase().includes(q) ||
    (p.chapter || '').toLowerCase().includes(q)
  ).slice(0, 20);

  $('#app').innerHTML = `
    <div class="page-header">
      <div>
        <div class="eyebrow">Search</div>
        <h1 style="margin-top:6px">${fmt(chapterHits.length + patternHits.length)} results</h1>
        <p class="text-secondary" style="margin-top:6px; font-size:14px;">for "${esc(q)}"</p>
      </div>
      <button class="btn btn-ghost" onclick="document.getElementById('search').value=''; go('home')">Clear</button>
    </div>

    ${chapterHits.length > 0 ? `
      <div class="section">
        <div class="section-head"><h2>Chapters</h2><div class="hint">${chapterHits.length} matches</div></div>
        ${renderChapterList(chapterHits.slice(0, 15))}
      </div>
    ` : ''}

    ${patternHits.length > 0 ? `
      <div class="section">
        <div class="section-head"><h2>Patterns</h2><div class="hint">${patternHits.length} matches</div></div>
        ${patternHits.map(p => renderPatternCard(p)).join('')}
      </div>
    ` : ''}

    ${chapterHits.length === 0 && patternHits.length === 0 ? `
      <div class="empty"><h4>No results</h4><p>Try a different keyword.</p></div>
    ` : ''}
  `;
}

// ── Drawer ───────────────────────────────────────
function toggleDrawer() {
  $('#drawer').classList.toggle('open');
}

// ── Keyboard ─────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closeModal();
    if ($('#drawer').classList.contains('open')) toggleDrawer();
  }
  if (e.key === '/' && document.activeElement !== $('#search')) {
    e.preventDefault();
    $('#search').focus();
  }
});

// ── Init ─────────────────────────────────────────
go('home');
"""


# ──────────────────────────────────────────────────────────
#  Build
# ──────────────────────────────────────────────────────────
def build():
    data = load_data()
    data_json = embed_data(data)
    html_out = HTML_HEAD.replace("__CSS__", CSS).replace("__JS__", JS).replace("__DATA__", data_json).replace("__DATA_PLACEHOLDER__", "")

    with open(OUT_PATH, "w") as f:
        f.write(html_out)
    size_kb = os.path.getsize(OUT_PATH) / 1024
    print(f"Wrote {OUT_PATH} ({size_kb:.0f} KB)")
    print(f"  Chapters: {len(data['chapters'])}")
    print(f"  Patterns: {len(data['patterns'])}")
    print(f"  Trends: {len(data['trends'])}")
    print(f"  Questions: {len(data['questions'])}")


if __name__ == "__main__":
    build()