import requests, json
from bs4 import BeautifulSoup

urls = {
    "vedantu_main": "https://www.vedantu.com/jee-main/weightage",
    "vedantu_advanced": "https://www.vedantu.com/jee-advanced/weightage"
}

all_data = {}

for name, url in urls.items():
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
    all_data[name] = data

with open("/data/data/com.termux/files/home/jee-analysis/raw_data/vedantu.json", "w") as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {sum(len(v) for v in all_data.values())} tables")
