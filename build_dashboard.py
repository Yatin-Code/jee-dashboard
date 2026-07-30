#!/usr/bin/env python3
"""
JEE Strategy Dashboard Builder
Creates a self-contained HTML file with embedded JSON data, CSS, and JS.
Target: AIR <200 (Top 5 IIT CSE)
"""
import json, os

BASE = "/data/data/com.termux/files/home/jee-analysis"

with open(f"{BASE}/raw_data/final_data.json") as f:
    data = json.load(f)

# Prepare data for embedding
# We need: chapter_rankings, patterns (top ones), trends, chapter_stats, questions (classified only)

# Top patterns by frequency (for the dashboard)
patterns = sorted(data['patterns'], key=lambda p: -p['frequency'])

# Questions — only classified ones, and limit text length for file size
classified_qs = []
for q in data['questions']:
    if q.get('chapter') and q['chapter'] != 'Unclassified':
        classified_qs.append({
            'subject': q['subject'],
            'chapter': q['chapter'],
            'sub_topic': q.get('sub_topic', ''),
            'difficulty': q.get('difficulty', 'Medium'),
            'question_type': q.get('question_type', 'MCQ'),
            'year': q['year'],
            'exam': q['exam'],
            'text': q['text'][:600],
            'answer': q.get('answer'),
            'key_formula': q.get('key_formula'),
            'common_trap': q.get('common_trap'),
            'core_concept': q.get('core_concept'),
            'cluster_id': q.get('cluster_id'),
            'cluster_size': q.get('cluster_size', 1),
            'needs_figure': q.get('needs_figure', False),
        })

# Chapter rankings — clean up
chapter_rankings = []
for c in data['chapter_rankings']:
    if c['chapter'] != 'Unclassified':
        chapter_rankings.append({
            'subject': c['subject'],
            'chapter': c['chapter'],
            'total': c['total'],
            'repeating': c['repeating'],
            'repeat_ratio': round(c['repeat_ratio'] * 100, 1),
            'easy_ratio': round(c['easy_ratio'] * 100, 1),
            'roi_score': round(c['roi_score'], 1),
            'sub_topics': c.get('sub_topics', 0),
        })

# Trends — filter out Unclassified
trends = [t for t in data['trends'] if t['chapter'] != 'Unclassified']

# Chapter stats for detailed view
chapter_stats = {}
for subj in data['chapter_stats']:
    chapter_stats[subj] = {}
    for chap, stats in data['chapter_stats'][subj].items():
        if chap != 'Unclassified':
            chapter_stats[subj][chap] = stats

# Metadata
metadata = data['metadata']

# Build embedded JSON
embedded = {
    'metadata': metadata,
    'chapter_rankings': chapter_rankings,
    'patterns': patterns[:200],  # Top 200 patterns
    'trends': trends,
    'chapter_stats': chapter_stats,
    'questions': classified_qs,
}

embedded_json = json.dumps(embedded, ensure_ascii=False, separators=(',', ':'))

print(f"Embedded JSON size: {len(embedded_json) // 1024} KB")
print(f"Questions: {len(classified_qs)}")
print(f"Patterns: {len(patterns[:200])}")
print(f"Chapter rankings: {len(chapter_rankings)}")
print(f"Trends: {len(trends)}")

# Now build the HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JEE Strategy Dashboard | AIR <200</title>
<style>
:root {{
  --bg: #0a0a0f;
  --card: #12121a;
  --border: #1e1e2e;
  --text: #e0e0e8;
  --text-dim: #8080a0;
  --accent: #6c5ce7;
  --accent2: #00cec9;
  --green: #00b894;
  --yellow: #fdcb6e;
  --red: #e17055;
  --blue: #74b9ff;
  --radius: 12px;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ 
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--accent2); text-decoration: none; }}

/* NAV */
.nav {{
  position: sticky; top: 0; z-index: 100;
  background: rgba(10,10,15,0.95); backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  padding: 12px 20px; display: flex; align-items: center; gap: 20px;
}}
.nav-title {{ font-size: 1.1rem; font-weight: 700; color: var(--accent); white-space: nowrap; }}
.nav-subjects {{ display: flex; gap: 8px; }}
.nav-btn {{
  padding: 6px 16px; border-radius: 20px; border: 1px solid var(--border);
  background: transparent; color: var(--text-dim); cursor: pointer;
  font-size: 0.85rem; transition: all 0.2s;
}}
.nav-btn:hover {{ border-color: var(--accent); color: var(--text); }}
.nav-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
.nav-search {{
  flex: 1; max-width: 300px; padding: 6px 14px; border-radius: 20px;
  border: 1px solid var(--border); background: var(--card); color: var(--text);
  font-size: 0.85rem; outline: none;
}}
.nav-search:focus {{ border-color: var(--accent); }}

/* LAYOUT */
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

/* HOME VIEW */
.home-hero {{
  text-align: center; padding: 40px 20px;
}}
.home-hero h1 {{ font-size: 2rem; color: var(--text); margin-bottom: 8px; }}
.home-hero p {{ color: var(--text-dim); font-size: 1rem; max-width: 600px; margin: 0 auto; }}
.home-stats {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px; margin: 32px 0;
}}
.stat-card {{
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; text-align: center;
}}
.stat-card .num {{ font-size: 2rem; font-weight: 800; color: var(--accent); }}
.stat-card .label {{ font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }}

/* SUBJECT VIEW */
.subject-grid {{
  display: grid; grid-template-columns: 1fr; gap: 12px;
}}
.chapter-row {{
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 20px; display: flex; align-items: center; gap: 16px;
  cursor: pointer; transition: all 0.2s;
}}
.chapter-row:hover {{ border-color: var(--accent); transform: translateX(4px); }}
.chapter-rank {{ font-size: 1.5rem; font-weight: 800; color: var(--text-dim); min-width: 40px; }}
.chapter-name {{ flex: 1; }}
.chapter-name h3 {{ font-size: 1rem; color: var(--text); }}
.chapter-name .sub {{ font-size: 0.75rem; color: var(--text-dim); margin-top: 2px; }}
.chapter-badges {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.badge {{
  padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 600;
  white-space: nowrap;
}}
.badge-roi {{ background: rgba(108,92,231,0.2); color: var(--accent); }}
.badge-repeat {{ background: rgba(0,206,201,0.15); color: var(--accent2); }}
.badge-easy {{ background: rgba(0,184,148,0.15); color: var(--green); }}
.badge-hard {{ background: rgba(225,112,85,0.15); color: var(--red); }}
.badge-trend-up {{ background: rgba(0,184,148,0.15); color: var(--green); }}
.badge-trend-down {{ background: rgba(225,112,85,0.15); color: var(--red); }}
.badge-trend-stable {{ background: rgba(253,203,110,0.15); color: var(--yellow); }}

/* CHAPTER DETAIL */
.chapter-detail {{ display: none; }}
.back-btn {{
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: 8px; border: 1px solid var(--border);
  background: var(--card); color: var(--text-dim); cursor: pointer;
  font-size: 0.85rem; margin-bottom: 16px; transition: all 0.2s;
}}
.back-btn:hover {{ border-color: var(--accent); color: var(--text); }}
.detail-header {{
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 24px; margin-bottom: 16px;
}}
.detail-header h2 {{ font-size: 1.5rem; margin-bottom: 8px; }}
.detail-header .meta {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; }}
.detail-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px; margin-bottom: 20px;
}}
.detail-stat {{
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 16px; text-align: center;
}}
.detail-stat .v {{ font-size: 1.5rem; font-weight: 700; }}
.detail-stat .l {{ font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; }}

/* TREND CHART */
.trend-chart {{
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; margin-bottom: 20px;
}}
.trend-chart h3 {{ margin-bottom: 16px; font-size: 1rem; }}
.bar-chart {{ display: flex; align-items: flex-end; gap: 4px; height: 120px; }}
.bar {{
  flex: 1; min-width: 30px; background: linear-gradient(180deg, var(--accent), var(--accent2));
  border-radius: 4px 4px 0 0; position: relative; min-height: 4px;
  transition: opacity 0.2s;
}}
.bar:hover {{ opacity: 0.8; }}
.bar .bar-label {{
  position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%);
  font-size: 0.65rem; color: var(--text-dim); white-space: nowrap;
}}
.bar .bar-val {{
  position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
  font-size: 0.65rem; color: var(--text); font-weight: 600;
}}

/* PATTERNS */
.section-title {{
  font-size: 1.1rem; font-weight: 700; margin: 24px 0 12px;
  display: flex; align-items: center; gap: 8px;
}}
.section-title .count {{ font-size: 0.75rem; color: var(--text-dim); font-weight: 400; }}
.pattern-card {{
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 20px; margin-bottom: 10px;
}}
.pattern-card .p-header {{
  display: flex; align-items: center; gap: 12px; margin-bottom: 8px; flex-wrap: wrap;
}}
.pattern-card .p-topic {{ font-weight: 700; font-size: 0.95rem; }}
.pattern-card .p-body {{ font-size: 0.85rem; color: var(--text-dim); }}
.pattern-card .p-concept {{ margin: 8px 0; }}
.pattern-card .p-formula {{
  background: rgba(108,92,231,0.1); border-left: 3px solid var(--accent);
  padding: 8px 12px; border-radius: 4px; margin: 8px 0;
  font-family: 'Courier New', monospace; font-size: 0.8rem; color: var(--accent2);
}}
.pattern-card .p-trap {{
  background: rgba(225,112,85,0.08); border-left: 3px solid var(--red);
  padding: 8px 12px; border-radius: 4px; margin: 8px 0; font-size: 0.8rem;
}}
.pattern-card .p-years {{ display: flex; gap: 4px; flex-wrap: wrap; margin-top: 8px; }}
.pattern-card .p-year {{
  padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;
  background: var(--border); color: var(--text-dim);
}}
.pattern-card .p-freq {{
  padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;
  background: rgba(0,184,148,0.15); color: var(--green);
}}
.pattern-card .p-question {{
  background: rgba(0,0,0,0.3); border-radius: 6px; padding: 12px;
  margin: 8px 0; font-size: 0.8rem; color: var(--text); max-height: 200px;
  overflow-y: auto; white-space: pre-wrap;
}}

/* QUESTION LIST */
.q-card {{
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px 18px; margin-bottom: 8px;
}}
.q-card .q-meta {{
  display: flex; gap: 8px; align-items: center; margin-bottom: 8px; flex-wrap: wrap;
}}
.q-card .q-text {{
  font-size: 0.85rem; color: var(--text); white-space: pre-wrap;
  max-height: 150px; overflow-y: auto;
}}
.q-card .q-ans {{
  margin-top: 8px; font-size: 0.8rem; color: var(--green); font-weight: 600;
}}

/* FILTERS */
.filters {{
  display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px;
}}
.filter-btn {{
  padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border);
  background: var(--card); color: var(--text-dim); cursor: pointer;
  font-size: 0.8rem; transition: all 0.2s;
}}
.filter-btn:hover {{ border-color: var(--accent); }}
.filter-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}

/* HIDE */
.hidden {{ display: none !important; }}

/* SCROLLBAR */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--text-dim); }}

/* RESPONSIVE */
@media (max-width: 768px) {{
  .nav {{ flex-wrap: wrap; }}
  .nav-search {{ max-width: 100%; order: 3; }}
  .container {{ padding: 12px; }}
  .home-stats {{ grid-template-columns: repeat(2, 1fr); }}
  .chapter-row {{ flex-wrap: wrap; }}
  .detail-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-title">JEE Strategy</div>
  <div class="nav-subjects">
    <button class="nav-btn active" onclick="showHome()">Home</button>
    <button class="nav-btn" onclick="showSubject('physics')">Physics</button>
    <button class="nav-btn" onclick="showSubject('chemistry')">Chemistry</button>
    <button class="nav-btn" onclick="showSubject('mathematics')">Maths</button>
  </div>
  <input class="nav-search" type="text" placeholder="Search chapters, topics..." oninput="handleSearch(this.value)">
</nav>

<div class="container">
  <!-- HOME VIEW -->
  <div id="home-view">
    <div class="home-hero">
      <h1>JEE Pattern Intelligence</h1>
      <p>Built from 414 actual JEE papers (2019-2026), 10,051 questions, 1,118 repeating patterns. Your edge for AIR &lt;200.</p>
    </div>
    <div class="home-stats">
      <div class="stat-card"><div class="num">{metadata.get('total_questions', 10051)}</div><div class="label">Questions Analyzed</div></div>
      <div class="stat-card"><div class="num">414</div><div class="label">Papers Processed</div></div>
      <div class="stat-card"><div class="num">1,118</div><div class="label">Repeating Patterns</div></div>
      <div class="stat-card"><div class="num">{len(chapter_rankings)}</div><div class="label">Chapters Ranked</div></div>
      <div class="stat-card"><div class="num">2019-26</div><div class="label">Year Range</div></div>
    </div>
    <div class="section-title">Top 10 Highest ROI Chapters <span class="count">across all subjects</span></div>
    <div id="home-top-chapters"></div>
  </div>

  <!-- SUBJECT VIEW -->
  <div id="subject-view" class="hidden">
    <h2 id="subject-title" style="margin-bottom:16px"></h2>
    <div class="filters">
      <button class="filter-btn active" onclick="filterChapters('roi', this)">By ROI</button>
      <button class="filter-btn" onclick="filterChapters('frequency', this)">By Frequency</button>
      <button class="filter-btn" onclick="filterChapters('easy', this)">Easiest First</button>
    </div>
    <div id="chapter-list" class="subject-grid"></div>
  </div>

  <!-- CHAPTER DETAIL VIEW -->
  <div id="detail-view" class="chapter-detail">
    <button class="back-btn" onclick="goBack()">← Back</button>
    <div id="detail-content"></div>
  </div>
</div>

<script>
const DATA = {embedded_json};

let currentSubject = '';
let currentChapter = '';
let currentFilter = 'roi';
let searchQuery = '';

// ===== HOME VIEW =====
function showHome() {{
  document.getElementById('home-view').classList.remove('hidden');
  document.getElementById('subject-view').classList.add('hidden');
  document.getElementById('detail-view').classList.remove('chapter-detail');
  document.getElementById('detail-view').style.display = 'none';
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.querySelector('.nav-btn').classList.add('active');
  renderHomeTopChapters();
}}

function renderHomeTopChapters() {{
  const container = document.getElementById('home-top-chapters');
  const top = [...DATA.chapter_rankings].sort((a,b) => b.roi_score - a.roi_score).slice(0, 10);
  container.innerHTML = top.map((c, i) => {{
    const trend = DATA.trends.find(t => t.subject === c.subject && t.chapter === c.chapter);
    const trendBadge = trend ? `<span class="badge badge-trend-${{trend.trend}}">${{trend.trend === 'up' ? '↑ Rising' : trend.trend === 'down' ? '↓ Falling' : '→ Stable'}}</span>` : '';
    return `<div class="chapter-row" onclick="showSubject('${{c.subject}}'); setTimeout(() => showChapter('${{c.subject}}','${{c.chapter}}'), 100)">
      <div class="chapter-rank">${{i+1}}</div>
      <div class="chapter-name">
        <h3>${{c.chapter}}</h3>
        <div class="sub">${{c.subject.charAt(0).toUpperCase()+c.subject.slice(1)}} · ${{c.total}} questions · ${{c.sub_topics}} sub-topics</div>
      </div>
      <div class="chapter-badges">
        <span class="badge badge-roi">ROI ${{c.roi_score}}</span>
        <span class="badge badge-repeat">${{c.repeat_ratio}}% repeat</span>
        ${{c.easy_ratio > 20 ? `<span class="badge badge-easy">${{c.easy_ratio}}% easy</span>` : ''}}
        ${{trendBadge}}
      </div>
    </div>`;
  }}).join('');
}}

// ===== SUBJECT VIEW =====
function showSubject(subject) {{
  currentSubject = subject;
  document.getElementById('home-view').classList.add('hidden');
  document.getElementById('subject-view').classList.remove('hidden');
  document.getElementById('detail-view').style.display = 'none';
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const navMap = {{'physics':1, 'chemistry':2, 'mathematics':3}};
  if (navMap[subject] !== undefined) {{
    document.querySelectorAll('.nav-btn')[navMap[subject]].classList.add('active');
  }}
  document.getElementById('subject-title').textContent = subject.charAt(0).toUpperCase() + subject.slice(1) + ' — Chapter Rankings';
  renderChapters();
}}

function filterChapters(type, btn) {{
  currentFilter = type;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderChapters();
}}

function renderChapters() {{
  let chapters = DATA.chapter_rankings.filter(c => c.subject === currentSubject);
  if (searchQuery) {{
    const q = searchQuery.toLowerCase();
    chapters = chapters.filter(c => c.chapter.toLowerCase().includes(q) || 
      DATA.questions.some(qu => qu.subject === c.subject && qu.chapter === c.chapter && qu.sub_topic && qu.sub_topic.toLowerCase().includes(q)));
  }}
  if (currentFilter === 'roi') chapters.sort((a,b) => b.roi_score - a.roi_score);
  else if (currentFilter === 'frequency') chapters.sort((a,b) => b.total - a.total);
  else if (currentFilter === 'easy') chapters.sort((a,b) => b.easy_ratio - a.easy_ratio);

  const container = document.getElementById('chapter-list');
  container.innerHTML = chapters.map((c, i) => {{
    const trend = DATA.trends.find(t => t.subject === c.subject && t.chapter === c.chapter);
    const trendBadge = trend ? `<span class="badge badge-trend-${{trend.trend}}">${{trend.trend === 'up' ? '↑' : trend.trend === 'down' ? '↓' : '→'}}</span>` : '';
    return `<div class="chapter-row" onclick="showChapter('${{c.subject}}','${{c.chapter.replace(/'/g,"\\'")}}')">
      <div class="chapter-rank">${{i+1}}</div>
      <div class="chapter-name">
        <h3>${{c.chapter}}</h3>
        <div class="sub">${{c.total}} questions · ${{c.sub_topics}} sub-topics · ${{c.repeat_ratio}}% repeating</div>
      </div>
      <div class="chapter-badges">
        <span class="badge badge-roi">ROI ${{c.roi_score}}</span>
        <span class="badge badge-repeat">${{c.repeat_ratio}}% repeat</span>
        ${{c.easy_ratio > 15 ? `<span class="badge badge-easy">${{c.easy_ratio}}% easy</span>` : `<span class="badge badge-hard">${{c.easy_ratio}}% easy</span>`}}
        ${{trendBadge}}
      </div>
    </div>`;
  }}).join('');
}}

// ===== CHAPTER DETAIL VIEW =====
function showChapter(subject, chapter) {{
  currentChapter = chapter;
  document.getElementById('home-view').classList.add('hidden');
  document.getElementById('subject-view').classList.add('hidden');
  document.getElementById('detail-view').style.display = 'block';
  document.getElementById('detail-view').classList.add('chapter-detail');
  
  const stats = DATA.chapter_stats[subject]?.[chapter];
  const ranking = DATA.chapter_rankings.find(c => c.subject === subject && c.chapter === chapter);
  const trend = DATA.trends.find(t => t.subject === subject && t.chapter === chapter);
  const patterns = DATA.patterns.filter(p => p.subject === subject && p.chapter === chapter);
  const questions = DATA.questions.filter(q => q.subject === subject && q.chapter === chapter);

  // Sort patterns by frequency
  patterns.sort((a,b) => b.frequency - a.frequency);

  let html = `<div class="detail-header">
    <h2>${{chapter}}</h2>
    <div style="color:var(--text-dim);font-size:0.9rem">${{subject.charAt(0).toUpperCase()+subject.slice(1)}}</div>
    <div class="meta">
      <span class="badge badge-roi">ROI ${{ranking?.roi_score || 'N/A'}}</span>
      <span class="badge badge-repeat">${{ranking?.repeat_ratio || 0}}% repeating</span>
      <span class="badge badge-easy">${{ranking?.easy_ratio || 0}}% easy</span>
      ${{trend ? `<span class="badge badge-trend-${{trend.trend}}">${{trend.trend === 'up' ? '↑ Rising' : trend.trend === 'down' ? '↓ Falling' : '→ Stable'}}</span>` : ''}}
    </div>
  </div>`;

  // Stats grid
  if (stats) {{
    html += `<div class="detail-grid">
      <div class="detail-stat"><div class="v" style="color:var(--accent)">${{stats.total_questions}}</div><div class="l">Total Questions</div></div>
      <div class="detail-stat"><div class="v" style="color:var(--accent2)">${{patterns.length}}</div><div class="l">Repeating Patterns</div></div>
      <div class="detail-stat"><div class="v" style="color:var(--green)">${{stats.by_difficulty?.Easy || 0}}</div><div class="l">Easy</div></div>
      <div class="detail-stat"><div class="v" style="color:var(--yellow)">${{stats.by_difficulty?.Medium || 0}}</div><div class="l">Medium</div></div>
      <div class="detail-stat"><div class="v" style="color:var(--red)">${{stats.by_difficulty?.Hard || 0}}</div><div class="l">Hard</div></div>
    </div>`;
  }}

  // Year-wise trend chart
  if (stats?.by_year) {{
    const years = Object.keys(stats.by_year).sort();
    const maxVal = Math.max(...Object.values(stats.by_year));
    html += `<div class="trend-chart"><h3>Year-wise Distribution</h3><div class="bar-chart">`;
    html += years.map(y => {{
      const v = stats.by_year[y];
      const h = (v / maxVal * 100);
      return `<div class="bar" style="height:${{h}}%"><span class="bar-val">${{v}}</span><span class="bar-label">${{y}}</span></div>`;
    }}).join('');
    html += `</div></div>`;
  }}

  // Difficulty distribution
  if (stats?.by_difficulty) {{
    html += `<div class="trend-chart"><h3>Difficulty Distribution</h3><div style="display:flex;gap:12px;align-items:center;">`;
    const total = stats.total_questions || 1;
    const diffs = [['Easy', 'var(--green)'], ['Medium', 'var(--yellow)'], ['Hard', 'var(--red)']];
    diffs.forEach(([d, color]) => {{
      const v = stats.by_difficulty[d] || 0;
      const pct = (v / total * 100).toFixed(1);
      html += `<div style="flex:1;text-align:center;">
        <div style="height:8px;border-radius:4px;background:${{color}};width:${{pct}}%;margin:0 auto 4px;"></div>
        <div style="font-size:0.8rem;font-weight:600;">${{d}}: ${{v}} (${{pct}}%)</div>
      </div>`;
    }});
    html += `</div></div>`;
  }}

  // Question types
  if (stats?.by_question_type) {{
    html += `<div class="trend-chart"><h3>Question Types</h3><div style="display:flex;gap:12px;flex-wrap:wrap;">`;
    Object.entries(stats.by_question_type).sort((a,b) => b[1] - a[1]).forEach(([type, count]) => {{
      html += `<span class="badge" style="background:var(--border)">${{type}}: ${{count}}</span>`;
    }});
    html += `</div></div>`;
  }}

  // Repeating Patterns
  html += `<div class="section-title">Repeating Patterns <span class="count">${{patterns.length}} patterns found</span></div>`;
  if (patterns.length === 0) {{
    html += `<p style="color:var(--text-dim)">No repeating patterns found for this chapter.</p>`;
  }} else {{
    patterns.forEach((p, i) => {{
      html += `<div class="pattern-card">
        <div class="p-header">
          <span class="p-freq">×${{p.frequency}}</span>
          <span class="p-topic">${{p.sub_topic || 'General'}}</span>
          <span class="badge" style="background:var(--border)">${{p.difficulty}}</span>
          <span class="badge" style="background:var(--border)">${{p.question_type}}</span>
        </div>
        ${{p.core_concept ? `<div class="p-concept p-body">${{p.core_concept}}</div>` : ''}}
        ${{p.key_formula ? `<div class="p-formula">Formula: ${{p.key_formula}}</div>` : ''}}
        ${{p.common_trap ? `<div class="p-trap">⚠ Common Trap: ${{p.common_trap}}</div>` : ''}}
        <div class="p-years">
          ${{p.years.map(y => `<span class="p-year">${{y}}</span>`).join('')}}
        </div>
        ${{p.representative_question ? `<div class="p-question">${{p.representative_question.substring(0, 400)}}${{p.representative_question.length > 400 ? '...' : ''}}</div>` : ''}}
        ${{p.representative_answer ? `<div class="q-ans">Answer: ${{p.representative_answer}}</div>` : ''}}
      </div>`;
    }});
  }}

  // All Questions
  html += `<div class="section-title">All Questions <span class="count">${{questions.length}} questions</span></div>`;
  const sortedQs = questions.sort((a,b) => (b.year || '').localeCompare(a.year || ''));
  sortedQs.forEach((q, i) => {{
    html += `<div class="q-card">
      <div class="q-meta">
        <span class="badge" style="background:var(--border)">${{q.year}}</span>
        <span class="badge" style="background:var(--border)">${{q.exam}}</span>
        <span class="badge" style="background:var(--border)">${{q.difficulty}}</span>
        ${{q.sub_topic ? `<span class="badge" style="background:rgba(108,92,231,0.15);color:var(--accent)">${{q.sub_topic}}</span>` : ''}}
        ${{q.cluster_size > 1 ? `<span class="badge badge-repeat">×${{q.cluster_size}} repeat</span>` : ''}}
      </div>
      <div class="q-text">${{q.text}}</div>
      ${{q.answer ? `<div class="q-ans">Answer: ${{q.answer}}</div>` : ''}}
    </div>`;
  }});

  document.getElementById('detail-content').innerHTML = html;
  window.scrollTo(0, 0);
}}

// ===== NAVIGATION =====
function goBack() {{
  if (currentSubject) {{
    showSubject(currentSubject);
  }} else {{
    showHome();
  }}
}}

function handleSearch(val) {{
  searchQuery = val;
  if (!document.getElementById('subject-view').classList.contains('hidden')) {{
    renderChapters();
  }} else if (!document.getElementById('home-view').classList.contains('hidden')) {{
    // search across all chapters
  }}
}}

// INIT
showHome();
</script>
</body>
</html>'''

output_path = f"{BASE}/JEE_Dashboard.html"
with open(output_path, "w") as f:
    f.write(html)

print(f"\nDashboard saved to: {output_path}")
print(f"File size: {os.path.getsize(output_path) // 1024} KB")