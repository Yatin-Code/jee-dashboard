import { fmt } from "../lib/helpers";
import { TrendChart } from "../components/Charts";

export default function Home({ data, onNavigate }) {
  const m = data.m;
  const subjects = ["physics", "chemistry", "mathematics"];

  // Compute year-wise total for trend chart
  const yearTotals = {};
  (data.t || []).forEach((t) => {
    Object.entries(t.yc || {}).forEach(([y, n]) => {
      yearTotals[y] = (yearTotals[y] || 0) + n;
    });
  });
  const trendData = Object.entries(yearTotals)
    .sort(([a], [b]) => a - b)
    .map(([label, value]) => ({ label, value }));

  const subjectMeta = subjects.map((s) => ({
    name: s,
    chapters: (data.c || []).filter((c) => c.subject === s),
  }));

  const top10 = (data.c || []).slice().sort((a, b) => b.roi_score - a.roi_score).slice(0, 10);

  return (
    <div>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 pb-6 border-b border-[#E2E8F0] mb-8">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
            Overview
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[#0F172A] mt-1.5 tracking-tight">
            Strategic JEE Preparation
          </h1>
          <p className="text-sm text-[#475569] mt-1.5 max-w-lg">
            Patterns extracted from {fmt(m.total_papers)} JEE papers (2019–2026). Use this to
            prioritize what to study, not how much.
          </p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded bg-[#F1F5F9] text-[#475569] whitespace-nowrap">
          Updated {new Date().toLocaleDateString("en-IN", { month: "short", year: "numeric" })}
        </span>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-10">
        {[
          { label: "Papers analyzed", value: fmt(m.total_papers), sub: "2019 – 2026" },
          { label: "Questions extracted", value: fmt(m.total_questions), sub: `${fmt(m.total_classified)} classified` },
          { label: "Repeating patterns", value: fmt(m.total_patterns), sub: "Cross-year templates" },
          { label: "Chapters tracked", value: (data.c || []).length, sub: "Ranked by ROI" },
        ].map((s) => (
          <div key={s.label} className="bg-white border border-[#E2E8F0] rounded-lg p-4">
            <div className="text-xs font-medium text-[#475569]">{s.label}</div>
            <div className="text-xl sm:text-2xl font-semibold text-[#0F172A] mt-1 tracking-tight">
              {s.value}
            </div>
            <div className="text-xs text-[#94A3B8] mt-1">{s.sub}</div>
          </div>
        ))}
      </div>

      {/* Year Trend Chart */}
      {trendData.length > 0 && (
        <div className="bg-white border border-[#E2E8F0] rounded-lg p-5 mb-10">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-[#0F172A]">Question volume by year</h2>
            <span className="text-xs text-[#94A3B8]">
              {trendData[0]?.label} – {trendData[trendData.length - 1]?.label}
            </span>
          </div>
          <TrendChart data={trendData} height={180} />
        </div>
      )}

      {/* Subject cards */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-[#0F172A]">Choose your subject</h2>
          <span className="text-xs text-[#94A3B8]">Each ranked by ROI</span>
        </div>
        <div className="grid sm:grid-cols-3 gap-3">
          {subjectMeta.map((s) => {
            const top = s.chapters[0];
            return (
              <button
                key={s.name}
                onClick={() => onNavigate(s.name)}
                className="bg-white border border-[#E2E8F0] rounded-lg p-5 text-left hover:border-[#CBD5E1] transition-colors"
              >
                <h3 className="text-sm font-semibold text-[#0F172A] capitalize mb-3">
                  {s.name}
                </h3>
                <div className="text-xs text-[#475569] space-y-1">
                  <div>
                    <span className="font-medium text-[#0F172A]">{s.chapters.length}</span> chapters
                  </div>
                  <div>
                    Top: <span className="font-medium text-[#0F172A]">{top ? top.chapter : "—"}</span>
                  </div>
                  <div>
                    <span className="font-medium text-[#0F172A]">{top ? fmt(top.total) : "0"}</span> questions
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Top 10 chapters */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-[#0F172A]">Top 10 chapters by ROI</h2>
          <span className="text-xs text-[#94A3B8]">ROI = repeating × total / 100</span>
        </div>
        <div className="bg-white border border-[#E2E8F0] rounded-lg overflow-hidden">
          {top10.map((c, i) => (
            <button
              key={c.chapter}
              onClick={() => onNavigate("chapter", c.chapter)}
              className="w-full grid grid-cols-[28px_1fr_70px_70px_24px] items-center gap-2 px-4 sm:px-5 py-3 border-t border-[#E2E8F0] first:border-t-0 hover:bg-[#F8FAFC] text-left transition-colors"
            >
              <span className="text-xs font-semibold text-[#94A3B8] tabular-nums">
                {String(i + 1).padStart(2, "0")}
              </span>
              <div className="min-w-0">
                <div className="text-sm font-medium text-[#0F172A] truncate">{c.chapter}</div>
                <div className="text-xs text-[#94A3B8] mt-0.5 capitalize">{c.subject}</div>
              </div>
              <div className="text-xs text-right text-[#475569] tabular-nums">{fmt(c.total)}</div>
              <div className="text-xs text-right tabular-nums">
                <span className="font-medium text-[#0F172A]">{c.roi_score.toFixed(1)}</span>
              </div>
              <svg className="w-3.5 h-3.5 text-[#94A3B8] justify-self-end" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </button>
          ))}
        </div>
      </div>

      {/* How to use */}
      <div className="bg-white border border-[#E2E8F0] rounded-lg p-5 sm:p-6">
        <h2 className="text-sm font-semibold text-[#0F172A] mb-4">How to use this</h2>
        <div className="grid sm:grid-cols-3 gap-6">
          {[
            {
              title: "1. Identify high-ROI chapters",
              desc: "Start with chapters where the same pattern repeats year after year. The questions are essentially free.",
            },
            {
              title: "2. Practice repeating patterns",
              desc: "A pattern that has appeared in 4+ years will almost certainly appear again. Don't relearn — rehearse.",
            },
            {
              title: "3. Skip low-frequency chapters",
              desc: "Some chapters look important but yield only a few unique questions per year. Save them for last.",
            },
          ].map((item) => (
            <div key={item.title}>
              <h3 className="text-sm font-medium text-[#0F172A] mb-1.5">{item.title}</h3>
              <p className="text-xs text-[#475569] leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
