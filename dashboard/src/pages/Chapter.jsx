import { useState } from "react";
import { fmt, pct, cap, esc, getChapter, getChapterStats, getTrend, getPatterns } from "../lib/helpers";
import { BarRow } from "../components/Charts";
import PatternModal from "../components/PatternModal";

export default function Chapter({ data, subject, chapter, onNavigate }) {
  const [selectedPattern, setSelectedPattern] = useState(null);

  const ch = getChapter(data, subject, chapter);

  if (!ch) {
    return (
      <div className="text-center py-16 border border-dashed border-[#E2E8F0] rounded-lg">
        <h4 className="text-sm font-medium text-[#475569]">Chapter not found</h4>
        <p className="text-sm text-[#94A3B8] mt-1">"{esc(chapter)}" was not found.</p>
      </div>
    );
  }

  const stats = getChapterStats(data, subject, ch.chapter);
  const trend = getTrend(data, subject, ch.chapter);
  const patterns = getPatterns(data, subject, ch.chapter).sort((a, b) => b.frequency - a.frequency);

  const yearEntries = trend ? Object.entries(trend.yc || {}).sort(([a], [b]) => a - b) : [];
  const maxYear = Math.max(...yearEntries.map(([_, n]) => n), 1);

  const diffDist = stats.by_difficulty || {};
  const totalDiff = Object.values(diffDist).reduce((a, b) => a + b, 0) || 1;

  const typeDist = stats.by_question_type || {};
  const maxType = Math.max(...Object.values(typeDist), 1);

  const diffColors = { Easy: "#059669", Medium: "#D97706", Hard: "#DC2626" };

  return (
    <div>
      <button onClick={() => onNavigate(subject)} className="inline-flex items-center gap-1 text-sm text-[#475569] hover:text-[#0F172A] mb-4">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="15 18 9 12 15 6" />
        </svg>
        {cap(subject)}
      </button>

      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 pb-6 border-b border-[#E2E8F0] mb-8">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">{cap(subject)} chapter</div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[#0F172A] mt-1.5 tracking-tight">{esc(ch.chapter)}</h1>
          <p className="text-sm text-[#475569] mt-1.5">
            {fmt(ch.total)} questions across {yearEntries.length} years.
            {ch.repeat_ratio > 0.7 ? " High repeat rate — patterns reliably resurface." : ""}
          </p>
        </div>
        <div className="flex gap-2">
          <span className="text-xs font-medium px-2.5 py-1 rounded bg-[#EEF2FF] text-[#4F46E5]">ROI {ch.roi_score.toFixed(1)}</span>
          <span className="text-xs px-2.5 py-1 rounded bg-[#F1F5F9] text-[#475569]">{pct(ch.repeat_ratio)} repeat</span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        {[
          { k: "Total", v: fmt(ch.total) },
          { k: "Repeating", v: fmt(ch.repeating), sub: pct(ch.repeat_ratio) },
          { k: "Easy", v: pct(ch.easy_ratio), sub: `${fmt(diffDist.Easy || 0)} easy` },
          { k: "Sub-topics", v: ch.sub_topics },
        ].map((s) => (
          <div key={s.k} className="bg-white border border-[#E2E8F0] rounded-lg p-4">
            <div className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">{s.k}</div>
            <div className="text-lg sm:text-xl font-semibold text-[#0F172A] mt-1">{s.v}</div>
            {s.sub && <div className="text-xs text-[#94A3B8] mt-0.5">{s.sub}</div>}
          </div>
        ))}
      </div>

      {yearEntries.length > 0 && (
        <div className="bg-white border border-[#E2E8F0] rounded-lg p-5 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-[#0F172A]">Yearly volume</h3>
            <span className="text-xs text-[#94A3B8]">{yearEntries[0]?.[0]} – {yearEntries[yearEntries.length - 1]?.[0]}</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {yearEntries.map(([y, n]) => (
              <div key={y} className="text-center">
                <div className="text-xs text-[#475569] mb-1">{y}</div>
                <div className="flex items-end justify-center gap-1">
                  <div className="w-full max-w-[40px] bg-[#4F46E5] rounded-t" style={{ height: `${Math.max((n / maxYear) * 80, 4)}px`, opacity: 0.3 + 0.7 * (n / maxYear) }} />
                </div>
                <div className="text-xs font-medium text-[#0F172A] mt-1 tabular-nums">{fmt(n)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid sm:grid-cols-2 gap-4 mb-6">
        {Object.keys(diffDist).length > 0 && (
          <div className="bg-white border border-[#E2E8F0] rounded-lg p-5">
            <h3 className="text-sm font-semibold text-[#0F172A] mb-3">Difficulty</h3>
            {Object.entries(diffDist).map(([k, v]) => (
              <BarRow key={k} label={k} value={v} max={totalDiff} color={diffColors[k] || "#4F46E5"} right={pct(v / totalDiff)} />
            ))}
          </div>
        )}
        {Object.keys(typeDist).length > 0 && (
          <div className="bg-white border border-[#E2E8F0] rounded-lg p-5">
            <h3 className="text-sm font-semibold text-[#0F172A] mb-3">Question types</h3>
            {Object.entries(typeDist).map(([k, v]) => (
              <BarRow key={k} label={k} value={v} max={maxType} right={fmt(v)} />
            ))}
          </div>
        )}
      </div>

      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-[#0F172A]">Repeating patterns</h3>
          <span className="text-xs text-[#94A3B8]">{patterns.length} patterns</span>
        </div>

        {patterns.length === 0 ? (
          <div className="text-center py-16 border border-dashed border-[#E2E8F0] rounded-lg">
            <h4 className="text-sm font-medium text-[#475569]">No patterns catalogued yet</h4>
            <p className="text-xs text-[#94A3B8] mt-1">Patterns emerge when 3+ similar questions appear across years.</p>
          </div>
        ) : (
          <div className="space-y-2">
            {patterns.slice(0, 40).map((p, i) => (
              <button key={i} onClick={() => setSelectedPattern(p)} className="w-full text-left bg-white border border-[#E2E8F0] rounded-lg p-4 hover:border-[#CBD5E1] transition-colors">
                <div className="flex items-center justify-between gap-3 mb-2 flex-wrap">
                  <div className="flex gap-1.5 flex-wrap">
                    <span className="text-xs font-medium px-2 py-0.5 rounded bg-[#EEF2FF] text-[#4F46E5]">{cap(p.subject || subject)}</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-[#F1F5F9] text-[#475569]">{esc(p.sub_topic || p.chapter)}</span>
                    {p.difficulty && (
                      <span className={`text-xs font-medium px-2 py-0.5 rounded ${p.difficulty === "Easy" ? "bg-[#ECFDF5] text-[#059669]" : p.difficulty === "Medium" ? "bg-[#FEF3C7] text-[#D97706]" : "bg-[#FEE2E2] text-[#DC2626]"}`}>{p.difficulty}</span>
                    )}
                  </div>
                  <span className="text-xs text-[#94A3B8]"><strong className="text-[#0F172A]">{p.frequency}</strong>×</span>
                </div>
                <div className="text-sm font-medium text-[#0F172A]">{esc(p.core_concept || "Pattern")}</div>
              </button>
            ))}
            {patterns.length > 40 && <p className="text-xs text-[#94A3B8] text-center mt-3">Showing 40 of {fmt(patterns.length)} patterns.</p>}
          </div>
        )}
      </div>

      {selectedPattern && <PatternModal pattern={selectedPattern} onClose={() => setSelectedPattern(null)} />}
    </div>
  );
}
