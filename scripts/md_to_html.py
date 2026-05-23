import re
from pathlib import Path

md = Path("docs/SUNUM_MAKINELER.md").read_text(encoding="utf-8")

STYLE = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       max-width: 800px; margin: 0 auto; padding: 16px; line-height: 1.75; color: #222; }
h1 { color: #1a1a2e; border-bottom: 2px solid #4a90d9; padding-bottom: 8px; }
h2 { color: #2c5f8a; margin-top: 2em; border-left: 4px solid #4a90d9; padding-left: 12px; }
blockquote { background: #f0f6ff; border-left: 4px solid #4a90d9;
             margin: 8px 0; padding: 10px 16px; border-radius: 4px; }
blockquote p { margin: 4px 0; }
code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.88em; font-family: monospace; }
pre { background: #1e1e2e; color: #cdd6f4; padding: 14px; border-radius: 6px; overflow-x: auto; }
pre code { background: none; color: inherit; padding: 0; font-size: 0.88em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
th { background: #2c5f8a; color: white; }
tr:nth-child(even) { background: #f8f8f8; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
strong { color: #1a5276; }
p { margin: 0.5em 0; }
"""

def inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

lines = md.split("\n")
out = [f"<!DOCTYPE html>\n<html lang='tr'>\n<head>\n<meta charset='UTF-8'>\n"
       f"<meta name='viewport' content='width=device-width,initial-scale=1'>\n"
       f"<title>TuringLab Sunum Rehberi</title>\n<style>{STYLE}</style>\n</head>\n<body>"]

in_pre = False
in_bq = False
in_table = False

i = 0
while i < len(lines):
    line = lines[i]

    if line.strip().startswith("```"):
        if not in_pre:
            in_pre = True
            out.append("<pre><code>")
        else:
            in_pre = False
            out.append("</code></pre>")
        i += 1
        continue

    if in_pre:
        out.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        i += 1
        continue

    if re.match(r"^-{3,}$", line.strip()):
        if in_bq: out.append("</blockquote>"); in_bq = False
        if in_table: out.append("</table>"); in_table = False
        out.append("<hr>"); i += 1; continue

    if line.startswith("# "):
        out.append(f"<h1>{inline(line[2:])}</h1>"); i += 1; continue
    if line.startswith("## "):
        out.append(f"<h2>{inline(line[3:])}</h2>"); i += 1; continue
    if line.startswith("### "):
        out.append(f"<h3>{inline(line[4:])}</h3>"); i += 1; continue

    if line.startswith("|"):
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.match(r"^[-:]+$", c) for c in cells if c):
            i += 1; continue
        if not in_table:
            in_table = True
            out.append("<table>")
            out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
        else:
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
        i += 1; continue
    else:
        if in_table:
            out.append("</table>"); in_table = False

    if line.startswith("> ") or line == ">":
        content = line[2:] if line.startswith("> ") else ""
        if not in_bq:
            in_bq = True; out.append("<blockquote>")
        if content:
            out.append(f"<p>{inline(content)}</p>")
        i += 1; continue
    else:
        if in_bq:
            out.append("</blockquote>"); in_bq = False

    if line.strip() == "":
        i += 1; continue

    out.append(f"<p>{inline(line)}</p>")
    i += 1

if in_bq: out.append("</blockquote>")
if in_table: out.append("</table>")
if in_pre: out.append("</code></pre>")
out.append("</body></html>")

Path("docs/SUNUM_MAKINELER.html").write_text("\n".join(out), encoding="utf-8")
print("Kaydedildi: docs/SUNUM_MAKINELER.html")
