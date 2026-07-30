#!/usr/bin/env python3
"""
Merge all sub-agent classification results, apply to questions, mine patterns, build dashboard data.
"""
import json, os, glob
from collections import defaultdict, Counter

BASE = "/data/data/com.termux/files/home/jee-analysis"

# ====== 1. MERGE CLASSIFICATION RESULTS ======
print("=== MERGING CLASSIFICATIONS ===")
all_classifications = {}
batch_dir = f"{BASE}/raw_data/batches"

for i in range(32):
    path = f"{batch_dir}/result_{i:03d}.json"
    if not os.path.exists(path):
        print(f"  MISSING: result_{i:03d}.json")
        continue
    try:
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            for entry in data:
                cid = entry.get("cluster_id")
                if cid is not None:
                    all_classifications[cid] = entry
        elif isinstance(data, dict):
            # Some agents might return a dict with cluster_id keys
            for cid, entry in data.items():
                all_classifications[int(cid)] = entry
    except Exception as e:
        print(f"  ERROR reading result_{i:03d}.json: {e}")

print(f"  Total classifications merged: {len(all_classifications)}")

# ====== 2. LOAD CLUSTERS AND APPLY CLASSIFICATIONS ======
print("\n=== APPLYING CLASSIFICATIONS TO CLUSTERS ===")
with open(f"{BASE}/raw_data/clusters.json") as f:
    clusters_data = json.load(f)

clusters = clusters_data["clusters"]
print(f"  Total clusters: {len(clusters)}")
print(f"  Classifications available: {len(all_classifications)}")

classified_clusters = []
unclassified_count = 0

for c in clusters:
    cid = c["cluster_id"]
    cls = all_classifications.get(cid)
    
    if cls:
        c["chapter"] = cls.get("chapter", "Unknown")
        c["sub_topic"] = cls.get("sub_topic", "Unknown")
        c["difficulty"] = cls.get("difficulty", "Medium")
        c["core_concept"] = cls.get("core_concept", "")
        c["key_formula"] = cls.get("key_formula")
        c["common_trap"] = cls.get("common_trap")
        c["needs_figure"] = cls.get("needs_figure", False)
        c["question_type"] = cls.get("question_type", "MCQ")
    else:
        # Cluster wasn't in any batch (shouldn't happen for multi-clusters)
        unclassified_count += 1
        c["chapter"] = "Unclassified"
        c["sub_topic"] = "Unknown"
        c["difficulty"] = "Medium"
        c["core_concept"] = ""
        c["key_formula"] = None
        c["common_trap"] = None
        c["needs_figure"] = False
        c["question_type"] = "MCQ"
    
    classified_clusters.append(c)

print(f"  Classified: {len(classified_clusters) - unclassified_count}")
print(f"  Unclassified: {unclassified_count}")

# ====== 3. APPLY CLASSIFICATIONS TO ALL QUESTIONS ======
print("\n=== APPLYING TO ALL QUESTIONS ===")
with open(f"{BASE}/raw_data/questions_raw.json") as f:
    q_data = json.load(f)

questions = q_data["questions"]
print(f"  Total questions: {len(questions)}")

# Build cluster_id → classification map
cluster_class_map = {}
for c in classified_clusters:
    for member_idx in c["members"]:
        cluster_class_map[member_idx] = c

# Apply to each question
for i, q in enumerate(questions):
    c = cluster_class_map.get(i)
    if c:
        q["chapter"] = c["chapter"]
        q["sub_topic"] = c["sub_topic"]
        q["difficulty"] = c["difficulty"]
        q["core_concept"] = c["core_concept"]
        q["key_formula"] = c["key_formula"]
        q["common_trap"] = c["common_trap"]
        q["question_type"] = c["question_type"]
        q["cluster_size"] = c["size"]
        q["cluster_id"] = c["cluster_id"]
    else:
        q["chapter"] = "Unclassified"
        q["sub_topic"] = "Unknown"
        q["difficulty"] = "Medium"
        q["core_concept"] = ""
        q["key_formula"] = None
        q["common_trap"] = None
        q["question_type"] = "MCQ"
        q["cluster_size"] = 1
        q["cluster_id"] = -1

# Stats
chapter_counts = Counter(q["chapter"] for q in questions)
print(f"  Chapter distribution (top 20):")
for chap, count in chapter_counts.most_common(20):
    print(f"    {chap:40s} {count:5d}")

# ====== 4. MINE CROSS-YEAR PATTERNS ======
print("\n=== MINING CROSS-YEAR PATTERNS ===")

# Group clusters by chapter+sub_topic
pattern_groups = defaultdict(list)
for c in classified_clusters:
    if c["size"] >= 2 and c["chapter"] != "Unclassified":
        key = (c["subject"], c["chapter"], c["sub_topic"])
        pattern_groups[key].append(c)

# Merge clusters with same chapter+sub_topic
patterns = []
for (subject, chapter, sub_topic), cluster_list in pattern_groups.items():
    all_members = []
    all_years = set()
    all_exams = set()
    total_size = 0
    representative = None
    max_size = 0
    
    for c in cluster_list:
        all_members.extend(c["members"])
        all_years.update(c["years"])
        all_exams.update(c["exams"])
        total_size += c["size"]
        if c["size"] > max_size:
            max_size = c["size"]
            representative = c
    
    # Get sample questions
    sample_questions = []
    for c in cluster_list[:3]:
        rep = c["representative"]
        sample_questions.append({
            "text": rep["text"][:300],
            "year": rep.get("year"),
            "exam": rep.get("exam"),
            "answer": rep.get("answer"),
        })
    
    patterns.append({
        "subject": subject,
        "chapter": chapter,
        "sub_topic": sub_topic,
        "total_questions": total_size,
        "num_clusters": len(cluster_list),
        "years": sorted(all_years),
        "exams": sorted(all_exams),
        "frequency_score": total_size * len(all_years),
        "difficulty": representative.get("difficulty", "Medium") if representative else "Medium",
        "core_concept": representative.get("core_concept", "") if representative else "",
        "key_formula": representative.get("key_formula") if representative else None,
        "common_trap": representative.get("common_trap") if representative else None,
        "needs_figure": representative.get("needs_figure", False) if representative else False,
        "question_type": representative.get("question_type", "MCQ") if representative else "MCQ",
        "sample_questions": sample_questions,
    })

# Sort by frequency score (most important patterns first)
patterns.sort(key=lambda p: -p["frequency_score"])

print(f"  Total patterns mined: {len(patterns)}")
print(f"  Top 10 patterns:")
for p in patterns[:10]:
    print(f"    {p['subject']:12s} | {p['chapter']:30s} | {p['sub_topic']:30s} | Q={p['total_questions']:3d} | years={len(p['years'])} | score={p['frequency_score']}")

# ====== 5. BUILD CHAPTER SUMMARY STATS ======
print("\n=== BUILDING CHAPTER SUMMARIES ===")

chapter_stats = defaultdict(lambda: {
    "total_questions": 0,
    "years": set(),
    "exams": set(),
    "difficulties": Counter(),
    "question_types": Counter(),
    "sub_topics": set(),
    "patterns_count": 0,
})

for q in questions:
    key = (q["subject"], q["chapter"])
    chapter_stats[key]["total_questions"] += 1
    if q.get("year") and q["year"] != "unknown":
        chapter_stats[key]["years"].add(q["year"])
    if q.get("exam"):
        chapter_stats[key]["exams"].add(q["exam"])
    chapter_stats[key]["difficulties"][q.get("difficulty", "Medium")] += 1
    chapter_stats[key]["question_types"][q.get("question_type", "MCQ")] += 1
    if q.get("sub_topic"):
        chapter_stats[key]["sub_topics"].add(q["sub_topic"])

for p in patterns:
    key = (p["subject"], p["chapter"])
    chapter_stats[key]["patterns_count"] += 1

# Convert to list and sort
chapter_summary = []
for (subject, chapter), stats in chapter_stats.items():
    chapter_summary.append({
        "subject": subject,
        "chapter": chapter,
        "total_questions": stats["total_questions"],
        "years_covered": sorted(stats["years"]),
        "exams": sorted(stats["exams"]),
        "difficulty_dist": dict(stats["difficulties"]),
        "question_type_dist": dict(stats["question_types"]),
        "num_sub_topics": len(stats["sub_topics"]),
        "sub_topics": sorted(stats["sub_topics"]),
        "patterns_count": stats["patterns_count"],
    })

chapter_summary.sort(key=lambda x: -x["total_questions"])

print(f"  Total chapters: {len(chapter_summary)}")

# ====== 6. SAVE EVERYTHING ======
print("\n=== SAVING OUTPUT ===")

# Save classified questions
with open(f"{BASE}/raw_data/questions_classified.json", "w") as f:
    json.dump({
        "metadata": {
            "total_questions": len(questions),
            "classified": sum(1 for q in questions if q["chapter"] != "Unclassified"),
            "unclassified": sum(1 for q in questions if q["chapter"] == "Unclassified"),
        },
        "questions": questions,
    }, f, indent=2)
print("  Saved questions_classified.json")

# Save patterns
with open(f"{BASE}/raw_data/patterns.json", "w") as f:
    json.dump({
        "total_patterns": len(patterns),
        "patterns": patterns,
    }, f, indent=2)
print("  Saved patterns.json")

# Save chapter summary
with open(f"{BASE}/raw_data/chapter_summary.json", "w") as f:
    json.dump({
        "total_chapters": len(chapter_summary),
        "chapters": chapter_summary,
    }, f, indent=2)
print("  Saved chapter_summary.json")

# Save classified clusters
with open(f"{BASE}/raw_data/clusters_classified.json", "w") as f:
    json.dump({
        "metadata": clusters_data["metadata"],
        "clusters": classified_clusters,
    }, f, indent=2)
print("  Saved clusters_classified.json")

print("\n=== DONE ===")