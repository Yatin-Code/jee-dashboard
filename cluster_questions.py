#!/usr/bin/env python3
"""
JEE Question Clustering — groups similar questions using TF-IDF + cosine similarity.
Outputs representative questions for each cluster + full cluster membership.
"""
import json, re, math
from collections import defaultdict, Counter

BASE = "/data/data/com.termux/files/home/jee-analysis"

def normalize_text(text):
    """Normalize question text for comparison."""
    t = text.lower()
    # Remove numbers (they vary between instances of same template)
    t = re.sub(r'\b\d+\.?\d*\b', '#', t)
    # Remove common OCR artifacts
    t = re.sub(r'[^\w\s#]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def tokenize(text):
    """Extract meaningful tokens."""
    t = normalize_text(text)
    tokens = [w for w in t.split() if len(w) > 2]
    return tokens

def compute_tfidf(docs):
    """Compute TF-IDF vectors for all documents."""
    N = len(docs)
    
    # Document frequency
    df = defaultdict(int)
    for doc in docs:
        seen = set(tokenize(doc))
        for w in seen:
            df[w] += 1
    
    # IDF
    idf = {w: math.log(N / (df[w] + 1)) + 1 for w in df}
    
    # TF-IDF vectors
    vectors = []
    for doc in docs:
        tokens = tokenize(doc)
        tf = Counter(tokens)
        vec = {w: tf[w] * idf.get(w, 0) for w in tf}
        # Normalize
        norm = math.sqrt(sum(v*v for v in vec.values())) or 1
        vec = {w: v/norm for w, v in vec.items()}
        vectors.append(vec)
    
    return vectors, idf

def cosine_sim(v1, v2):
    """Compute cosine similarity between two sparse vectors."""
    if len(v1) > len(v2):
        v1, v2 = v2, v1
    return sum(v1[w] * v2.get(w, 0) for w in v1)

def cluster_questions(questions, threshold=0.55, min_cluster_size=2):
    """Cluster questions by text similarity."""
    # Group by subject first
    by_subject = defaultdict(list)
    for i, q in enumerate(questions):
        by_subject[q["subject"]].append((i, q))
    
    all_clusters = []
    
    for subject, qs in by_subject.items():
        if len(qs) < 2:
            for i, q in qs:
                all_clusters.append({
                    "cluster_id": len(all_clusters),
                    "subject": subject,
                    "members": [i],
                    "representative": q,
                    "size": 1
                })
            continue
        
        # Compute TF-IDF for this subject's questions
        texts = [q["text"] for _, q in qs]
        vectors, idf = compute_tfidf(texts)
        
        # Greedy clustering
        assigned = [False] * len(qs)
        clusters = []
        
        for i in range(len(qs)):
            if assigned[i]:
                continue
            
            cluster = [i]
            assigned[i] = True
            best_rep = vectors[i]
            
            for j in range(i+1, len(qs)):
                if assigned[j]:
                    continue
                sim = cosine_sim(vectors[i], vectors[j])
                if sim >= threshold:
                    cluster.append(j)
                    assigned[j] = True
            
            # Find best representative (question closest to cluster centroid)
            if len(cluster) > 1:
                # Compute centroid
                centroid = defaultdict(float)
                for idx in cluster:
                    for w, v in vectors[idx].items():
                        centroid[w] += v / len(cluster)
                
                best_sim = -1
                best_idx = cluster[0]
                for idx in cluster:
                    s = cosine_sim(vectors[idx], centroid)
                    if s > best_sim:
                        best_sim = s
                        best_idx = idx
            else:
                best_idx = cluster[0]
            
            member_indices = [qs[idx][0] for idx in cluster]
            clusters.append({
                "members": member_indices,
                "representative_idx": qs[best_idx][0],
                "size": len(cluster)
            })
        
        # Sort clusters by size (largest first)
        clusters.sort(key=lambda c: -c["size"])
        
        for c in clusters:
            all_clusters.append({
                "cluster_id": len(all_clusters),
                "subject": subject,
                "members": c["members"],
                "representative": questions[c["representative_idx"]],
                "size": c["size"],
                "years": sorted(set(questions[m]["year"] for m in c["members"] if questions[m]["year"] != "unknown")),
                "exams": sorted(set(questions[m]["exam"] for m in c["members"]))
            })
    
    return all_clusters

# ====== MAIN ======
with open(f"{BASE}/raw_data/questions_raw.json") as f:
    data = json.load(f)

questions = data["questions"]
print(f"Loaded {len(questions)} questions")

print("Clustering...")
clusters = cluster_questions(questions, threshold=0.55)

# Stats
multi_clusters = [c for c in clusters if c["size"] >= 2]
single_clusters = [c for c in clusters if c["size"] == 1]

print(f"\n=== CLUSTERING RESULTS ===")
print(f"Total clusters: {len(clusters)}")
print(f"Multi-question clusters (templates): {len(multi_clusters)}")
print(f"Single-question clusters: {len(single_clusters)}")
print(f"Questions in multi-clusters: {sum(c['size'] for c in multi_clusters)}")
print(f"Questions in single-clusters: {len(single_clusters)}")

# Show top clusters by size
print(f"\nTop 20 largest clusters:")
for c in sorted(clusters, key=lambda x: -x["size"])[:20]:
    rep = c["representative"]
    print(f"  Cluster {c['cluster_id']:3d} | {c['subject']:12s} | size={c['size']:3d} | years={c['years'][:5]} | {rep['text'][:100]}...")

# Save clusters
output = {
    "metadata": {
        "total_questions": len(questions),
        "total_clusters": len(clusters),
        "multi_clusters": len(multi_clusters),
        "single_clusters": len(single_clusters),
        "threshold": 0.55,
    },
    "clusters": clusters,
}

with open(f"{BASE}/raw_data/clusters.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to raw_data/clusters.json")