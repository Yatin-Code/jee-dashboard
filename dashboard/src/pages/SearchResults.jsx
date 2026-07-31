import { fmt, esc, cap } from "../lib/helpers";
import { getData } from "../lib/data";
import ChapterList from "../components/ChapterList";
import PatternModal from "../components/PatternModal";
import { useState } from "react";

export default function SearchResults({ query, onNavigate }) {
  const [selectedPattern, setSelectedPattern] = useState(null);
  const data = getData();
  const q = query.toLowerCase().trim();

  if (!q || !data) return null;

  const chapterHits = (data.c || []).filter(
    (c) =>
      c.chapter.toLowerCase().includes(q) ||
      c.subject.toLowerCase().includes(q)
  );

  const patternHits = (data.p || []).filter(
    (p) =>
      (p.core_concept || "").toLowerCase().includes(q) ||
      (p.sub_topic || "").toLowerCase().includes(q) ||
      (p.chapter || "").toLowerCase().includes(q)
  );

  const total = chapterHits.length + patternHits.length;

  return (
    <div>
      <div className="flex items-center justify-between pb-6 border-b border-[#E2E8F0] mb-8">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
            Search
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[#0F172A] mt-1.5 tracking-tight">
            {fmt(total)} results
          </h1>
          <p className="text-sm text-[#475569] mt-1.5">
            for "{esc(query)}"
          </p>
        </div>
        <button
          onClick={() => onNavigate("home")}
          className="text-xs px-2.5 py-1 rounded bg-[#F1F5F9] text-[#475569] hover:text-[#0F172A]"
        >
          Clear
        </button>
      </div>

      {chapterHits.length > 0 && (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-[#0F172A]">Chapters</h2>
            <span className="text-xs text-[#94A3B8]">{chapterHits.length} matches</span>
          </div>
          <ChapterList chapters={chapterHits.slice(0, 15)} onNavigate={onNavigate} />
        </div>
      )}

      {patternHits.length > 0 && (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-[#0F172A]">Patterns</h2>
            <span className="text-xs text-[#94A3B8]">{patternHits.length} matches</span>
          </div>
          <div className="space-y-2">
            {patternHits.slice(0, 30).map((p, i) => (
              <button
                key={i}
                onClick={() => setSelectedPattern(p)}
                className="w-full text-left bg-white border border-[#E2E8F0] rounded-lg p-4 hover:border-[#CBD5E1] transition-colors"
              >
                <div className="flex items-center justify-between gap-3 mb-2 flex-wrap">
                  <div className="flex gap-1.5 flex-wrap">
                    <span className="text-xs font-medium px-2 py-0.5 rounded bg-[#EEF2FF] text-[#4F46E5]">
                      {cap(p.subject)}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded bg-[#F1F5F9] text-[#475569]">
                      {esc(p.sub_topic || p.chapter)}
                    </span>
                    {p.difficulty && (
                      <span
                        className={`text-xs font-medium px-2 py-0.5 rounded ${
                          p.difficulty === "Easy"
                            ? "bg-[#ECFDF5] text-[#059669]"
                            : p.difficulty === "Medium"
                            ? "bg-[#FEF3C7] text-[#D97706]"
                            : "bg-[#FEE2E2] text-[#DC2626]"
                        }`}
                      >
                        {p.difficulty}
                      </span>
                    )}
                  </div>
                  <span className="text-xs text-[#94A3B8] whitespace-nowrap">
                    <strong className="text-[#0F172A]">{p.frequency}</strong>×
                  </span>
                </div>
                <div className="text-sm font-medium text-[#0F172A]">
                  {esc(p.core_concept || "Pattern")}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {total === 0 && (
        <div className="text-center py-16 border border-dashed border-[#E2E8F0] rounded-lg">
          <h4 className="text-sm font-medium text-[#475569]">No results</h4>
          <p className="text-xs text-[#94A3B8] mt-1">Try a different keyword.</p>
        </div>
      )}

      {selectedPattern && (
        <PatternModal
          pattern={selectedPattern}
          onClose={() => setSelectedPattern(null)}
        />
      )}
    </div>
  );
}
