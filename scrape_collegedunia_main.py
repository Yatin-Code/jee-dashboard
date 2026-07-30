import requests, json, re
from bs4 import BeautifulSoup

url = "https://www.collegedunia.com/exams/jee-main/chapter-wise-weightage"
r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
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

with open("/data/data/com.termux/files/home/jee-analysis/raw_data/collegedunia_main.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(tables)} tables")
print(json.dumps({k: len(v) for k, v in data.items()}, indent=2))
