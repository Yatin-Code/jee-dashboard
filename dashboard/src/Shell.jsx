import { useState, useEffect, useCallback } from "react";
import { Routes, Route, useNavigate, useParams } from "react-router-dom";
import { loadData, getData } from "./lib/data";
import Nav from "./components/Nav";
import Home from "./pages/Home";
import Subject from "./pages/Subject";
import ChapterPage from "./pages/Chapter";
import Patterns from "./pages/Patterns";
import SearchResults from "./pages/SearchResults";

function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F8FAFC]">
      <div className="text-center">
        <div className="w-8 h-8 border-2 border-[#4F46E5] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm text-[#475569]">Loading JEE data...</p>
      </div>
    </div>
  );
}

function HomePage({ onNavigate }) {
  const data = getData();
  if (!data) return <Loading />;
  return <Home data={data} onNavigate={onNavigate} />;
}

function SubjectRoute({ onNavigate }) {
  const { subject } = useParams();
  const data = getData();
  if (!data) return <Loading />;
  if (!["physics", "chemistry", "mathematics"].includes(subject)) {
    return <div className="text-center py-16 text-sm text-[#475569]">Subject not found</div>;
  }
  return <Subject data={data} subject={subject} onNavigate={onNavigate} />;
}

function ChapterRoute({ onNavigate }) {
  const { subject, chapter } = useParams();
  const data = getData();
  if (!data) return <Loading />;
  return <ChapterPage data={data} subject={subject} chapter={decodeURIComponent(chapter)} onNavigate={onNavigate} />;
}

function PatternsPage() {
  const data = getData();
  if (!data) return <Loading />;
  return <Patterns data={data} />;
}

function SearchRoute({ onNavigate }) {
  const { query } = useParams();
  return <SearchResults query={query} onNavigate={onNavigate} />;
}

export default function Shell() {
  const [ready, setReady] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    loadData().then(() => setReady(true));
  }, []);

  const handleSearch = useCallback((q) => {
    setSearchQuery(q);
    if (q.trim()) {
      navigate(`/search/${encodeURIComponent(q.trim())}`);
    }
  }, [navigate]);

  const handleNavigate = useCallback((page, chapter) => {
    if (page === "home") navigate("/");
    else if (page === "patterns") navigate("/patterns");
    else if (page === "chapter") {
      // We need subject context — find it client side
      const data = getData();
      if (data) {
        for (const s of ["physics", "chemistry", "mathematics"]) {
          const ch = (data.c || []).find((c) => c.subject === s && c.chapter === chapter);
          if (ch) {
            navigate(`/${s}/${encodeURIComponent(chapter)}`);
            return;
          }
        }
      }
      navigate("/");
    } else {
      navigate(`/${page}`);
    }
    window.scrollTo(0, 0);
  }, [navigate]);

  if (!ready) return <Loading />;

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Nav
        page={window.location.pathname.split("/")[1] || "home"}
        onNavigate={handleNavigate}
        onSearch={handleSearch}
        searchQuery={searchQuery}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 pb-16">
        <Routes>
          <Route path="/" element={<HomePage onNavigate={handleNavigate} />} />
          <Route path="/physics" element={<SubjectRoute onNavigate={handleNavigate} />} />
          <Route path="/chemistry" element={<SubjectRoute onNavigate={handleNavigate} />} />
          <Route path="/mathematics" element={<SubjectRoute onNavigate={handleNavigate} />} />
          <Route path="/patterns" element={<PatternsPage />} />
          <Route path="/:subject/:chapter" element={<ChapterRoute onNavigate={handleNavigate} />} />
          <Route path="/search/:query" element={<SearchRoute onNavigate={handleNavigate} />} />
          <Route path="*" element={<div className="text-center py-16 text-sm text-[#475569]">Page not found</div>} />
        </Routes>
      </main>
    </div>
  );
}
