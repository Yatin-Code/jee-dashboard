import markdown
import os, re

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.7;
  color: #1a1a1a;
  max-width: 210mm;
  margin: 0 auto;
  padding: 20mm 25mm;
  background: white;
}
h1 {
  font-size: 24pt;
  color: #1a237e;
  border-bottom: 3px solid #1a237e;
  padding-bottom: 10px;
  margin-bottom: 20px;
  margin-top: 0;
}
h2 {
  font-size: 16pt;
  color: #283593;
  border-bottom: 2px solid #c5cae9;
  padding-bottom: 6px;
  margin-top: 28px;
  margin-bottom: 12px;
}
h3 {
  font-size: 13pt;
  color: #3949ab;
  margin-top: 20px;
  margin-bottom: 8px;
}
h4 { font-size: 11pt; color: #5c6bc0; margin-top: 14px; }
p { margin: 8px 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0;
  font-size: 9.5pt;
  page-break-inside: avoid;
}
th {
  background: #1a237e;
  color: white;
  padding: 7px 9px;
  text-align: left;
  font-weight: 600;
}
td {
  padding: 5px 9px;
  border-bottom: 1px solid #e0e0e0;
}
tr:nth-child(even) { background: #f5f5f5; }
tr:hover { background: #e8eaf6; }
code {
  background: #e8eaf6;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10pt;
  font-family: 'Courier New', monospace;
}
blockquote {
  border-left: 4px solid #1a237e;
  margin: 12px 0;
  padding: 10px 18px;
  background: #f5f7ff;
  font-style: italic;
  border-radius: 0 6px 6px 0;
}
strong { color: #1a237e; }
em { color: #c62828; }
hr {
  border: none;
  border-top: 2px solid #c5cae9;
  margin: 24px 0;
}
ul, ol { padding-left: 24px; margin: 8px 0; }
li { margin-bottom: 4px; }
img { max-width: 100%; }
.page-break { page-break-before: always; }
.footer {
  margin-top: 40px;
  padding-top: 15px;
  border-top: 2px solid #c5cae9;
  font-size: 9pt;
  color: #666;
  text-align: center;
}
.section-title {
  background: linear-gradient(135deg, #1a237e, #3949ab);
  color: white;
  padding: 12px 18px;
  border-radius: 6px;
  margin: 20px 0 16px 0;
}
.section-title h2 {
  color: white;
  border: none;
  margin: 0;
  padding: 0;
}
.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 8pt;
  font-weight: 600;
}
.tag-green { background: #e8f5e9; color: #2e7d32; }
.tag-red { background: #ffebee; color: #c62828; }
.tag-blue { background: #e3f2fd; color: #1565c0; }
.tag-orange { background: #fff3e0; color: #e65100; }
"""

def md_to_html(md_path):
    with open(md_path) as f:
        md_content = f.read()

    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])

    name = os.path.basename(md_path).replace('.md', '').replace('_', ' ').title()
    if name == 'Master Report':
        name = 'JEE Chapter Weightage Analysis — Master Report'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}</title>
<style>{CSS}</style>
</head>
<body>
{html_body}
<div class="footer">
  Generated from JEE Chapter Weightage Analysis — Data sources: Collegedunia, Careers360, Vedantu (2016-2026)
</div>
</body>
</html>"""
    return html

base = "/data/data/com.termux/files/home/jee-analysis"
files = [
    "reports/MASTER_REPORT.md",
    "reports/mains_physics.md",
    "reports/mains_chemistry.md",
    "reports/mains_mathematics.md",
    "reports/advanced_physics.md",
    "reports/advanced_chemistry.md",
    "reports/advanced_mathematics.md",
]

for fname in files:
    md_path = f"{base}/{fname}"
    html_path = md_path.replace('.md', '.html')
    print(f"Converting {fname} → {os.path.basename(html_path)}", end=" ")
    try:
        html = md_to_html(md_path)
        with open(html_path, 'w') as f:
            f.write(html)
        size = os.path.getsize(html_path)
        print(f"✓ {size/1024:.0f} KB")
    except Exception as e:
        print(f"✗ {e}")

# Copy HTML files to storage
os.system(f"cp {base}/reports/*.html /storage/emulated/0/Download/jee/reports/ 2>/dev/null")
os.system(f"rm -f {base}/reports/*.html 2>/dev/null")
print("\n✓ HTML files created and copied to /storage/emulated/0/Download/jee/reports/")
print("  Open in Chrome → tap ⋮ → Print → Save as PDF")
