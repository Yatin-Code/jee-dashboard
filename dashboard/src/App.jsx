import { useState, useEffect } from "react";
import { loadData, getData } from "./lib/data";
import Nav from "./components/Nav";
import Home from "./pages/Home";
import Subject from "./pages/Subject";
import Chapter from "./pages/Chapter";
import Patterns from "./pages/Patterns";
import SearchResults from "./pages/SearchResults";

function getPage() {
  const path = window.location.pathname;
  if (path.includes("physics")) return "physics";
  if (path.includes("chemistry")) return "chemistry";
  if (path.includes("mathematics")) return "mathematics";
  if (path.includes("patterns")) return "patterns";
  if (path.includes("chapter")) return "chapter";
  return "home";
}

export default function App() {
  const [ready, setReady] = useState(false);
  const [page, setPage] = useState(getPage);
  const [chapter, setChapter] = useState(null);
  const [query, setQuery] = useState("");
  const [searchActive, setSearchActive] = useState(false);

  useEffect(() => {
    loadData().then(() => setReady(true));
  }, []);

  const navigate = (p, ch = null) => {
    setPage(p);
    setChapter(ch);
    setSearchActive(false);
    setQuery("");
    window.scrollTo(0, 0);
  };

  const handleSearch = (q) => {
    setQuery(q);
    setSearchActive(q.length > 0);
  };

  if (!ready) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F8FAFC]">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-[#4F46E5] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-sm text-[#475569]">Loading JEE data...</p>
        </div>
      </div>
    );
  }

  const data = getData();

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Nav
        page={page}
        onNavigate={navigate}
        onSearch={handleSearch}
        searchQuery={query}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 pb-16">
        {searchActive ? (
          <SearchResults query={query} onNavigate={navigate} />
        ) : page === "home" ? (
          <Home data={data} onNavigate={navigate} />
        ) : page === "patterns" ? (
          <Patterns data={data} />
        ) : page === "chapter" ? (
          <Chapter data={data} chapter={chapter} onNavigate={navigate} />
        ) : (
          <Subject data={data} subject={page} onNavigate={navigate} />
        )}
      </main>
    </div>
  );
}
