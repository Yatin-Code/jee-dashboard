import { fmt, cap, getChapters, getTrend } from "../lib/helpers";
import { TrendChart } from "../components/Charts";
import ChapterList from "../components/ChapterList";

export default function Subject({ data, subject, onNavigate }) {
  const chapters = getChapters(data, subject);
  const totalQs = chapters.reduce((a, c) => a + c.total, 0);

  // Per-subject trend
  const trendMap = {};
  chapters.forEach((c) => {
    const t = getTrend(data, subject, c.chapter);
    if (t) {
      Object.entries(t.yc || {}).forEach(([y, n]) => {
        trendMap[y] = (trendMap[y] || 0) + n;
      });
    }
  });
  const trendData = Object.entries(trendMap)
    .sort(([a], [b]) => a - b)
    .map(([label, value]) => ({ label, value }));

  return (
    <div>
      <button
        onClick={() => onNavigate("home")}
        className="inline-flex items-center gap-1 text-sm text-[#475569] hover:text-[#0F172A] mb-4"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="15 18 9 12 15 6" />
        </svg>
        Overview
      </button>

      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 pb-6 border-b border-[#E2E8F0] mb-8">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
            {cap(subject)}
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[#0F172A] mt-1.5 tracking-tight">
            {chapters.length} chapters
          </h1>
          <p className="text-sm text-[#475569] mt-1.5">
            {fmt(totalQs)} questions across {chapters.filter((c) => c.total > 0).length} active
            chapters.
          </p>
        </div>
      </div>

      {/* Trend chart */}
      {trendData.length > 1 && (
        <div className="bg-white border border-[#E2E8F0] rounded-lg p-5 mb-8">
          <div className="text-sm font-semibold text-[#0F172A] mb-4">
            {cap(subject)} question volume by year
          </div>
          <TrendChart data={trendData} height={160} />
        </div>
      )}

      <ChapterList chapters={chapters} subject={subject} onNavigate={onNavigate} />
    </div>
  );
}
