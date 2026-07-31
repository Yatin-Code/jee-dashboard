export function fmt(n) {
  if (n === undefined || n === null) return "—";
  return Number(n).toLocaleString("en-IN");
}

export function pct(n) {
  return (n * 100).toFixed(0) + "%";
}

export function cap(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
}

export function esc(s) {
  if (!s) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

export function getSubjects(data) {
  return ["physics", "chemistry", "mathematics"];
}

export function getChapters(data, subject) {
  return (data.c || []).filter(
    (c) => c.subject === subject
  );
}

export function getChapter(data, subject, name) {
  return (data.c || []).find(
    (c) => c.subject === subject && c.chapter === name
  );
}

export function getPatterns(data, subject, chapter) {
  return (data.p || []).filter(
    (p) => p.subject === subject && p.chapter === chapter
  );
}

export function getTrend(data, subject, chapter) {
  return (data.t || []).find(
    (t) => t.sc === `${subject}/${chapter}`
  );
}

export function getChapterStats(data, subject, chapter) {
  return data.s?.[subject]?.[chapter] || {};
}

export function sortChapters(chapters, by) {
  const arr = [...chapters];
  if (by === "roi") arr.sort((a, b) => b.roi_score - a.roi_score);
  else if (by === "total") arr.sort((a, b) => b.total - a.total);
  else if (by === "repeat")
    arr.sort((a, b) => b.repeat_ratio - a.repeat_ratio);
  else if (by === "easy")
    arr.sort((a, b) => b.easy_ratio - a.easy_ratio);
  return arr;
}
