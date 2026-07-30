import json, re
from collections import defaultdict

def parse_number(s):
    s = s.strip().replace('%', '').replace(',', '')
    try: return int(s)
    except: return 0

def parse_float(s):
    s = s.strip().replace('%', '').replace(',', '')
    try: return float(s)
    except: return 0.0

# ====== LOAD RAW DATA ======
with open("raw_data/collegedunia_main.json") as f:
    cd_main = json.load(f)
tables_cd = list(cd_main.values())

with open("raw_data/collegedunia_advanced.json") as f:
    cd_adv = json.load(f)
tables_cd_adv = list(cd_adv.values())

with open("raw_data/careers360_main.json") as f:
    c360 = json.load(f)

with open("raw_data/vedantu.json") as f:
    ved = json.load(f)

# Helper: Find table by checking header keywords
def find_table(tables, keywords, min_rows=2):
    for t in tables:
        if len(t) < min_rows: continue
        header = ' '.join(str(c).lower() for c in t[0])
        if any(k in header for k in keywords):
            return t
    return None

def find_tables(tables, keywords, min_rows=2):
    results = []
    for t in tables:
        if len(t) < min_rows: continue
        header = ' '.join(str(c).lower() for c in t[0])
        if any(k in header for k in keywords):
            results.append(t)
    return results

# ====== EXTRACT: Careers360 (aggregate 2026 data, out of 475) ======
def extract_careers360_table(table_name, col_q, col_wt):
    """Extract from careers360 tables"""
    t = c360.get(table_name)
    if not t: return {}
    data = {}
    for row in t[1:]:
        if len(row) < 3: continue
        name = row[0].strip()
        q_count = parse_number(row[col_q])
        wt = parse_float(row[col_wt])
        data[name] = {"questions": q_count, "weightage_pct": wt}
    return data

c360_physics_11 = extract_careers360_table("JEE Main Chapter-Wise Weightage of Class 11 Physics", 1, 2)
c360_physics_12 = extract_careers360_table("JEE Mains Chapter-Wise Weightage Of Class 12 Physics", 1, 2)
c360_chem_11 = extract_careers360_table("JEE Mains 2027 Chapter-Wise Weightage of Class 11 Chemistry", 1, 2)
c360_chem_12 = extract_careers360_table("JEE Mains 2027 Chapter-Wise Weightage of Class 12 Chemistry", 1, 2)
c360_math = extract_careers360_table("JEE Mains 2027 Chapter-wise Weightage for Mathematics", 1, 2)

# Most asked topics
def extract_most_asked(table_name):
    t = c360.get(table_name)
    if not t: return []
    result = []
    for row in t[1:]:
        if len(row) >= 3:
            result.append({"topic": row[0], "chapter": row[1], "questions": parse_number(row[2])})
    return result

most_asked_physics = extract_most_asked("Most Asked Topics Of JEE Mains 2027 Physics")
most_asked_chem = extract_most_asked("Most Asked Topics Of JEE Mains 2027 Chemistry")
most_asked_math = extract_most_asked("Most Asked Topics Of JEE Mains 2027 Mathematics")

# ====== EXTRACT: Collegedunia Main (shift-by-shift 2025) ======
def extract_shift_table(table, subject):
    """Extract chapter-wise totals from shift-by-shift table"""
    data = {}
    for row in table[1:]:
        if len(row) < 2: continue
        name = row[0].strip()
        total = parse_number(row[1])
        data[name] = {"total_questions": total, "source": "collegedunia_2025_shifts"}
    return data

cd_physics_shifts = extract_shift_table(tables_cd[13] if len(tables_cd) > 13 else [], "Physics")
cd_chem_shifts = extract_shift_table(tables_cd[15] if len(tables_cd) > 15 else [], "Chemistry")

# Weightage estimate tables
cd_phys_wt_11 = find_table(tables_cd, ["kinematics", "law of motion"])
cd_phys_wt_12 = find_table(tables_cd, ["electrostatics", "current electricity"])
cd_chem_wt_11 = find_table(tables_cd, ["structure of an atom", "chemical bonding"])
cd_chem_wt_12 = find_table(tables_cd, ["coordination", "aldehyde"])
cd_math_wt = find_table(tables_cd, ["coordinate geometry", "3d geometry"])

def extract_weightage_table(table):
    if not table: return {}
    data = {}
    for row in table[1:]:
        if len(row) >= 2:
            name = row[0].strip()
            wt = parse_float(row[1])
            data[name] = {"weightage_pct": wt}
    return data

cd_phys_wt_11_data = extract_weightage_table(cd_phys_wt_11)
cd_phys_wt_12_data = extract_weightage_table(cd_phys_wt_12)
cd_chem_wt_11_data = extract_weightage_table(cd_chem_wt_11)
cd_chem_wt_12_data = extract_weightage_table(cd_chem_wt_12)
cd_math_wt_data = extract_weightage_table(cd_math_wt)

# ====== EXTRACT: Vedantu (5-year weightage, 2025 session data) ======
ved_main = ved.get("vedantu_main", {})
ved_adv = ved.get("vedantu_advanced", {})

def find_vedantu_table(tables_dict, keywords):
    for k, v in tables_dict.items():
        if len(v) < 2: continue
        header = ' '.join(str(c).lower() for c in v[0])
        if any(kw in header for kw in keywords):
            return v
    return None

# Past 5-year weightage
ved_physics_5yr = find_vedantu_table(ved_main, ["physics chapter-wise weightage", "past 5"])
ved_chem_5yr = find_vedantu_table(ved_main, ["chemistry chapter-wise weightage", "past 5"])
ved_math_5yr = find_vedantu_table(ved_main, ["mathematics chapter-wise weightage", "past 5"])

# 2025 session data (question counts per chapter)
ved_physics_2025 = find_vedantu_table(ved_main, ["2025 physics"])
ved_chem_2025 = find_vedantu_table(ved_main, ["2025 chemistry"])
ved_math_2025 = find_vedantu_table(ved_main, ["2025 maths"])

# 2026 expected
ved_physics_2026 = find_vedantu_table(ved_main, ["2026 physics"])
ved_chem_2026 = find_vedantu_table(ved_main, ["2026 chemistry"])
ved_math_2026 = find_vedantu_table(ved_main, ["2026 maths"])

def extract_vedantu_5yr(table):
    if not table: return {}
    data = {}
    for row in table[1:]:
        if len(row) >= 3:
            name = row[1].strip()
            wt = parse_float(row[2])
            data[name] = {"weightage_pct": wt}
    return data

def extract_vedantu_2025(table):
    if not table: return {}
    data = {}
    for row in table[1:]:
        if len(row) >= 3:
            name = row[0].strip()
            jan = parse_number(row[1])
            apr = parse_number(row[2])
            data[name] = {"jan_2025": jan, "apr_2025": apr, "total_2025": jan + apr}
    return data

def extract_vedantu_2026(table):
    if not table: return {}
    data = {}
    for row in table[1:]:
        if len(row) >= 3:
            name = row[0].strip()
            q = parse_number(row[1])
            wt = parse_float(row[2])
            data[name] = {"questions": q, "weightage_pct": wt}
    return data

ved_physics_5yr_data = extract_vedantu_5yr(ved_physics_5yr)
ved_chem_5yr_data = extract_vedantu_5yr(ved_chem_5yr)
ved_math_5yr_data = extract_vedantu_5yr(ved_math_5yr)

ved_physics_2025_data = extract_vedantu_2025(ved_physics_2025)
ved_chem_2025_data = extract_vedantu_2025(ved_chem_2025)
ved_math_2025_data = extract_vedantu_2025(ved_math_2025)

ved_physics_2026_data = extract_vedantu_2026(ved_physics_2026)
ved_chem_2026_data = extract_vedantu_2026(ved_chem_2026)
ved_math_2026_data = extract_vedantu_2026(ved_math_2026)

# ====== EXTRACT: Collegedunia Advanced ======
def find_cd_adv_table(keywords):
    for t in tables_cd_adv:
        if len(t) < 2: continue
        header = ' '.join(str(c).lower() for c in t[0])
        if any(k in header for k in keywords):
            return t
    return None

def extract_adv_table(table):
    if not table: return {}
    data = {}
    for row in table[1:]:
        if len(row) >= 5:
            name = row[0].strip()
            if name.lower().startswith("class"): continue
            q = parse_number(row[2])
            marks = parse_number(row[3])
            wt = parse_float(row[4])
            data[name] = {"questions": q, "marks": marks, "weightage_pct": wt}
    return data

adv_physics = extract_adv_table(find_cd_adv_table(["physics chapter"]))
adv_chem = extract_adv_table(find_cd_adv_table(["chemistry chapter"]))
adv_math = extract_adv_table(find_cd_adv_table(["mathematics chapter"]))

# ====== EXTRACT: Vedantu Advanced ======
def extract_ved_adv_table(table):
    if not table: return {}
    data = {}
    for row in table[1:]:
        if len(row) >= 5:
            name = row[0].strip()
            if name.lower().startswith("class"): continue
            q = parse_number(row[2])
            marks = parse_number(row[3])
            wt = parse_float(row[4])
            data[name] = {"questions": q, "marks": marks, "weightage_pct": wt}
    return data

ved_adv_physics = extract_ved_adv_table(ved_adv.get("JEE Advanced Physics Chapter-Wise Weightage 2026"))
ved_adv_chem = extract_ved_adv_table(ved_adv.get("JEE Advanced Chemistry Chapter-Wise Weightage 2026"))
ved_adv_math = extract_ved_adv_table(ved_adv.get("JEE Advanced Mathematics Chapter-Wise Weightage 2026"))

# ====== BUILD CONSOLIDATED OUTPUT ======
consolidated = {
    "jee_mains": {
        "physics": {
            "careers360_2026_aggregate": {**c360_physics_11, **c360_physics_12},
            "collegedunia_2025_shift_totals": cd_physics_shifts,
            "collegedunia_weightage_class11": cd_phys_wt_11_data,
            "collegedunia_weightage_class12": cd_phys_wt_12_data,
            "vedantu_5yr_weightage": ved_physics_5yr_data,
            "vedantu_2025_session_counts": ved_physics_2025_data,
            "vedantu_2026_expected": ved_physics_2026_data,
            "most_asked_topics": most_asked_physics
        },
        "chemistry": {
            "careers360_2026_aggregate": {**c360_chem_11, **c360_chem_12},
            "collegedunia_2025_shift_totals": cd_chem_shifts,
            "collegedunia_weightage_class11": cd_chem_wt_11_data,
            "collegedunia_weightage_class12": cd_chem_wt_12_data,
            "vedantu_5yr_weightage": ved_chem_5yr_data,
            "vedantu_2025_session_counts": ved_chem_2025_data,
            "vedantu_2026_expected": ved_chem_2026_data,
            "most_asked_topics": most_asked_chem
        },
        "mathematics": {
            "careers360_2026_aggregate": c360_math,
            "collegedunia_2025_shift_totals": {}, # Math shift table not identified
            "collegedunia_weightage": cd_math_wt_data,
            "vedantu_5yr_weightage": ved_math_5yr_data,
            "vedantu_2025_session_counts": ved_math_2025_data,
            "vedantu_2026_expected": ved_math_2026_data,
            "most_asked_topics": most_asked_math
        }
    },
    "jee_advanced": {
        "physics": {
            "collegedunia_weightage": adv_physics,
            "vedantu_weightage": ved_adv_physics
        },
        "chemistry": {
            "collegedunia_weightage": adv_chem,
            "vedantu_weightage": ved_adv_chem
        },
        "mathematics": {
            "collegedunia_weightage": adv_math,
            "vedantu_weightage": ved_adv_math
        }
    }
}

with open("raw_data/consolidated.json", "w") as f:
    json.dump(consolidated, f, indent=2)

# Summary
print("=== CONSOLIDATION COMPLETE ===")
for exam, subjects in consolidated.items():
    print(f"\n--- {exam.upper()} ---")
    for subj, sources in subjects.items():
        n_sources = sum(1 for v in sources.values() if v)
        chapter_sets = []
        for v in sources.values():
            if isinstance(v, dict):
                chapter_sets.append(list(v.keys()))
        n_chapters = len(set().union(*chapter_sets) if chapter_sets else set())
        print(f"  {subj}: {n_sources} sources, ~{n_chapters} chapters identified")
