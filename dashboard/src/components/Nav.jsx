import { useState } from "react";

const tabs = [
  { id: "home", label: "Overview" },
  { id: "physics", label: "Physics" },
  { id: "chemistry", label: "Chemistry" },
  { id: "mathematics", label: "Maths" },
  { id: "patterns", label: "Patterns" },
];

export default function Nav({ page, onNavigate, onSearch, searchQuery }) {
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-50 bg-white border-b border-[#E2E8F0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center gap-6">
          <button
            onClick={() => onNavigate("home")}
            className="flex items-center gap-2 shrink-0"
          >
            <span className="w-5.5 h-5.5 bg-[#4F46E5] rounded-md flex items-center justify-center text-white text-xs font-bold">
              J
            </span>
            <span className="font-semibold text-sm hidden sm:inline">
              JEE Intelligence
            </span>
          </button>

          <nav className="hidden md:flex items-center gap-1 flex-1">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => onNavigate(t.id)}
                className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                  t.id === page
                    ? "bg-[#F1F5F9] text-[#0F172A]"
                    : "text-[#475569] hover:text-[#0F172A] hover:bg-[#F1F5F9]"
                }`}
              >
                {t.label}
              </button>
            ))}
          </nav>

          <div className="relative flex-1 md:flex-none max-w-xs ml-auto">
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#94A3B8] pointer-events-none"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="search"
              value={searchQuery}
              onChange={(e) => onSearch(e.target.value)}
              placeholder="Search chapters, patterns…"
              className="w-full pl-9 pr-3 py-1.5 text-sm bg-[#F8FAFC] border border-[#E2E8F0] rounded-md focus:outline-none focus:border-[#4F46E5] focus:bg-white transition-colors"
            />
          </div>

          <button
            onClick={() => setDrawerOpen(true)}
            className="md:hidden p-2 text-[#475569] hover:text-[#0F172A]"
            aria-label="Menu"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
        </div>
      </header>

      {drawerOpen && (
        <div
          className="fixed inset-0 z-50 md:hidden"
          onClick={(e) => {
            if (e.target === e.currentTarget) setDrawerOpen(false);
          }}
        >
          <div className="absolute inset-0 bg-[#0F172A]/40" />
          <div className="absolute left-0 top-0 bottom-0 w-64 bg-white border-r border-[#E2E8F0] p-5">
            <div className="font-semibold text-sm mb-6">JEE Intelligence</div>
            <nav className="flex flex-col gap-1">
              {tabs.map((t) => (
                <button
                  key={t.id}
                  onClick={() => {
                    onNavigate(t.id);
                    setDrawerOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-sm rounded-md ${
                    t.id === page
                      ? "bg-[#F1F5F9] text-[#0F172A] font-medium"
                      : "text-[#475569] hover:bg-[#F1F5F9]"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </nav>
          </div>
        </div>
      )}
    </>
  );
}
