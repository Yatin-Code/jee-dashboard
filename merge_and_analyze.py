#!/usr/bin/env python3
"""
Merge all sub-agent classification results, apply to questions, mine patterns.
Output: final_data.json (used by HTML dashboard)
"""
import json, os
from collections import defaultdict, Counter

BASE = "/data/data/com.termux/files/home/jee-analysis"
BATCH_DIR = f"{BASE}/raw_data/batches"

# ====== 1. MERGE CLASSIFICATION RESULTS ======
all_classifications = {}
for i in range(32):
    path = f"{BATCH_DIR}/result_{i:03d}.json"
    if not os.path.exists(path):
        print(f"WARNING: {path} missing!")
        continue
    try:
        with open(path) as f:
            results = json.load(f)
        for entry in results:
            cid = entry.get("cluster_id")
            if cid is not None:
                all_classifications[cid] = entry
    except Exception as e:
        print(f"ERROR reading {path}: {e}")

print(f"Merged {len(all_classifications)} cluster classifications")

# ====== 2. LOAD CLUSTERS ======
with open(f"{BASE}/raw_data/clusters.json") as f:
    cluster_data = json.load(f)

clusters = cluster_data["clusters"]
print(f"Loaded {len(clusters)} clusters")

# ====== 3. LOAD RAW QUESTIONS ======
with open(f"{BASE}/raw_data/questions_raw.json") as f:
    q_data = json.load(f)

questions = q_data["questions"]
print(f"Loaded {len(questions)} questions")

# ====== 4. APPLY CLASSIFICATIONS TO QUESTIONS ======
classified_questions = []
unclassified_count = 0

for cluster in clusters:
    cid = cluster["cluster_id"]
    classification = all_classifications.get(cid)
    
    for q_idx in cluster["members"]:
        if q_idx < len(questions):
            q = questions[q_idx].copy()
            if classification:
                q["chapter"] = classification.get("chapter", "Unknown")
                q["sub_topic"] = classification.get("sub_topic", "Unknown")
                q["difficulty"] = classification.get("difficulty", "Medium")
                q["core_concept"] = classification.get("core_concept", "")
                q["key_formula"] = classification.get("key_formula")
                q["common_trap"] = classification.get("common_trap")
                q["needs_figure"] = classification.get("needs_figure", False)
                q["question_type"] = classification.get("question_type", "MCQ")
                q["cluster_id"] = cid
                q["cluster_size"] = cluster["size"]
                q["cluster_years"] = cluster["years"]
                q["cluster_exams"] = cluster["exams"]
            else:
                # Unclassified cluster — use subject as chapter
                q["chapter"] = "Unclassified"
                q["sub_topic"] = "Unknown"
                q["difficulty"] = "Medium"
                q["core_concept"] = ""
                q["key_formula"] = None
                q["common_trap"] = None
                q["needs_figure"] = False
                q["question_type"] = "MCQ"
                q["cluster_id"] = cid
                q["cluster_size"] = cluster["size"]
                q["cluster_years"] = cluster["years"]
                q["cluster_exams"] = cluster["exams"]
                unclassified_count += 1
            
            classified_questions.append(q)

print(f"Classified {len(classified_questions)} questions ({unclassified_count} unclassified)")

# ====== 5. COMPUTE CHAPTER STATISTICS ======
chapter_stats = defaultdict(lambda: {
    "total_questions": 0,
    "by_year": defaultdict(int),
    "by_difficulty": defaultdict(int),
    "by_exam": defaultdict(int),
    "by_question_type": defaultdict(int),
    "repeating_questions": 0,  # questions in clusters with size >= 2
    "unique_questions": 0,     # questions in singleton clusters
    "sub_topics": defaultdict(int),
    "needs_figure": 0,
})

subject_chapter_stats = {
    "physics": {},
    "chemistry": {},
    "mathematics": {},
}

for q in classified_questions:
    subject = q.get("subject", "unknown")
    chapter = q.get("chapter", "Unknown")
    
    stats = chapter_stats[f"{subject}|{chapter}"]
    stats["total_questions"] += 1
    year = q.get("year", "unknown")
    if year != "unknown":
        stats["by_year"][year] += 1
    stats["by_difficulty"][q.get("difficulty", "Medium")] += 1
    stats["by_exam"][q.get("exam", "unknown")] += 1
    stats["by_question_type"][q.get("question_type", "MCQ")] += 1
    
    if q.get("cluster_size", 1) >= 2:
        stats["repeating_questions"] += 1
    else:
        stats["unique_questions"] += 1
    
    sub_topic = q.get("sub_topic", "Unknown")
    stats["sub_topics"][sub_topic] += 1
    
    if q.get("needs_figure"):
        stats["needs_figure"] += 1

# Convert to serializable
for key, stats in chapter_stats.items():
    stats["by_year"] = dict(stats["by_year"])
    stats["by_difficulty"] = dict(stats["by_difficulty"])
    stats["by_exam"] = dict(stats["by_exam"])
    stats["by_question_type"] = dict(stats["by_question_type"])
    stats["sub_topics"] = dict(stats["sub_topics"])
    
    subject, chapter = key.split("|", 1)
    if subject not in subject_chapter_stats:
        subject_chapter_stats[subject] = {}
    subject_chapter_stats[subject][chapter] = stats

# ====== 6. COMPUTE REPEATING PATTERNS ======
patterns = []
for cluster in clusters:
    if cluster["size"] >= 2:
        cid = cluster["cluster_id"]
        classification = all_classifications.get(cid, {})
        pattern = {
            "cluster_id": cid,
            "subject": cluster["subject"],
            "chapter": classification.get("chapter", "Unknown"),
            "sub_topic": classification.get("sub_topic", "Unknown"),
            "difficulty": classification.get("difficulty", "Medium"),
            "core_concept": classification.get("core_concept", ""),
            "key_formula": classification.get("key_formula"),
            "common_trap": classification.get("common_trap"),
            "needs_figure": classification.get("needs_figure", False),
            "question_type": classification.get("question_type", "MCQ"),
            "frequency": cluster["size"],
            "years": cluster["years"],
            "exams": cluster["exams"],
            "representative_question": cluster["representative"].get("text", "")[:500],
            "representative_answer": cluster["representative"].get("answer"),
            "representative_year": cluster["representative"].get("year"),
            "representative_exam": cluster["representative"].get("exam"),
        }
        patterns.append(pattern)

# Sort by frequency (most repeated first)
patterns.sort(key=lambda p: -p["frequency"])

print(f"Found {len(patterns)} repeating patterns")

# ====== 7. COMPUTE YEAR-WISE TRENDS ======
year_trends = defaultdict(lambda: defaultdict(int))
for q in classified_questions:
    year = q.get("year", "unknown")
    if year == "unknown":
        continue
    subject = q.get("subject", "unknown")
    chapter = q.get("chapter", "Unknown")
    year_trends[f"{subject}|{chapter}"][year] += 1

# Convert to list for trend analysis
trend_data = []
for key, year_counts in year_trends.items():
    subject, chapter = key.split("|", 1)
    total = sum(year_counts.values())
    if total < 5:
        continue  # skip rare chapters
    years_sorted = sorted(year_counts.keys())
    trend_data.append({
        "subject": subject,
        "chapter": chapter,
        "total": total,
        "year_counts": {y: year_counts[y] for y in years_sorted},
        "trend": "up" if len(years_sorted) > 1 and year_counts[years_sorted[-1]] > year_counts[years_sorted[0]] * 1.2 else
                 "down" if len(years_sorted) > 1 and year_counts[years_sorted[0]] > year_counts[years_sorted[-1]] * 1.2 else
                 "stable",
    })

trend_data.sort(key=lambda t: -t["total"])

# ====== 8. BUILD CHAPTER RANKINGS (ROI) ======
# ROI = total_questions * (repeating_ratio) — chapters with more repeats are higher value
chapter_rankings = []
for key, stats in chapter_stats.items():
    subject, chapter = key.split("|", 1)
    if chapter == "Unclassified" or chapter == "Unknown":
        continue
    total = stats["total_questions"]
    if total < 5:
        continue
    repeating = stats["repeating_questions"]
    repeat_ratio = repeating / total if total > 0 else 0
    easy = stats["by_difficulty"].get("Easy", 0)
    easy_ratio = easy / total if total > 0 else 0
    
    # ROI score: high frequency + high repeat ratio + easy questions = high ROI
    roi_score = total * (0.5 + repeat_ratio * 0.3 + easy_ratio * 0.2)
    
    chapter_rankings.append({
        "subject": subject,
        "chapter": chapter,
        "total": total,
        "repeating": repeating,
        "repeat_ratio": round(repeat_ratio, 3),
        "easy_ratio": round(easy_ratio, 3),
        "roi_score": round(roi_score, 1),
        "needs_figure": stats["needs_figure"],
        "sub_topics": len(stats["sub_topics"]),
    })

chapter_rankings.sort(key=lambda r: -r["roi_score"])

# ====== 9. SAVE FINAL DATA ======
final_data = {
    "metadata": {
        "total_papers": 414,
        "total_questions": len(classified_questions),
        "total_classified": len(classified_questions) - unclassified_count,
        "unclassified": unclassified_count,
        "total_patterns": len(patterns),
        "total_chapters": len(chapter_rankings),
    },
    "chapter_stats": subject_chapter_stats,
    "chapter_rankings": chapter_rankings,
    "patterns": patterns,
    "trends": trend_data,
    "questions": classified_questions,
}

output_path = f"{BASE}/raw_data/final_data.json"
with open(output_path, "w") as f:
    json.dump(final_data, f, indent=2)

print(f"\n=== FINAL DATA ===")
print(f"Total questions: {len(classified_questions)}")
print(f"Classified: {len(classified_questions) - unclassified_count}")
print(f"Unclassified: {unclassified_count}")
print(f"Repeating patterns: {len(patterns)}")
print(f"Chapters ranked: {len(chapter_rankings)}")
print(f"\nTop 10 chapters by ROI:")
for r in chapter_rankings[:10]:
    print(f"  {r['subject']:12s} | {r['chapter']:35s} | total={r['total']:4d} | repeat={r['repeat_ratio']:.1%} | easy={r['easy_ratio']:.1%} | ROI={r['roi_score']}")
print(f"\nSaved to {output_path}")