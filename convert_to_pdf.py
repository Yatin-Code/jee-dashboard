import markdown
import weasyprint
import os

CSS = """
@page {
  size: A4;
  margin: 2cm 2.5cm;
  @top-center {
    content: "JEE Chapter Weightage Analysis";
    font-size: 9pt;
    color: #666;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
  @bottom-center {
    content: "Page " counter(page);
    font-size: 9pt;
    color: #666;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
}

body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #1a1a1a;
}

h1 {
  font-size: 22pt;
  color: #1a237e;
  border-bottom: 3px solid #1a237e;
  padding-bottom: 8px;
  margin-top: 0;
}

h2 {
  font-size: 16pt;
  color: #283593;
  border-bottom: 2px solid #c5cae9;
  padding-bottom: 4px;
  margin-top: 24px;
}

h3 {
  font-size: 13pt;
  color: #3949ab;
  margin-top: 18px;
}

h4 {
  font-size: 11pt;
  color: #5c6bc0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 10pt;
}

th {
  background: #1a237e;
  color: white;
  padding: 8px 10px;
  text-align: left;
  font-weight: 600;
}

td {
  padding: 6px 10px;
  border-bottom: 1px solid #e0e0e0;
}

tr:nth-child(even) {
  background: #f5f5f5;
}

tr:hover {
  background: #e8eaf6;
}

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
  padding: 8px 16px;
  background: #f5f7ff;
  font-style: italic;
}

strong {
  color: #1a237e;
}

em {
  color: #c62828;
}

hr {
  border: none;
  border-top: 2px solid #c5cae9;
  margin: 20px 0;
}

ul, ol {
  padding-left: 24px;
}

li {
  margin-bottom: 4px;
}

p {
  margin: 8px 0;
}
"""

def md_to_pdf(md_path, pdf_path):
    with open(md_path) as f:
        md_content = f.read()

    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    weasyprint.HTML(string=html).write_pdf(pdf_path)
    return os.path.getsize(pdf_path)

base = "/data/data/com.termux/files/home/jee-analysis"
files = [
    ("reports/MASTER_REPORT.md", "reports/MASTER_REPORT.pdf"),
    ("reports/mains_physics.md", "reports/mains_physics.pdf"),
    ("reports/mains_chemistry.md", "reports/mains_chemistry.pdf"),
    ("reports/mains_mathematics.md", "reports/mains_mathematics.pdf"),
    ("reports/advanced_physics.md", "reports/advanced_physics.pdf"),
    ("reports/advanced_chemistry.md", "reports/advanced_chemistry.pdf"),
    ("reports/advanced_mathematics.md", "reports/advanced_mathematics.pdf"),
]

for md_rel, pdf_rel in files:
    md_path = f"{base}/{md_rel}"
    pdf_path = f"{base}/{pdf_rel}"
    print(f"Converting {md_rel}...", end=" ")
    try:
        size = md_to_pdf(md_path, pdf_path)
        print(f"✓ {size/1024:.0f} KB")
    except Exception as e:
        print(f"✗ {e}")

# Copy to storage
os.system(f"cp {base}/reports/*.pdf /storage/emulated/0/Download/jee/reports/ 2>/dev/null")
print("\nCopied to /storage/emulated/0/Download/jee/reports/")
