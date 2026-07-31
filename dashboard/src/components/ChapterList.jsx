import { fmt, pct, cap, esc, sortChapters } from "../lib/helpers";
import { useState } from "react";

export default function ChapterList({ chapters, subject, onNavigate, max }) {
  const [sort, setSort] = useState("roi");
  const sorted = sortChapters(chapters, sort);
  const display = max ? sorted.slice(0, max) : sorted;

  if (!display.length) {
    return (
      <div className="text-center py-16 border border-dashed border-[#E2E8F0] rounded-lg">
        <h4 className="text-sm font-medium text-[#475569]">No chapters found</h4>
        <p className="text-sm text-[#94A3B8] mt-1">Try a different filter.</p>
      </div>
    );
  }

  const sorts = [
    { key: "roi", label: "ROI" },
    { key: "total", label: "Volume" },
    { key: "repeat", label: "Repeats" },
    { key: "easy", label: "Easy %" },
  ];

  return (
    <div>
      {!max && (
        <div className="flex items-center gap-1 bg-white border border-[#E2E8F0] rounded-md p-0.5 mb-4 w-fit">
          {sorts.map((s) => (
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
      )}

      <div className="bg-white border border-[#E2E8F0] rounded-lg overflow-hidden">
        {display.map((c, i) => (
          <button
            key={c.chapter}
            onClick={() => onNavigate("chapter", c.chapter)}
            className="w-full grid grid-cols-[28px_1fr_70px_70px_70px_24px] items-center gap-2 px-4 sm:px-5 py-3 border-t border-[#E2E8F0] first:border-t-0 hover:bg-[#F8FAFC] text-left transition-colors"
          >
            <span className="text-xs font-semibold text-[#94A3B8] tabular-nums">
              {String(i + 1).padStart(2, "0")}
            </span>
            <div className="min-w-0">
              <div className="text-sm font-medium text-[#0F172A] truncate">
                {esc(c.chapter)}
              </div>
              {!subject && (
                <div className="text-xs text-[#94A3B8] mt-0.5">
                  {cap(c.subject)} · {c.sub_topics} sub-topics
                </div>
              )}
            </div>
            <div className="text-xs text-right text-[#475569] tabular-nums hidden sm:block">
              {fmt(c.total)}
            </div>
            <div className="text-xs text-right tabular-nums hidden sm:block">
              <span className="font-medium text-[#0F172A]">{pct(c.repeat_ratio)}</span>
            </div>
            <div className="text-xs text-right tabular-nums">
              <span className="font-medium text-[#0F172A]">{c.roi_score.toFixed(1)}</span>
            </div>
            <svg
              className="w-3.5 h-3.5 text-[#94A3B8] justify-self-end"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        ))}
      </div>
    </div>
  );
}
