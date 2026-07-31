import { useState } from "react";
import { fmt, esc, cap } from "../lib/helpers";
import PatternModal from "../components/PatternModal";

export default function Patterns({ data }) {
  const [selectedPattern, setSelectedPattern] = useState(null);
  const [sort, setSort] = useState("freq");

  const all = (data.p || []).slice();
  if (sort === "freq") all.sort((a, b) => b.frequency - a.frequency);
  else if (sort === "recent") all.sort((a, b) => Math.max(...(b.years || [0])) - Math.max(...(a.years || [0])));
  else if (sort === "subject") all.sort((a, b) => a.subject.localeCompare(b.subject));

  const display = all.slice(0, 80);

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 pb-6 border-b border-[#E2E8F0] mb-8">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
            Patterns
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[#0F172A] mt-1.5 tracking-tight">
            {fmt(all.length)} repeating patterns
          </h1>
          <p className="text-sm text-[#475569] mt-1.5 max-w-lg">
            Question templates that appear in multiple years. Higher frequency = more likely to
            appear again.
          </p>
        </div>
      </div>

      {/* Sort */}
      <div className="flex items-center gap-1 bg-white border border-[#E2E8F0] rounded-md p-0.5 mb-6 w-fit">
        {[
          { key: "freq", label: "Frequency" },
          { key: "recent", label: "Most recent" },
          { key: "subject", label: "Subject" },
        ].map((s) => (
          <button
            key={s.key}
            onClick={() => setSort(s.key)}
            className={`px-3 py-1 text-sm font-medium rounded-[3px] transition-colors ${
              sort === s.key
                ? "bg-[#0F172A] text-white"
                : "text-[#475569] hover:text-[#0F172A]"
            }`}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* Pattern cards */}
      <div className="space-y-2">
        {display.map((p, i) => (
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
                {p.question_type && (
                  <span className="text-xs px-2 py-0.5 rounded bg-[#F1F5F9] text-[#475569]">
                    {esc(p.question_type)}
                  </span>
                )}
              </div>
              <span className="text-xs text-[#94A3B8] whitespace-nowrap">
                <strong className="text-[#0F172A]">{p.frequency}</strong>×
              </span>
            </div>
            <div className="text-sm font-medium text-[#0F172A] mb-2">
              {esc(p.core_concept || "Pattern")}
            </div>
            <div className="flex gap-1.5 flex-wrap">
              {(p.years || []).slice(0, 6).map((y) => (
                <span key={y} className="text-[11px] px-1.5 py-0.5 rounded bg-[#F8FAFC] text-[#94A3B8]">
                  {y}
                </span>
              ))}
              {(p.years || []).length > 6 && (
                <span className="text-[11px] text-[#94A3B8]">
                  +{p.years.length - 6} more
                </span>
              )}
            </div>
          </button>
        ))}
      </div>

      {all.length > 80 && (
        <p className="text-xs text-[#94A3B8] text-center mt-4">
          Showing 80 of {fmt(all.length)} patterns. Use search to find more.
        </p>
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
