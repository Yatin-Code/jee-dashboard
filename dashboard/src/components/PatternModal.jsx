import { esc, cap } from "../lib/helpers";

export default function PatternModal({ pattern, onClose }) {
  if (!pattern) return null;
  const p = pattern;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center p-4 sm:p-10 overflow-y-auto"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="absolute inset-0 bg-[#0F172A]/40" />
      <div className="relative bg-white border border-[#E2E8F0] rounded-xl w-full max-w-2xl mt-10 mb-16">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#E2E8F0]">
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8]">
              {cap(p.subject)} · {esc(p.sub_topic || p.chapter)}
            </div>
            <h3 className="text-base font-semibold text-[#0F172A] mt-1">
              {esc(p.core_concept)}
            </h3>
          </div>
          <button onClick={onClose} className="p-1 text-[#94A3B8] hover:text-[#0F172A]">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-5 space-y-6">
          {/* Tags */}
          <div className="flex flex-wrap gap-2">
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
              <span className="text-xs font-medium px-2 py-0.5 rounded bg-[#F1F5F9] text-[#475569]">
                {p.question_type}
              </span>
            )}
            <span className="text-xs font-medium px-2 py-0.5 rounded bg-[#EEF2FF] text-[#4F46E5]">
              {p.frequency}× occurrences
            </span>
            {(p.years || []).slice(0, 5).map((y) => (
              <span key={y} className="text-xs px-2 py-0.5 rounded bg-[#F1F5F9] text-[#475569]">
                {y}
              </span>
            ))}
          </div>

          {/* Question */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8] mb-2">
              Representative question
            </h4>
            <p className="text-sm leading-relaxed text-[#0F172A]">
              {esc(p.representative_question || "—")}
            </p>
          </div>

          {/* Answer */}
          {p.representative_answer && (
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8] mb-2">
                Answer
              </h4>
              <div className="text-sm pl-3 border-l-2 border-[#4F46E5] text-[#475569]">
                {esc(p.representative_answer)}
              </div>
            </div>
          )}

          {/* Key formula */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8] mb-2">
              Key formula
            </h4>
            <div className="text-sm font-mono bg-[#F8FAFC] px-3 py-2 rounded-md text-[#0F172A]">
              {esc(p.key_formula || "—")}
            </div>
          </div>

          {/* Common trap */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8] mb-2">
              Common trap
            </h4>
            <p className="text-sm text-[#475569] leading-relaxed">
              {esc(p.common_trap || "—")}
            </p>
          </div>

          {/* All years */}
          {(p.years || []).length > 5 && (
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8] mb-2">
                All years
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {(p.years || []).map((y) => (
                  <span key={y} className="text-xs px-2 py-0.5 rounded bg-[#F1F5F9] text-[#475569]">
                    {y}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
