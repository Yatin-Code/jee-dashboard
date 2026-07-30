import json

with open("raw_data/collegedunia_main.json") as f:
    cd = json.load(f)
tables = list(cd.values())

def extract_year_table(table):
    """Extract year-by-year weightage data.
    Structure: row0 = header, row1 = years, row2+ = chapter data
    """
    years = table[1]  # ['2025', '2024', '2023', ...]
    data = {}
    for row in table[2:]:
        chapter = row[0]
        yearly = {}
        for i, year_val in enumerate(row[1:]):
            if i < len(years):
                yr = str(years[i])
                try:
                    yearly[yr] = float(year_val)
                except:
                    # Handle ranges like '3-4' - take the higher value
                    if '–' in year_val or '-' in year_val:
                        parts = str(year_val).replace('–', '-').split('-')
                        try:
                            yearly[yr] = (float(parts[0]) + float(parts[1])) / 2
                        except:
                            yearly[yr] = float(parts[0])
                    else:
                        yearly[yr] = 0.0
        data[chapter] = yearly
    return data

# Tables 25, 28 = Physics, 26, 29 = Chemistry, 27, 30 = Mathematics
phys_10yr = extract_year_table(tables[25])
chem_10yr = extract_year_table(tables[26])
math_10yr = extract_year_table(tables[27])
phys_5yr = extract_year_table(tables[28])
chem_5yr = extract_year_table(tables[29])
math_5yr = extract_year_table(tables[30])

years_10 = ['2016','2017','2018','2019','2020','2021','2022','2023','2024','2025']
years_5 = ['2021','2022','2023','2024','2025']

# Create per-chapter-per-year data
# For the 10-year data, we have broader categories
# Let's map them to individual chapters using Careers360 data as the base

# For the full report, we'll use 10-year trends for category-level analysis
# and Careers360 2026 data for individual chapter ranking

historical = {
    "years_available": "2016-2025 (year-by-year), 2026 (aggregate)",
    "physics_categories_10yr": phys_10yr,
    "chemistry_categories_10yr": chem_10yr,
    "mathematics_categories_10yr": math_10yr,
    "note": "Collegedunia uses broad categories (e.g., Modern Physics) not individual chapters. For per-chapter ranking use Careers360 2026 data."
}

with open("raw_data/historical_year_data.json", "w") as f:
    json.dump(historical, f, indent=2)

print("=== CORRECTED HISTORICAL DATA ===")
for k, v in historical.items():
    if k.endswith("_10yr"):
        print(f"\n{k}:")
        for chapter, years in v.items():
            vals = [f"{yr}={years[yr]}" for yr in years_10 if yr in years]
            print(f"  {chapter}: {', '.join(vals)}")
