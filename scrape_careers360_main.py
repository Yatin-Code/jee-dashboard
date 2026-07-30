import requests, json
from bs4 import BeautifulSoup

url = "https://engineering.careers360.com/articles/jee-main-chapter-wise-weightage"
r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")
data = {}
for i, table in enumerate(tables):
    caption = ""
    caption_tag = table.find("caption") or table.find_previous(["h2", "h3", "h4"])
    if caption_tag:
        caption = caption_tag.get_text(strip=True)
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    data[caption or f"Table_{i}"] = rows

with open("/data/data/com.termux/files/home/jee-analysis/raw_data/careers360_main.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(tables)} tables")
