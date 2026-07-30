#!/usr/bin/env python3
"""
JEE Intelligence Dashboard v2 — Professional rebuild
Applies: ui-design, ux-design, responsive-design, navigation-design,
usability, design-trends, visual-direction, component-patterns,
web-typography, color-theory, agent-ui-design, branding-identity

Design system:
- Dark mode first (#0A0A0F base)
- 8px baseline grid
- 2 font families: Inter (body) + Space Grotesk (display)
- Color: monochrome + 2 accents (purple #7C6CF0 + cyan #00D4FF)
- 60-30-10 rule
- Max 3 clicks to any question
- Touch targets 44px+
- Animated stat counters, scroll reveals, modal system
"""
import json, os

BASE = "/data/data/com.termux/files/home/jee-analysis"

with open(f"{BASE}/raw_data/embedded_compact.json") as f:
    embedded_json = f.read()

# ═══════════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════════════════════════════════

HTML_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JEE Intelligence — AIR&lt;200 Strategy</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* ═══ DESIGN TOKENS ═══ */
:root {
  /* Primitive palette */
  --purple-50:#F3F1FF;--purple-100:#E9E5FF;--purple-200:#D4CEFF;--purple-300:#B8AEFF;
  --purple-400:#9B87FF;--purple-500:#7C6CF0;--purple-600:#6B4FE6;--purple-700:#5A3DDC;
  --cyan-400:#33DDFF;--cyan-500:#00D4FF;--cyan-600:#00B8E0;
  --green-500:#2DD4A8;--yellow-500:#F5C451;--red-500:#F0564F;--orange-500:#F97316;
  --gray-050:#F5F5F8;--gray-100:#E8E8F0;--gray-200:#D0D0DE;--gray-300:#A8A8BC;
  --gray-400:#7878A0;--gray-500:#5A5A78;--gray-600:#3E3E58;--gray-700:#2A2A40;
  --gray-800:#1A1A28;--gray-900:#12121E;--gray-950:#0A0A12;--gray-975:#06060A;

  /* Semantic tokens */
  --bg-base:#0A0A12;
  --bg-surface:#12121E;
  --bg-elevated:#1A1A28;
  --bg-hover:#22223A;
  --glass:rgba(18,18,30,0.65);
  --glass-border:rgba(124,108,240,0.12);
  --glass-border-hover:rgba(124,108,240,0.3);

  --text-primary:#E8E8F0;
  --text-secondary:#9090B0;
  --text-tertiary:#5A5A78;
  --text-faint:#3E3E58;

  --accent:#7C6CF0;
  --accent-hover:#9B87FF;
  --accent-glow:rgba(124,108,240,0.35);
  --cyan:#00D4FF;
  --cyan-glow:rgba(0,212,255,0.2);
  --success:#2DD4A8;
  --warning:#F5C451;
  --danger:#F0564F;

  /* Spacing — 8px baseline */
  --sp-1:4px;--sp-2:8px;--sp-3:12px;--sp-4:16px;--sp-5:24px;--sp-6:32px;--sp-7:48px;--sp-8:64px;--sp-9:96px;

  /* Radius */
  --r-sm:8px;--r-md:12px;--r-lg:16px;--r-xl:24px;--r-full:9999px;

  /* Typography */
  --font-body:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
  --font-display:'Space Grotesk',Inter,sans-serif;
  --font-mono:'JetBrains Mono','Fira Code',monospace;

  /* Shadows */
  --shadow-sm:0 1px 2px rgba(0,0,0,0.3);
  --shadow-md:0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg:0 8px 32px rgba(0,0,0,0.5);
  --shadow-glow:0 0 24px var(--accent-glow);

  /* Transitions */
  --ease:cubic-bezier(0.4,0,0.2,1);
  --ease-spring:cubic-bezier(0.34,1.56,0.64,1);
  --dur:0.25s;
}

/* ═══ RESET ═══ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
*::selection{background:var(--accent-glow);color:var(--text-primary)}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  font-family:var(--font-body);
  background:var(--bg-base);
  color:var(--text-primary);
  font-size:16px;
  line-height:1.6;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  overflow-x:hidden;
  min-height:100vh;
}

/* Ambient background */
body::before{
  content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:
    radial-gradient(ellipse 900px 500px at 15% -5%,rgba(124,108,240,0.06),transparent 60%),
    radial-gradient(ellipse 700px 400px at 85% 100%,rgba(0,212,255,0.04),transparent 60%);
}

/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--gray-700);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--accent)}

/* ═══ TYPOGRAPHY ═══ */
h1,h2,h3,h4{font-family:var(--font-display);font-weight:700;letter-spacing:-0.02em;line-height:1.2}
h1{font-size:clamp(1.75rem,5vw,3rem)}
h2{font-size:clamp(1.25rem,3vw,1.75rem)}
h3{font-size:clamp(1rem,2vw,1.25rem)}
.eyebrow{font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.12em;color:var(--text-tertiary)}
.mono{font-family:var(--font-mono);font-size:0.85em}
.text-sm{font-size:0.85rem}
.text-xs{font-size:0.75rem}
.text-muted{color:var(--text-secondary)}
.text-faint{color:var(--text-tertiary)}

/* ═══ NAVIGATION ═══ */
.nav{
  position:sticky;top:0;z-index:200;
  background:rgba(10,10,18,0.8);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--glass-border);
  height:60px;display:flex;align-items:center;
  padding:0 var(--sp-5);gap:var(--sp-4);
}
.nav-brand{
  font-family:var(--font-display);
  font-size:1.1rem;font-weight:700;
  background:linear-gradient(135deg,var(--accent),var(--cyan));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  white-space:nowrap;letter-spacing:-0.03em;
}
.nav-tabs{display:flex;gap:2px;background:var(--bg-surface);border-radius:var(--r-full);padding:3px}
.nav-tab{
  padding:7px 18px;border-radius:var(--r-full);border:none;
  background:transparent;color:var(--text-secondary);cursor:pointer;
  font-family:inherit;font-size:0.82rem;font-weight:500;
  transition:all var(--dur) var(--ease);min-height:36px;
  display:flex;align-items:center;
}
.nav-tab:hover{color:var(--text-primary)}
.nav-tab.active{
  background:var(--accent);color:#fff;
  box-shadow:0 2px 12px var(--accent-glow);
}
.nav-search{flex:1;max-width:280px;position:relative;margin-left:auto}
.nav-search input{
  width:100%;height:38px;padding:0 14px 0 38px;
  border-radius:var(--r-full);border:1px solid var(--gray-700);
  background:var(--bg-surface);color:var(--text-primary);
  font-family:inherit;font-size:0.82rem;outline:none;
  transition:border-color var(--dur) var(--ease);
}
.nav-search input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow)}
.nav-search::before{
  content:'';position:absolute;left:14px;top:50%;transform:translateY(-50%);
  width:14px;height:14px;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' stroke='%235A5A78' stroke-width='2' viewBox='0 0 24 24'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cpath d='m21 21-4.3-4.3'/%3E%3C/svg%3E") center/contain no-repeat;
}

/* Mobile nav */
.nav-hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;color:var(--text-primary)}

/* ═══ LAYOUT ═══ */
.container{max-width:1100px;margin:0 auto;padding:0 var(--sp-5) var(--sp-8)}
.page{animation:pageIn 0.4s var(--ease) both}
@keyframes pageIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.hidden{display:none!important}

/* ═══ HERO ═══ */
.hero{text-align:center;padding:var(--sp-9) var(--sp-5) var(--sp-7)}
.hero-badge{
  display:inline-block;padding:6px 16px;border-radius:var(--r-full);
  background:linear-gradient(135deg,rgba(124,108,240,0.12),rgba(0,212,255,0.08));
  border:1px solid var(--glass-border);
  font-size:0.72rem;font-weight:600;color:var(--accent);
  letter-spacing:0.1em;text-transform:uppercase;margin-bottom:var(--sp-5);
}
.hero h1{
  margin-bottom:var(--sp-3);
  background:linear-gradient(135deg,var(--text-primary) 30%,var(--text-secondary));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero p{color:var(--text-secondary);max-width:560px;margin:0 auto;line-height:1.7;font-size:1.05rem}
.hero strong{color:var(--accent);font-weight:600}

/* ═══ STAT CARDS (Bento Grid) ═══ */
.bento{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(160px,1fr));
  gap:var(--sp-3);margin:var(--sp-7) 0;
}
.bento-card{
  background:var(--bg-surface);border:1px solid var(--glass-border);
  border-radius:var(--r-md);padding:var(--sp-5) var(--sp-4);
  text-align:center;position:relative;overflow:hidden;
  transition:transform var(--dur) var(--ease),border-color var(--dur) var(--ease);
}
.bento-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--accent),transparent);
  opacity:0;transition:opacity var(--dur) var(--ease);
}
.bento-card:hover{transform:translateY(-3px);border-color:var(--glass-border-hover)}
.bento-card:hover::before{opacity:1}
.bento-num{
  font-family:var(--font-display);font-size:2rem;font-weight:700;
  background:linear-gradient(135deg,var(--accent),var(--cyan));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.bento-label{font-size:0.68rem;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:0.08em;font-weight:600;margin-top:4px}

/* ═══ SECTION HEADER ═══ */
.sec-head{display:flex;align-items:center;gap:var(--sp-3);margin:var(--sp-8) 0 var(--sp-4)}
.sec-head h2{font-size:1.2rem}
.sec-head .line{flex:1;height:1px;background:linear-gradient(90deg,var(--glass-border),transparent)}
.sec-head .count{font-size:0.75rem;color:var(--text-tertiary);font-weight:500}

/* ═══ CHAPTER LIST ═══ */
.ch-list{display:flex;flex-direction:column;gap:var(--sp-2)}
.ch-card{
  background:var(--bg-surface);border:1px solid var(--glass-border);
  border-radius:var(--r-md);padding:var(--sp-4) var(--sp-5);
  display:flex;align-items:center;gap:var(--sp-4);cursor:pointer;
  transition:all var(--dur) var(--ease);position:relative;overflow:hidden;
  min-height:44px;
}
.ch-card::after{
  content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--accent),var(--cyan));
  transform:scaleY(0);transition:transform var(--dur) var(--ease);
}
.ch-card:hover{background:var(--bg-elevated);border-color:var(--glass-border-hover);transform:translateX(3px)}
.ch-card:hover::after{transform:scaleY(1)}
.ch-rank{font-family:var(--font-display);font-size:1.2rem;font-weight:700;color:var(--text-faint);min-width:32px;text-align:center;flex-shrink:0}
.ch-info{flex:1;min-width:0}
.ch-info h3{font-size:0.92rem;font-weight:600;color:var(--text-primary);margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ch-info .ch-meta{font-size:0.72rem;color:var(--text-tertiary)}

/* ═══ BADGES ═══ */
.badges{display:flex;gap:6px;flex-wrap:wrap;flex-shrink:0}
.badge{
  padding:3px 10px;border-radius:6px;font-size:0.68rem;font-weight:600;
  white-space:nowrap;display:inline-flex;align-items:center;gap:4px;
}
.b-accent{background:rgba(124,108,240,0.1);color:var(--accent)}
.b-cyan{background:rgba(0,212,255,0.08);color:var(--cyan)}
.b-success{background:rgba(45,212,168,0.08);color:var(--success)}
.b-danger{background:rgba(240,86,79,0.08);color:var(--danger)}
.b-warning{background:rgba(245,196,81,0.08);color:var(--warning)}
.b-neutral{background:var(--bg-elevated);color:var(--text-secondary)}
.b-up{background:rgba(45,212,168,0.08);color:var(--success)}
.b-down{background:rgba(240,86,79,0.08);color:var(--danger)}
.b-stable{background:rgba(245,196,81,0.08);color:var(--warning)}

/* ═══ FILTER PILLS ═══ */
.pills{display:flex;gap:var(--sp-2);flex-wrap:wrap;margin-bottom:var(--sp-4)}
.pill{
  padding:7px 16px;border-radius:var(--r-full);border:1px solid var(--gray-700);
  background:var(--bg-surface);color:var(--text-secondary);cursor:pointer;
  font-family:inherit;font-size:0.8rem;font-weight:500;min-height:36px;
  transition:all var(--dur) var(--ease);display:flex;align-items:center;
}
.pill:hover{border-color:var(--accent);color:var(--text-primary)}
.pill.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 2px 12px var(--accent-glow)}

/* ═══ DETAIL VIEW ═══ */
.back-btn{
  display:inline-flex;align-items:center;gap:6px;
  padding:8px 16px;border-radius:var(--r-sm);
  border:1px solid var(--gray-700);background:var(--bg-surface);
  color:var(--text-secondary);cursor:pointer;font-family:inherit;
  font-size:0.82rem;font-weight:500;margin-bottom:var(--sp-5);
  transition:all var(--dur) var(--ease);min-height:38px;
}
.back-btn:hover{border-color:var(--accent);color:var(--text-primary);background:var(--bg-elevated)}

.detail-hero{
  background:var(--bg-surface);border:1px solid var(--glass-border);
  border-radius:var(--r-lg);padding:var(--sp-6) var(--sp-7);
  margin-bottom:var(--sp-5);position:relative;overflow:hidden;
}
.detail-hero::before{
  content:'';position:absolute;top:-50%;right:-10%;width:300px;height:300px;
  background:radial-gradient(circle,var(--accent-glow),transparent 70%);opacity:0.15;
}
.detail-hero h2{font-size:1.6rem;margin-bottom:4px;position:relative}
.detail-hero .subj{font-size:0.82rem;color:var(--text-secondary);text-transform:capitalize;position:relative}
.detail-hero .badges{margin-top:var(--sp-3);position:relative}

/* Detail stats */
.dstats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:var(--sp-3);margin-bottom:var(--sp-5)}
.dstat{
  background:var(--bg-surface);border:1px solid var(--glass-border);
  border-radius:var(--r-sm);padding:var(--sp-4);text-align:center;
  transition:border-color var(--dur) var(--ease);
}
.dstat:hover{border-color:var(--glass-border-hover)}
.dstat .dv{font-family:var(--font-display);font-size:1.5rem;font-weight:700}
.dstat .dl{font-size:0.62rem;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:0.08em;margin-top:2px}

/* Chart */
.chart-box{
  background:var(--bg-surface);border:1px solid var(--glass-border);
  border-radius:var(--r-md);padding:var(--sp-5);margin-bottom:var(--sp-4);
}
.chart-box h3{font-size:0.92rem;margin-bottom:var(--sp-4)}

/* Bar chart */
.bars{display:flex;align-items:flex-end;gap:4px;height:120px;padding-top:var(--sp-4)}
.bar-w{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0}
.bar{
  width:100%;border-radius:4px 4px 0 0;min-height:4px;
  background:linear-gradient(180deg,var(--accent),rgba(124,108,240,0.2));
  transform:scaleY(0);transform-origin:bottom;
  animation:barUp 0.5s var(--ease) forwards;position:relative;cursor:pointer;
}
@keyframes barUp{to{transform:scaleY(1)}}
.bar:hover{filter:brightness(1.3)}
.bar-tip{
  position:absolute;top:-24px;left:50%;transform:translateX(-50%);
  font-size:0.65rem;font-weight:700;color:var(--text-primary);
  background:var(--bg-elevated);padding:2px 8px;border-radius:4px;
  border:1px solid var(--gray-700);opacity:0;transition:opacity 0.15s;white-space:nowrap;
}
.bar:hover .bar-tip{opacity:1}
.bar-l{font-size:0.6rem;color:var(--text-tertiary)}

/* Difficulty bars */
.diffs{display:flex;gap:var(--sp-4)}
.diff{flex:1;text-align:center}
.diff-bg{height:6px;border-radius:3px;background:var(--bg-elevated);overflow:hidden;margin-bottom:6px}
.diff-fill{height:100%;border-radius:3px;transform:scaleX(0);transform-origin:left;animation:diffGrow 0.6s var(--ease) forwards}
@keyframes diffGrow{to{transform:scaleX(1)}}
.diff-v{font-size:0.72rem;font-weight:600}
.diff-l{font-size:0.6rem;color:var(--text-tertiary)}

/* ═══ PATTERN CARDS ═══ */
.pat-card{
  background:var(--bg-surface);border:1px solid var(--glass-border);
  border-radius:var(--r-md);padding:var(--sp-4) var(--sp-5);
  margin-bottom:var(--sp-2);transition:border-color var(--dur) var(--ease);
}
.pat-card:hover{border-color:var(--glass-border-hover)}
.pat-head{display:flex;align-items:center;gap:var(--sp-2);margin-bottom:var(--sp-2);flex-wrap:wrap}
.freq{
  padding:3px 10px;border-radius:var(--r-sm);font-size:0.72rem;font-weight:700;
  background:linear-gradient(135deg,rgba(45,212,168,0.12),rgba(0,212,255,0.08));
  color:var(--success);border:1px solid rgba(45,212,168,0.15);
}
.pat-topic{font-weight:600;font-size:0.92rem;flex:1}
.pat-body{font-size:0.8rem;color:var(--text-secondary);margin:var(--sp-2) 0;line-height:1.6}
.pat-formula{
  background:rgba(124,108,240,0.04);border-left:3px solid var(--accent);
  padding:10px 14px;border-radius:0 var(--r-sm) var(--r-sm) 0;margin:var(--sp-2) 0;
  font-family:var(--font-mono);font-size:0.78rem;color:var(--cyan);
}
.pat-trap{
  background:rgba(240,86,79,0.04);border-left:3px solid var(--danger);
  padding:10px 14px;border-radius:0 var(--r-sm) var(--r-sm) 0;margin:var(--sp-2) 0;
  font-size:0.78rem;color:var(--text-secondary);
}
.pat-years{display:flex;gap:4px;flex-wrap:wrap;margin-top:var(--sp-2)}
.yr{padding:2px 8px;border-radius:4px;font-size:0.66rem;background:var(--bg-elevated);color:var(--text-secondary);font-weight:500}
.pat-q{
  background:rgba(0,0,0,0.25);border-radius:var(--r-sm);padding:var(--sp-3);
  margin:var(--sp-2) 0;font-size:0.78rem;color:var(--text-primary);
  max-height:160px;overflow-y:auto;white-space:pre-wrap;line-height:1.5;
}
.pat-ans{font-size:0.75rem;color:var(--success);font-weight:600;margin-top:var(--sp-1)}

/* ═══ QUESTION CARDS ═══ */
.q-card{
  background:var(--bg-surface);border:1px solid var(--gray-700);
  border-radius:var(--r-sm);padding:var(--sp-3) var(--sp-4);margin-bottom:6px;
  cursor:pointer;transition:all var(--dur) var(--ease);min-height:44px;
}
.q-card:hover{border-color:var(--accent);background:var(--bg-elevated)}
.q-meta{display:flex;gap:5px;align-items:center;flex-wrap:wrap;margin-bottom:var(--sp-2)}
.q-text{font-size:0.8rem;color:var(--text-primary);white-space:pre-wrap;max-height:70px;overflow:hidden;position:relative;line-height:1.5}
.q-text.expanded{max-height:none}
.q-text:not(.expanded)::after{content:'';position:absolute;bottom:0;left:0;right:0;height:24px;background:linear-gradient(transparent,var(--bg-surface))}
.q-expand{font-size:0.7rem;color:var(--accent);cursor:pointer;font-weight:600;margin-top:4px;display:inline-block}

/* ═══ MODAL ═══ */
.modal-bg{
  position:fixed;inset:0;background:rgba(4,4,8,0.75);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  z-index:300;display:none;align-items:center;justify-content:center;
  padding:var(--sp-4);animation:fadeIn 0.2s ease;
}
.modal-bg.show{display:flex}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.modal{
  background:var(--bg-surface);border:1px solid var(--glass-border);
  border-radius:var(--r-lg);max-width:580px;width:100%;
  max-height:85vh;overflow-y:auto;padding:var(--sp-6) var(--sp-7);
  position:relative;animation:modalIn 0.3s var(--ease-spring);
}
@keyframes modalIn{from{opacity:0;transform:scale(0.95) translateY(20px)}to{opacity:1;transform:scale(1) translateY(0)}}
.modal-x{
  position:absolute;top:var(--sp-4);right:var(--sp-4);
  width:32px;height:32px;border-radius:50%;border:1px solid var(--gray-700);
  background:var(--bg-elevated);color:var(--text-secondary);cursor:pointer;
  font-size:1.1rem;display:flex;align-items:center;justify-content:center;
  transition:all var(--dur) var(--ease);font-family:inherit;
}
.modal-x:hover{background:var(--danger);color:#fff;border-color:var(--danger)}
.modal h3{font-size:1.1rem;margin-bottom:6px}
.modal .m-badges{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:var(--sp-4)}
.modal .m-sec{margin-bottom:var(--sp-4)}
.modal .m-label{font-size:0.65rem;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:0.08em;font-weight:600;margin-bottom:4px}
.modal .m-text{font-size:0.84rem;color:var(--text-primary);line-height:1.6;white-space:pre-wrap}
.modal .m-formula{font-family:var(--font-mono);font-size:0.8rem;color:var(--cyan);background:rgba(124,108,240,0.04);padding:10px 14px;border-radius:var(--r-sm);border-left:3px solid var(--accent)}
.modal .m-years{display:flex;gap:5px;flex-wrap:wrap}

/* ═══ EMPTY STATE ═══ */
.empty{text-align:center;padding:var(--sp-7);color:var(--text-tertiary)}
.empty p{margin-top:var(--sp-2)}

/* ═══ RESPONSIVE ═══ */
@media(max-width:768px){
  .nav{padding:0 var(--sp-4);height:56px;gap:var(--sp-2)}
  .nav-tabs{display:none}
  .nav-hamburger{display:block}
  .nav-search{max-width:160px}
  .container{padding:0 var(--sp-4) var(--sp-6)}
  .hero{padding:var(--sp-7) var(--sp-3) var(--sp-5)}
  .bento{grid-template-columns:repeat(2,1fr)}
  .ch-card{flex-wrap:wrap;gap:var(--sp-2)}
  .dstats{grid-template-columns:repeat(2,1fr)}
  .bars{height:80px}
  .diffs{flex-direction:column;gap:var(--sp-2)}
  .modal{padding:var(--sp-5) var(--sp-5)}
}

/* Mobile nav drawer */
.nav-drawer{
  position:fixed;top:56px;left:0;right:0;
  background:var(--bg-surface);border-bottom:1px solid var(--glass-border);
  padding:var(--sp-3);z-index:150;
  transform:translateY(-100%);opacity:0;pointer-events:none;
  transition:all var(--dur) var(--ease);
}
.nav-drawer.open{transform:translateY(0);opacity:1;pointer-events:auto}
.nav-drawer .nav-tab{
  width:100%;text-align:center;padding:12px;margin-bottom:4px;
  border-radius:var(--r-sm);display:block;
}
.nav-drawer .nav-tab.active{background:var(--accent);color:#fff}

/* Reduced motion */
@media(prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important}
}
</style>
</head>
<body>
'''

HTML_BODY = '''
<!-- NAV -->
<nav class="nav">
  <div class="nav-brand">JEE Intelligence</div>
  <div class="nav-tabs">
    <button class="nav-tab active" onclick="go('home')">Home</button>
    <button class="nav-tab" onclick="go('physics')">Physics</button>
    <button class="nav-tab" onclick="go('chemistry')">Chemistry</button>
    <button class="nav-tab" onclick="go('mathematics')">Maths</button>
  </div>
  <div class="nav-search">
    <input type="text" placeholder="Search chapters, topics..." oninput="doSearch(this.value)" aria-label="Search">
  </div>
  <button class="nav-hamburger" onclick="toggleDrawer()" aria-label="Menu">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
</nav>
<div class="nav-drawer" id="drawer">
  <button class="nav-tab active" onclick="go('home');closeDrawer()">Home</button>
  <button class="nav-tab" onclick="go('physics');closeDrawer()">Physics</button>
  <button class="nav-tab" onclick="go('chemistry');closeDrawer()">Chemistry</button>
  <button class="nav-tab" onclick="go('mathematics');closeDrawer()">Maths</button>
</div>

<div class="container">
  <!-- HOME -->
  <div id="page-home" class="page">
    <div class="hero">
      <div class="hero-badge">AIR &lt; 200 · Top 5 IIT CSE</div>
      <h1>JEE Pattern Intelligence</h1>
      <p>Built from <strong>414 actual papers</strong>, <strong>10,051 questions</strong>, and <strong>1,118 repeating patterns</strong>. Your data-driven edge for the next 1.5 years.</p>
    </div>
    <div class="bento" id="home-stats"></div>
    <div class="sec-head">
      <h2>Top 10 ROI Chapters</h2>
      <div class="line"></div>
      <span class="count">across all subjects</span>
    </div>
    <div class="ch-list" id="home-top"></div>
  </div>

  <!-- SUBJECT -->
  <div id="page-subject" class="page hidden">
    <h2 id="subj-title" style="margin-bottom:var(--sp-4)"></h2>
    <div class="pills">
      <button class="pill active" onclick="sortCh('roi',this)">ROI Score</button>
      <button class="pill" onclick="sortCh('freq',this)">Most Frequent</button>
      <button class="pill" onclick="sortCh('easy',this)">Easiest First</button>
      <button class="pill" onclick="sortCh('trend',this)">Rising Trends</button>
    </div>
    <div class="ch-list" id="ch-list"></div>
  </div>

  <!-- DETAIL -->
  <div id="page-detail" class="page hidden">
    <button class="back-btn" onclick="back()">\u2190 Back to Chapters</button>
    <div id="detail-content"></div>
  </div>
</div>

<!-- MODAL -->
<div class="modal-bg" id="modal" onclick="closeModal(event)">
  <div class="modal" id="modal-c"></div>
</div>
'''

HTML_JS_START = '''
<script>
const D=JSON.parse(`'''

HTML_JS_END = '''`);

const SM={'phy':'Physics','che':'Chemistry','mat':'Mathematics'};
let curSubj='',curCh='',curSort='roi',searchQ='';
const esc=s=>s.replace(/'/g,"\\\\'").replace(/"/g,'&quot;');

// ===== ANIMATED COUNTERS =====
function animCount(el,target,dur=1200){
  const start=performance.now();
  function tick(now){
    const p=Math.min((now-start)/dur,1);
    const e=1-Math.pow(1-p,3);
    el.textContent=Math.floor(target*e).toLocaleString();
    if(p<1)requestAnimationFrame(tick);
    else el.textContent=target.toLocaleString();
  }
  requestAnimationFrame(tick);
}

// ===== NAV =====
function go(s){
  closeDrawer();
  if(s==='home'){showPage('home');setTab('Home');renderHome();}
  else{curSubj=s;showPage('subject');setTab(SM[s]);document.getElementById('subj-title').textContent=SM[s]+' — Chapter Rankings';renderCh();}
}
function setTab(name){
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.toggle('active',t.textContent===name));
}
function toggleDrawer(){document.getElementById('drawer').classList.toggle('open');}
function closeDrawer(){document.getElementById('drawer').classList.remove('open');}
function showPage(p){
  ['home','subject','detail'].forEach(x=>{
    const el=document.getElementById('page-'+x);
    el.classList.toggle('hidden',x!==p);
  });
  const el=document.getElementById('page-'+p);
  el.classList.remove('page');void el.offsetWidth;el.classList.add('page');
  window.scrollTo(0,0);
}
function back(){if(curSubj)go(curSubj);else go('home');}

// ===== HOME =====
function renderHome(){
  const stats=[
    {n:10051,l:'Questions Analyzed'},
    {n:414,l:'Papers Processed'},
    {n:1118,l:'Repeating Patterns'},
    {n:64,l:'Chapters Ranked'},
    {n:8,l:'Years (2019-26)'},
    {n:4225,l:'Classified Questions'},
  ];
  document.getElementById('home-stats').innerHTML=stats.map((s,i)=>
    `<div class="bento-card"><div class="bento-num" id="hc-${i}">0</div><div class="bento-label">${s.l}</div></div>`
  ).join('');
  stats.forEach((s,i)=>setTimeout(()=>animCount(document.getElementById('hc-'+i),s.n),i*80));
  renderHomeTop();
}
function renderHomeTop(){
  const top=[...D.chapters].sort((a,b)=>b.roi-a.roi).slice(0,10);
  document.getElementById('home-top').innerHTML=top.map((c,i)=>{
    const t=D.trends.find(t=>t.s===c.s&&t.c===c.c);
    const tb=t?`<span class="badge b-${t.td}">${t.td==='up'?'\\u2191 Rising':t.td==='down'?'\\u2193 Falling':'\\u2192 Stable'}</span>`:'';
    return `<div class="ch-card" onclick="go('${c.s}');setTimeout(()=>openCh('${c.s}','${esc(c.c)}'),150)">
      <div class="ch-rank">${i+1}</div>
      <div class="ch-info"><h3>${c.c}</h3><div class="ch-meta">${SM[c.s]} · ${c.t} Qs · ${c.st} topics</div></div>
      <div class="badges"><span class="badge b-accent">ROI ${c.roi}</span><span class="badge b-cyan">${c.r}% repeat</span>${c.e>15?`<span class="badge b-success">${c.e}% easy</span>`:''}${tb}</div>
    </div>`;
  }).join('');
}

// ===== SUBJECT =====
function sortCh(type,btn){
  curSort=type;document.querySelectorAll('.pill').forEach(p=>p.classList.remove('active'));btn.classList.add('active');renderCh();
}
function renderCh(){
  let ch=D.chapters.filter(c=>c.s===curSubj);
  if(searchQ){
    const q=searchQ.toLowerCase();
    ch=ch.filter(c=>c.c.toLowerCase().includes(q)||D.questions.some(qu=>qu.s===c.s&&qu.c===c.c&&qu.st&&qu.st.toLowerCase().includes(q)));
  }
  if(curSort==='roi')ch.sort((a,b)=>b.roi-a.roi);
  else if(curSort==='freq')ch.sort((a,b)=>b.t-a.t);
  else if(curSort==='easy')ch.sort((a,b)=>b.e-a.e);
  else if(curSort==='trend'){
    const ord={up:0,stable:1,down:2};
    ch.sort((a,b)=>{
      const ta=D.trends.find(t=>t.s===a.s&&t.c===a.c);
      const tb=D.trends.find(t=>t.s===b.s&&t.c===b.c);
      return(ord[ta?.td]||3)-(ord[tb?.td]||3)||b.roi-a.roi;
    });
  }
  document.getElementById('ch-list').innerHTML=ch.map((c,i)=>{
    const t=D.trends.find(t=>t.s===c.s&&t.c===c.c);
    const tb=t?`<span class="badge b-${t.td}">${t.td==='up'?'\\u2191':t.td==='down'?'\\u2193':'\\u2192'}</span>`:'';
    return `<div class="ch-card" onclick="openCh('${c.s}','${esc(c.c)}')">
      <div class="ch-rank">${i+1}</div>
      <div class="ch-info"><h3>${c.c}</h3><div class="ch-meta">${c.t} Qs · ${c.st} topics · ${c.r}% repeating</div></div>
      <div class="badges"><span class="badge b-accent">ROI ${c.roi}</span><span class="badge b-cyan">${c.r}%</span>${c.e>15?`<span class="badge b-success">${c.e}% easy</span>`:`<span class="badge b-danger">${c.e}% easy</span>`}${tb}</div>
    </div>`;
  }).join('');
}

// ===== CHAPTER DETAIL =====
function openCh(s,ch){
  curCh=ch;showPage('detail');
  const st=D.stats[s]?.[ch],rk=D.chapters.find(c=>c.s===s&&c.c===ch),tr=D.trends.find(t=>t.s===s&&t.c===ch);
  const pats=D.patterns.filter(p=>p.s===s&&p.c===ch).sort((a,b)=>b.f-a.f);
  const qs=D.questions.filter(q=>q.s===s&&q.c===ch).sort((a,b)=>(b.y||'').localeCompare(a.y||''));
  let h=`<div class="detail-hero"><h2>${ch}</h2><div class="subj">${SM[s]}</div><div class="badges">
    <span class="badge b-accent">ROI ${rk?.roi||'—'}</span><span class="badge b-cyan">${rk?.r||0}% repeating</span><span class="badge b-success">${rk?.e||0}% easy</span>
    ${tr?`<span class="badge b-${tr.td}">${tr.td==='up'?'\\u2191 Rising':tr.td==='down'?'\\u2193 Falling':'\\u2192 Stable'}</span>`:''}
  </div></div>`;
  if(st){
    h+=`<div class="dstats">
      <div class="dstat"><div class="dv" style="color:var(--accent)">${st.total_questions}</div><div class="dl">Total Qs</div></div>
      <div class="dstat"><div class="dv" style="color:var(--cyan)">${pats.length}</div><div class="dl">Patterns</div></div>
      <div class="dstat"><div class="dv" style="color:var(--success)">${st.by_difficulty?.Easy||0}</div><div class="dl">Easy</div></div>
      <div class="dstat"><div class="dv" style="color:var(--warning)">${st.by_difficulty?.Medium||0}</div><div class="dl">Medium</div></div>
      <div class="dstat"><div class="dv" style="color:var(--danger)">${st.by_difficulty?.Hard||0}</div><div class="dl">Hard</div></div>
    </div>`;
  }
  // Year chart
  if(st?.by_year){
    const yrs=Object.keys(st.by_year).sort(),mx=Math.max(...Object.values(st.by_year));
    h+=`<div class="chart-box"><h3>Year-wise Distribution</h3><div class="bars">`;
    yrs.forEach((y,i)=>{
      const v=st.by_year[y],h2=(v/mx*100);
      h+=`<div class="bar-w"><div class="bar" style="height:${h2}%;animation-delay:${i*50}ms"><span class="bar-tip">${v} Qs</span></div><div class="bar-l">${y}</div></div>`;
    });
    h+=`</div></div>`;
  }
  // Difficulty bars
  if(st?.by_difficulty){
    const tot=st.total_questions||1;
    const ds=[['Easy','var(--success)'],['Medium','var(--warning)'],['Hard','var(--danger)']];
    h+=`<div class="chart-box"><h3>Difficulty Distribution</h3><div class="diffs">`;
    ds.forEach(([d,c],i)=>{
      const v=st.by_difficulty[d]||0,pct=(v/tot*100).toFixed(1);
      h+=`<div class="diff"><div class="diff-bg"><div class="diff-fill" style="width:${pct}%;background:${c};animation-delay:${i*80}ms"></div></div><div class="diff-v" style="color:${c}">${v}</div><div class="diff-l">${d} (${pct}%)</div></div>`;
    });
    h+=`</div></div>`;
  }
  // Question types
  if(st?.by_question_type){
    h+=`<div class="chart-box"><h3>Question Types</h3><div style="display:flex;gap:6px;flex-wrap:wrap;">`;
    Object.entries(st.by_question_type).sort((a,b)=>b[1]-a[1]).forEach(([t,c])=>{h+=`<span class="badge b-neutral">${t}: ${c}</span>`;});
    h+=`</div></div>`;
  }
  // Patterns
  h+=`<div class="sec-head"><h2>Repeating Patterns</h2><div class="line"></div><span class="count">${pats.length} found</span></div>`;
  if(!pats.length){h+=`<div class="empty"><p>No repeating patterns found.</p></div>`;}
  else{
    pats.forEach(p=>{
      h+=`<div class="pat-card"><div class="pat-head"><span class="freq">\\u00d7${p.f}</span><span class="pat-topic">${p.st||'General'}</span><span class="badge b-neutral">${p.d}</span><span class="badge b-neutral">${p.qt}</span></div>`;
      if(p.cc)h+=`<div class="pat-body">${p.cc}</div>`;
      if(p.kf)h+=`<div class="pat-formula">${p.kf}</div>`;
      if(p.ct)h+=`<div class="pat-trap">\\u26A0 ${p.ct}</div>`;
      h+=`<div class="pat-years">${p.y.map(y=>`<span class="yr">${y}</span>`).join('')}</div>`;
      if(p.rq)h+=`<div class="pat-q">${p.rq}</div>`;
      if(p.ra)h+=`<div class="pat-ans">\\u2705 Answer: ${p.ra}</div>`;
      h+=`</div>`;
    });
  }
  // Questions
  h+=`<div class="sec-head"><h2>All Questions</h2><div class="line"></div><span class="count">${qs.length} total</span></div>`;
  qs.forEach((q,i)=>{
    h+=`<div class="q-card" onclick="showQ(${i},'${s}','${esc(ch)}')">
      <div class="q-meta"><span class="badge b-neutral">${q.y}</span><span class="badge b-neutral">${q.e}</span><span class="badge ${q.d==='Easy'?'b-success':q.d==='Hard'?'b-danger':'b-neutral'}">${q.d}</span>${q.st?`<span class="badge b-accent">${q.st}</span>`:''}${q.cs>1?`<span class="badge b-cyan">\\u00d7${q.cs}</span>`:''}</div>
      <div class="q-text" id="qt-${i}">${q.t}</div>
      ${q.t.length>180?`<span class="q-expand" onclick="toggleQ(${i});event.stopPropagation()">Show more</span>`:''}
    </div>`;
  });
  document.getElementById('detail-content').innerHTML=h;
}
function toggleQ(i){
  const el=document.getElementById('qt-'+i);
  el.classList.toggle('expanded');
  const btn=el.parentElement.querySelector('.q-expand');
  if(btn)btn.textContent=el.classList.contains('expanded')?'Show less':'Show more';
}

// ===== MODAL =====
function showQ(idx,s,ch){
  const qs=D.questions.filter(q=>q.s===s&&q.c===ch);
  const q=qs[idx];if(!q)return;
  const cy=q.cs>1?D.patterns.find(p=>p.id===q.ci)?.y||[]:[];
  let m=`<button class="modal-x" onclick="closeModal()">\\u00d7</button><h3>${q.st||'Question'}</h3>
  <div class="m-badges"><span class="badge b-neutral">${q.y}</span><span class="badge b-neutral">${q.e}</span><span class="badge ${q.d==='Easy'?'b-success':q.d==='Hard'?'b-danger':'b-neutral'}">${q.d}</span><span class="badge b-neutral">${q.qt}</span>${q.cs>1?`<span class="badge b-cyan">\\u00d7${q.cs} repeat</span>`:''}${q.nf?`<span class="badge b-danger">\\u1F4C8 Figure</span>`:''}</div>`;
  if(q.cs>1)m+=`<div class="m-sec"><div class="m-label">Repeats Across Years</div><div class="m-years">${cy.map(y=>`<span class="yr">${y}</span>`).join('')}</div></div>`;
  m+=`<div class="m-sec"><div class="m-label">Question</div><div class="m-text">${q.t}</div></div>`;
  if(q.a)m+=`<div class="m-sec"><div class="m-label">Answer</div><div class="m-text" style="color:var(--success);font-weight:600">\\u2705 ${q.a}</div></div>`;
  if(q.kf)m+=`<div class="m-sec"><div class="m-label">Key Formula</div><div class="m-formula">${q.kf}</div></div>`;
  if(q.cc)m+=`<div class="m-sec"><div class="m-label">Core Concept</div><div class="m-text" style="color:var(--text-secondary)">${q.cc}</div></div>`;
  if(q.ct)m+=`<div class="m-sec"><div class="m-label">\\u26A0 Common Trap</div><div class="m-text" style="color:var(--danger)">${q.ct}</div></div>`;
  document.getElementById('modal-c').innerHTML=m;
  document.getElementById('modal').classList.add('show');
}
function closeModal(e){
  if(e&&e.target!==document.getElementById('modal'))return;
  document.getElementById('modal').classList.remove('show');
}
function doSearch(v){
  searchQ=v;
  if(!document.getElementById('page-subject').classList.contains('hidden'))renderCh();
}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});

// INIT
renderHome();
</script>
</body>
</html>'''

# ═══════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════
output_path = f"{BASE}/JEE_Dashboard.html"

with open(output_path, "w") as f:
    f.write(HTML_HEAD)
    f.write(HTML_BODY)
    f.write(HTML_JS_START)
    f.write(embedded_json)
    f.write(HTML_JS_END)

size = os.path.getsize(output_path)
print(f"\nDashboard rebuilt: {output_path}")
print(f"Size: {size//1024} KB ({size/1024/1024:.1f} MB)")