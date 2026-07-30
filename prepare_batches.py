#!/usr/bin/env python3
"""
Prepare batch files for sub-agent classification.
Each batch contains cluster representative questions for an LLM sub-agent to classify.
"""
import json, os

BASE = "/data/data/com.termux/files/home/jee-analysis"

with open(f"{BASE}/raw_data/clusters.json") as f:
    data = json.load(f)

clusters = data["clusters"]

# We want to classify:
# 1. All multi-question clusters (1118) — these are the repeating patterns
# 2. A sample of singletons (to cover chapters that don't repeat but are still asked)

multi = [c for c in clusters if c["size"] >= 2]
single = [c for c in clusters if c["size"] == 1]

print(f"Multi clusters: {len(multi)}")
print(f"Single clusters: {len(single)}")

# For singletons, group by subject and take a representative sample
# We want about 200 singletons per subject (to cover unique topics)
from collections import defaultdict
single_by_subj = defaultdict(list)
for c in single:
    single_by_subj[c["subject"]].append(c)

# Sample singletons — take every Nth to get variety
sampled_singles = []
for subj, cs in single_by_subj.items():
    step = max(1, len(cs) // 150)  # ~150 per subject
    for i in range(0, len(cs), step):
        sampled_singles.append(cs[i])
    print(f"  {subj}: {len(cs)} singletons → sampled {len(range(0, len(cs), step))}")

# Combine all clusters to classify
to_classify = multi + sampled_singles
print(f"\nTotal to classify: {len(to_classify)}")

# Split into batches of ~50 (balanced across subjects)
BATCH_SIZE = 50
batches = []
for i in range(0, len(to_classify), BATCH_SIZE):
    batch = []
    for j in range(i, min(i + BATCH_SIZE, len(to_classify))):
        c = to_classify[j]
        rep = c["representative"]
        batch.append({
            "cluster_id": c["cluster_id"],
            "subject": c["subject"],
            "size": c["size"],
            "years": c["years"],
            "exams": c["exams"],
            "question_text": rep["text"][:500],
            "answer": rep.get("answer"),
            "exam": rep.get("exam"),
            "year": rep.get("year"),
        })
    batches.append(batch)

print(f"Batches: {len(batches)} (size {BATCH_SIZE})")

# Save batch files
batch_dir = f"{BASE}/raw_data/batches"
os.makedirs(batch_dir, exist_ok=True)

for i, batch in enumerate(batches):
    with open(f"{batch_dir}/batch_{i:03d}.json", "w") as f:
        json.dump(batch, f, indent=2)

print(f"Saved {len(batches)} batch files to {batch_dir}/")

# Also save a summary
with open(f"{batch_dir}/batch_summary.json", "w") as f:
    json.dump({
        "total_clusters": len(to_classify),
        "multi_clusters": len(multi),
        "sampled_singles": len(sampled_singles),
        "batches": len(batches),
        "batch_size": BATCH_SIZE,
    }, f, indent=2)

print("Done")