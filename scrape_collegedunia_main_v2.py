import requests, json, re
from bs4 import BeautifulSoup

url = "https://collegedunia.com/exams/jee-main/chapter-wise-weightage"
r = requests.get(url, timeout=30, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})
soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")
data = {}
for i, table in enumerate(tables):
    caption = table.find("caption")
    caption_text = caption.get_text(strip=True) if caption else f"Table_{i}"
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    data[caption_text] = rows

# Also look for Next.js __NEXT_DATA__ with JSON tables
next_data = soup.find("script", id="__NEXT_DATA__")
if next_data:
    data["__NEXT_DATA__"] = next_data.string[:5000] if next_data.string else ""

with open("/data/data/com.termux/files/home/jee-analysis/raw_data/collegedunia_main.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(tables)} tables")
for k, v in data.items():
    if k != "__NEXT_DATA__":
        print(f"  {k}: {len(v)} rows")
