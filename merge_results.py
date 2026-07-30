#!/usr/bin/env python3
"""
Merge all sub-agent classification results, apply to clusters, 
and build the final classified dataset for the dashboard.
"""
import json, os, glob
from collections import defaultdict, Counter

BASE = "/data/data/com.termux/files/home/jee-analysis"

# ====== STEP 1: Load and merge all result files ======
print("=== MERGING CLASSIFICATION RESULTS ===")

all_classifications = {}
batch_dir = f"{BASE}/raw_data/batches"

for i in range(32):
    fpath = f"{batch_dir}/result_{i:03d}.json"
    if not os.path.exists(fpath):
        print(f"  MISSING: result_{i:03d}.json")
        continue
    
    with open(fpath) as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ERROR parsing result_{i:03d}.json: {e}")
            # Try to fix common JSON issues
            with open(fpath) as f2:
                content = f2.read()
            # Try removing trailing commas
            content = content.replace(",]", "]").replace(",}", "}")
            try:
                results = json.loads(content)
            except:
                print(f"  FAILED to fix result_{i:03d}.json, skipping")
                continue
    
    if isinstance(results, list):
        for entry in results:
            cid = entry.get("cluster_id")
            if cid is not None:
                all_classifications[cid] = entry
        print(f"  result_{i:03d}.json: {len(results)} entries")
    elif isinstance(results, dict):
        # Some agents might return a dict
        for cid, entry in results.items():
            all_classifications[int(cid)] = entry
        print(f"  result_{i:03d}.json: {len(results)} entries (dict format)")

print(f"\nTotal unique classifications: {len(all_classifications)}")

# ====== STEP 2: Load clusters and apply classifications ======
print("\n=== APPLYING CLASSIFICATIONS TO CLUSTERS ===")

with open(f"{BASE}/raw_data/clusters.json") as f:
    cluster_data = json.load(f)

clusters = cluster_data["clusters"]
questions_meta = json.load(open(f"{BASE}/raw_data/questions_raw.json"))
all_questions = questions_meta["questions"]

classified_clusters = []
unclassified_count = 0

for c in clusters:
    cid = c["cluster_id"]
    classification = all_classifications.get(cid)
    
    if classification:
        c["classification"] = {
            "chapter": classification.get("chapter", "Unknown"),
            "sub_topic": classification.get("sub_topic", "Unknown"),
            "difficulty": classification.get("difficulty", "Unknown"),
            "core_concept": classification.get("core_concept", ""),
            "key_formula": classification.get("key_formula"),
            "common_trap": classification.get("common_trap"),
            "needs_figure": classification.get("needs_figure", False),
            "question_type": classification.get("question_type", "Other"),
        }
    else:
        unclassified_count += 1
        c["classification"] = {
            "chapter": "Unclassified",
            "sub_topic": "Unknown",
            "difficulty": "Unknown",
            "core_concept": "",
            "key_formula": None,
            "common_trap": None,
            "needs_figure": False,
            "question_type": "Other",
        }
    
    classified_clusters.append(c)

print(f"Classified: {len(all_classifications)} clusters")
print(f"Unclassified: {unclassified_count} clusters")

# ====== STEP 3: Build chapter statistics ======
print("\n=== BUILDING CHAPTER STATISTICS ===")

chapter_stats = defaultdict(lambda: {
    "total_questions": 0,
    "total_clusters": 0,
    "multi_clusters": 0,
    "by_year": defaultdict(int),
    "by_difficulty": defaultdict(int),
    "by_exam": defaultdict(int),
    "sub_topics": defaultdict(int),
    "needs_figure": 0,
})

for c in classified_clusters:
    ch = c["classification"]["chapter"]
    diff = c["classification"]["difficulty"]
    subj = c["subject"]
    
    chapter_stats[f"{subj}|{ch}"]["total_questions"] += c["size"]
    chapter_stats[f"{subj}|{ch}"]["total_clusters"] += 1
    if c["size"] >= 2:
        chapter_stats[f"{subj}|{ch}"]["multi_clusters"] += 1
    chapter_stats[f"{subj}|{ch}"]["by_difficulty"][diff] += 1
    chapter_stats[f"{subj}|{ch}"]["by_exam"][c.get("representative", {}).get("exam", "unknown")] += 1
    chapter_stats[f"{subj}|{ch}"]["sub_topics"][c["classification"]["sub_topic"]] += c["size"]
    if c["classification"]["needs_figure"]:
        chapter_stats[f"{subj}|{ch}"]["needs_figure"] += c["size"]
    
    for year in c.get("years", []):
        chapter_stats[f"{subj}|{ch}"]["by_year"][year] += c["size"]

# Convert to serializable format
chapter_stats_clean = {}
for key, stats in chapter_stats.items():
    subj, ch = key.split("|", 1)
    chapter_stats_clean[key] = {
        "subject": subj,
        "chapter": ch,
        "total_questions": stats["total_questions"],
        "total_clusters": stats["total_clusters"],
        "multi_clusters": stats["multi_clusters"],
        "by_year": dict(stats["by_year"]),
        "by_difficulty": dict(stats["by_difficulty"]),
        "by_exam": dict(stats["by_exam"]),
        "sub_topics": dict(stats["sub_topics"]),
        "needs_figure": stats["needs_figure"],
    }

# ====== STEP 4: Build pattern data (repeating templates) ======
print("\n=== BUILDING PATTERN DATA ===")

patterns = []
for c in classified_clusters:
    if c["size"] >= 2:
        rep = c["representative"]
        patterns.append({
            "cluster_id": c["cluster_id"],
            "subject": c["subject"],
            "chapter": c["classification"]["chapter"],
            "sub_topic": c["classification"]["sub_topic"],
            "difficulty": c["classification"]["difficulty"],
            "core_concept": c["classification"]["core_concept"],
            "key_formula": c["classification"]["key_formula"],
            "common_trap": c["classification"]["common_trap"],
            "needs_figure": c["classification"]["needs_figure"],
            "question_type": c["classification"]["question_type"],
            "frequency": c["size"],
            "years": c.get("years", []),
            "exams": c.get("exams", []),
            "representative_question": rep.get("text", "")[:500],
            "answer": rep.get("answer"),
            "member_years": sorted(set(all_questions[m].get("year", "unknown") for m in c["members"] if m < len(all_questions))),
        })

patterns.sort(key=lambda x: -x["frequency"])
print(f"Total patterns (repeating templates): {len(patterns)}")

# ====== STEP 5: Save merged data ======
output = {
    "metadata": {
        "total_questions": len(all_questions),
        "total_clusters": len(classified_clusters),
        "classified_clusters": len(all_classifications),
        "total_patterns": len(patterns),
        "total_chapters": len(chapter_stats_clean),
    },
    "chapter_stats": chapter_stats_clean,
    "patterns": patterns,
    "clusters": [{"cluster_id": c["cluster_id"], "subject": c["subject"], "size": c["size"], "classification": c["classification"], "years": c.get("years", []), "exams": c.get("exams", []), "representative_question": c["representative"].get("text", "")[:500], "answer": c["representative"].get("answer")} for c in classified_clusters],
}

with open(f"{BASE}/raw_data/classified_data.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n=== SUMMARY ===")
print(f"Total questions: {len(all_questions)}")
print(f"Total clusters: {len(classified_clusters)}")
print(f"Classified: {len(all_classifications)}")
print(f"Repeating patterns: {len(patterns)}")
print(f"Chapter entries: {len(chapter_stats_clean)}")

# Print top chapters by question count
print(f"\nTop 20 chapters by question count:")
sorted_chapters = sorted(chapter_stats_clean.items(), key=lambda x: -x[1]["total_questions"])
for key, stats in sorted_chapters[:20]:
    print(f"  {stats['subject']:12s} | {stats['chapter']:35s} | Q={stats['total_questions']:4d} | clusters={stats['total_clusters']:3d} | patterns={stats['multi_clusters']:3d}")

print(f"\nSaved to raw_data/classified_data.json")