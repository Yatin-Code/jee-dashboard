#!/usr/bin/env python3
"""
JEE Question Extractor — extracts individual questions from OCR'd papers.
Handles 4 formats: eSaral (2019-2024), Collegedunia/NTA (2025-2026), Advanced eSaral, Advanced official.
Outputs: questions_raw.json
"""
import json, re, os
from collections import defaultdict

BASE = "/data/data/com.termux/files/home/jee-analysis"

def load_ocr():
    with open(f"{BASE}/raw_data/ocr_results.json") as f:
        return json.load(f)

def detect_subject_from_url(url):
    u = url.lower()
    if "math" in u: return "mathematics"
    if "physics" in u: return "physics"
    if "chemistry" in u or "chem" in u: return "chemistry"
    return None

def detect_subject_from_text(text):
    """For combined papers — detect which section we're in."""
    text_upper = text.upper()
    # Find subject section headers
    patterns = [
        (r'SECTION\s*:\s*(PHYSICS|CHEMISTRY|MATHEMATICS|MATH(?:EMATICS)?)\s*SECTION\s*[AB]', 'section_header'),
        (r'Section\s*:\s*(Physics|Chemistry|Mathematics|Math)\s*Section\s*[AB]', 'section_header'),
        (r'(PHYSICS|CHEMISTRY|MATHEMATICS)\s*SECTION\s*[-:]', 'section_header'),
    ]
    return None

def split_combined_by_sections(text):
    """Split a combined paper into physics/chemistry/maths sections."""
    sections = {}
    
    # Find section boundaries
    # Pattern: "Section : Mathematics Section A" or "Section : Physics Section B"
    section_pattern = r'(?:Section\s*:\s*|SECTION\s*:\s*)(Physics|Chemistry|Mathematics|Math)(?:\s+Section\s+[AB])?'
    matches = list(re.finditer(section_pattern, text, re.IGNORECASE))
    
    if len(matches) >= 3:
        # Sort by position
        for i, m in enumerate(matches):
            subj_raw = m.group(1).lower()
            if "math" in subj_raw: subj = "mathematics"
            elif "physics" in subj_raw: subj = "physics"
            elif "chem" in subj_raw: subj = "chemistry"
            else: continue
            
            start = m.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            # For each subject, take the content from this section header to the next
            if subj not in sections:
                sections[subj] = text[start:end]
            else:
                sections[subj] += "\n" + text[start:end]
        return sections
    
    # Fallback: look for "Mathematics)", "( Physics )", "( Chemistry )" type headers
    section_pattern2 = r'\(\s*(Physics|Chemistry|Mathematics|Math)\s*\)'
    matches2 = list(re.finditer(section_pattern2, text, re.IGNORECASE))
    if len(matches2) >= 3:
        for i, m in enumerate(matches2):
            subj_raw = m.group(1).lower()
            if "math" in subj_raw: subj = "mathematics"
            elif "physics" in subj_raw: subj = "physics"
            elif "chem" in subj_raw: subj = "chemistry"
            else: continue
            start = m.end()
            end = matches2[i+1].start() if i+1 < len(matches2) else len(text)
            if subj not in sections:
                sections[subj] = text[start:end]
            else:
                sections[subj] += "\n" + text[start:end]
        return sections
    
    return sections

def extract_answer(text):
    """Extract the official answer from question text."""
    patterns = [
        r'Official\s*Ans\.?\s*by\s*NTA\s*\((\d)\)',
        r'Official\s*Ans\.?\s*by\s*NTA\s*\(?([A-D])\)?',
        r'Ans\.?\s*\((\d)\)',
        r'Ans\.?\s*\(([A-D])\)',
        r'Correct\s*Option\s*[:\-]?\s*(\d)',
        r'Chosen\s*Option\s*:\s*(\d)',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)
    return None

def extract_questions_esaral(text, subject):
    """Extract questions from eSaral format papers (2019-2024 Mains, 2019-2023 Advanced)."""
    questions = []
    
    # Try Q.N format first
    q_pattern = r'Q\.(\d+)\s+'
    matches = list(re.finditer(q_pattern, text))
    
    if len(matches) >= 5:
        for i, m in enumerate(matches):
            q_num = int(m.group(1))
            start = m.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            q_text = text[start:end].strip()
            
            # Clean up — remove solution after "Sol." or "Sol:"
            sol_match = re.search(r'\bSol\.?\s', q_text)
            if sol_match:
                q_text = q_text[:sol_match.start()].strip()
            
            # Remove "Official Ans" and everything after
            ans_match = re.search(r'Official\s*Ans', q_text)
            if ans_match:
                q_text = q_text[:ans_match.start()].strip()
            
            if len(q_text) > 15:
                answer = extract_answer(text[m.start():end])
                questions.append({
                    "q_num": q_num,
                    "text": q_text[:2000],
                    "answer": answer,
                    "subject": subject,
                })
        if questions:
            return questions
    
    # Try "N." format (number followed by dot and space, then capital letter)
    q_pattern2 = r'(?:^|\n)\s*(\d{1,2})\.\s+(?=[A-Z"\'(])'
    matches2 = list(re.finditer(q_pattern2, text))
    
    # Filter: question numbers should be sequential
    if len(matches2) >= 5:
        for i, m in enumerate(matches2):
            q_num = int(m.group(1))
            start = m.end()
            end = matches2[i+1].start() if i+1 < len(matches2) else len(text)
            q_text = text[start:end].strip()
            
            # Clean up solution
            sol_match = re.search(r'\bSol\.?\s', q_text)
            if sol_match:
                q_text = q_text[:sol_match.start()].strip()
            
            ans_match = re.search(r'Official\s*Ans', q_text)
            if ans_match:
                q_text = q_text[:ans_match.start()].strip()
            
            if len(q_text) > 15:
                answer = extract_answer(text[m.start():end])
                questions.append({
                    "q_num": q_num,
                    "text": q_text[:2000],
                    "answer": answer,
                    "subject": subject,
                })
        if questions:
            return questions
    
    # Fallback: try "N)" format
    q_pattern3 = r'(?:^|\n)\s*(\d{1,2})\)\s+'
    matches3 = list(re.finditer(q_pattern3, text))
    if len(matches3) >= 5:
        for i, m in enumerate(matches3):
            q_num = int(m.group(1))
            start = m.end()
            end = matches3[i+1].start() if i+1 < len(matches3) else len(text)
            q_text = text[start:end].strip()
            
            sol_match = re.search(r'\bSol\.?\s', q_text)
            if sol_match:
                q_text = q_text[:sol_match.start()].strip()
            
            ans_match = re.search(r'Official\s*Ans', q_text)
            if ans_match:
                q_text = q_text[:ans_match.start()].strip()
            
            if len(q_text) > 15:
                answer = extract_answer(text[m.start():end])
                questions.append({
                    "q_num": q_num,
                    "text": q_text[:2000],
                    "answer": answer,
                    "subject": subject,
                })
    
    return questions

def extract_questions_combined(text, subject):
    """Extract questions from combined NTA/Collegedunia format (2025-2026 Mains, 2024-2026 Advanced)."""
    questions = []
    
    # Format: Q.1 text... Options 1. ... 2. ... 3. ... 4. ... Question Type : MCQ ...
    q_pattern = r'Q\.(\d+)\s+'
    matches = list(re.finditer(q_pattern, text))
    
    if len(matches) >= 5:
        for i, m in enumerate(matches):
            q_num = int(m.group(1))
            start = m.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            q_text = text[start:end].strip()
            
            # Remove metadata lines (Question Type, Question ID, Option IDs, Status, Chosen Option)
            q_text = re.sub(r'Question Type\s*:\s*.*', '', q_text)
            q_text = re.sub(r'Question ID\s*:\s*.*', '', q_text)
            q_text = re.sub(r'Option \d+ ID\s*:\s*.*', '', q_text)
            q_text = re.sub(r'Status\s*:\s*.*', '', q_text)
            q_text = re.sub(r'Chosen Option\s*:\s*.*', '', q_text)
            q_text = re.sub(r'Marked For Review\s*', '', q_text)
            q_text = re.sub(r'Give\s+.*?n\s*Ans\s*wer\s*:', '', q_text)
            q_text = re.sub(r'Give\s+.*?n\s*Ans\s*wer\s*', '', q_text)
            q_text = re.sub(r'\n\s*\n', '\n', q_text).strip()
            
            if len(q_text) > 15:
                questions.append({
                    "q_num": q_num,
                    "text": q_text[:2000],
                    "answer": None,
                    "subject": subject,
                })
    
    return questions

def extract_questions_advanced(text, subject):
    """Extract questions from JEE Advanced papers."""
    questions = []
    
    # Advanced has sections with different question types
    # Try Q.N format
    q_pattern = r'(?:^|\n)\s*(\d{1,2})\.\s+(?=[A-Z"\'(])'
    matches = list(re.finditer(q_pattern, text))
    
    if len(matches) >= 3:
        for i, m in enumerate(matches):
            q_num = int(m.group(1))
            start = m.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            q_text = text[start:end].strip()
            
            # Clean solution
            sol_match = re.search(r'\bSol\.?\s', q_text)
            if sol_match:
                q_text = q_text[:sol_match.start()].strip()
            
            ans_match = re.search(r'\bAns\.?\s*\(', q_text)
            if ans_match:
                q_text = q_text[:ans_match.start()].strip()
            
            if len(q_text) > 15:
                answer = extract_answer(text[m.start():end])
                questions.append({
                    "q_num": q_num,
                    "text": q_text[:2000],
                    "answer": answer,
                    "subject": subject,
                })
    
    return questions

def detect_paper_info(paper_id, url):
    """Detect exam type, year, shift from paper ID and URL."""
    pid = paper_id.lower()
    
    exam = "unknown"
    year = "unknown"
    shift = "unknown"
    
    if pid.startswith("adv"):
        exam = "advanced"
        parts = paper_id.split("_")
        year = parts[1] if len(parts) > 1 else "unknown"
        if len(parts) > 2:
            shift = "_".join(parts[2:])
    elif pid.startswith("mains"):
        exam = "mains"
        parts = paper_id.split("_")
        year = parts[1] if len(parts) > 1 else "unknown"
        if len(parts) > 2:
            shift = "_".join(parts[2:])
    
    # Try to extract date from URL for eSaral papers
    url_date_match = re.search(r'(\d{1,2})-(\d{1,2})-(\d{4})', url)
    if url_date_match and shift == "unknown":
        shift = f"{url_date_match.group(1)}-{url_date_match.group(2)}"
    
    # Try to extract morning/evening from URL
    if "morning" in url.lower() or "morning" in pid:
        shift += "_morning" if shift != "unknown" else "morning"
    elif "evening" in url.lower() or "evening" in pid:
        shift += "_evening" if shift != "unknown" else "evening"
    
    return {"exam": exam, "year": year, "shift": shift}

def is_answer_key_only(text):
    """Check if paper is just an answer key (no question text)."""
    if "CORRECT OPTION ID" in text and "QUESTION ID" in text:
        # Check if there's any actual question text
        if "Q." not in text and len(text) < 5000:
            return True
    return False

# ====== MAIN ======
ocr_data = load_ocr()
all_questions = []
stats = {"total_papers": 0, "total_questions": 0, "by_exam": defaultdict(int), "by_subject": defaultdict(int), "by_year": defaultdict(int), "skipped": 0}

for key, paper in ocr_data["papers"].items():
    text = paper["text"]
    pid = paper["id"]
    url = paper["url"]
    
    stats["total_papers"] += 1
    
    # Skip answer-key-only papers
    if is_answer_key_only(text):
        stats["skipped"] += 1
        continue
    
    info = detect_paper_info(pid, url)
    subject_from_url = detect_subject_from_url(url)
    
    # Determine if combined or subject-specific
    is_combined = subject_from_url is None
    
    extracted = []
    
    if is_combined:
        # Split by sections
        sections = split_combined_by_sections(text)
        
        if sections and len(sections) >= 2:
            for subj, section_text in sections.items():
                # Determine exam format
                if info["exam"] == "advanced":
                    qs = extract_questions_advanced(section_text, subj)
                else:
                    qs = extract_questions_combined(section_text, subj)
                extracted.extend(qs)
        else:
            # Try to detect subject from content
            text_lower = text.lower()
            phys_score = text_lower.count("physics") + text_lower.count("field") + text_lower.count("charge") + text_lower.count("circuit") + text_lower.count("velocity")
            chem_score = text_lower.count("chemistry") + text_lower.count("mole") + text_lower.count("reaction") + text_lower.count("bond") + text_lower.count("compound")
            math_score = text_lower.count("mathematics") + text_lower.count("equation") + text_lower.count("integral") + text_lower.count("matrix") + text_lower.count("function")
            
            best = max([("physics", phys_score), ("chemistry", chem_score), ("mathematics", math_score)], key=lambda x: x[1])
            if best[1] > 3:
                if info["exam"] == "advanced":
                    extracted = extract_questions_advanced(text, best[0])
                else:
                    extracted = extract_questions_combined(text, best[0])
    else:
        # Subject-specific paper
        if info["exam"] == "advanced":
            extracted = extract_questions_advanced(text, subject_from_url)
        else:
            extracted = extract_questions_esaral(text, subject_from_url)
    
    # Add metadata to each question
    for q in extracted:
        q["exam"] = info["exam"]
        q["year"] = info["year"]
        q["shift"] = info["shift"]
        q["paper_id"] = pid
        all_questions.append(q)
        stats["total_questions"] += 1
        stats["by_exam"][info["exam"]] += 1
        stats["by_subject"][q["subject"]] += 1
        stats["by_year"][info["year"]] += 1

# Save
output = {
    "metadata": {
        "total_papers_processed": stats["total_papers"],
        "total_questions": stats["total_questions"],
        "skipped_answer_keys": stats["skipped"],
        "by_exam": dict(stats["by_exam"]),
        "by_subject": dict(stats["by_subject"]),
        "by_year": dict(stats["by_year"]),
    },
    "questions": all_questions,
}

with open(f"{BASE}/raw_data/questions_raw.json", "w") as f:
    json.dump(output, f, indent=2)

print("=== EXTRACTION RESULTS ===")
print(f"Papers processed: {stats['total_papers']}")
print(f"Skipped (answer keys): {stats['skipped']}")
print(f"Total questions: {stats['total_questions']}")
print(f"\nBy exam: {dict(stats['by_exam'])}")
print(f"By subject: {dict(stats['by_subject'])}")
print(f"By year: {dict(stats['by_year'])}")
print(f"\nSaved to raw_data/questions_raw.json")