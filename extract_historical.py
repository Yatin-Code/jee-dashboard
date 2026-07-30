import json

with open("raw_data/collegedunia_main.json") as f:
    cd = json.load(f)
tables = list(cd.values())

# Tables 25, 26, 27: 2016-2025 (10 years) for Physics, Chemistry, Math
# Tables 28, 29, 30: 2021-2025 (5 years, slightly different groupings)

def extract_year_table(table, subject):
    """Extract year-by-year weightage data"""
    years = table[0]  # [2025, 2024, ...]
    data = {}
    for row in table[1:]:
        chapter = row[0]
        yearly = {}
        for i, year_val in enumerate(row[1:]):
            if i < len(years):
                try:
                    yearly[str(years[i])] = float(year_val)
                except:
                    yearly[str(years[i])] = year_val  # might be '3-4' range
        data[chapter] = yearly
    return data

# 10-year data (2016-2025)
phys_10yr = extract_year_table(tables[25], "Physics")
chem_10yr = extract_year_table(tables[26], "Chemistry")
math_10yr = extract_year_table(tables[27], "Mathematics")

# 5-year data (2021-2025)
phys_5yr = extract_year_table(tables[28], "Physics")
chem_5yr = extract_year_table(tables[29], "Chemistry")
math_5yr = extract_year_table(tables[30], "Mathematics")

# Build historical data structure
historical = {
    "physics_10yr": phys_10yr,
    "chemistry_10yr": chem_10yr,
    "mathematics_10yr": math_10yr,
    "physics_5yr_detail": phys_5yr,
    "chemistry_5yr_detail": chem_5yr,
    "mathematics_5yr_detail": math_5yr,
}

# Save
with open("raw_data/historical_year_data.json", "w") as f:
    json.dump(historical, f, indent=2)

print("=== HISTORICAL DATA EXTRACTED ===")
for k, v in historical.items():
    print(f"\n{k}:")
    for chapter, years in v.items():
        print(f"  {chapter}: {years}")
