"""
docs/SUNUM_MAKINELER.md  →  docs/SUNUM_MAKINELER.pdf
"""
import re
from pathlib import Path
from fpdf import FPDF

# ── renk paleti ────────────────────────────────────────────────
C_BLACK  = (30,  30,  30)
C_H1     = (26,  26,  46)
C_H2     = (44,  95, 138)
C_BQ_BG  = (240, 246, 255)
C_BQ_BAR = (74, 144, 217)
C_CODE   = (244, 244, 244)
C_PRE_BG = (30,  30,  46)
C_PRE_FG = (205, 214, 244)
C_TH_BG  = (44,  95, 138)
C_TH_FG  = (255, 255, 255)
C_TR_ALT = (248, 248, 248)
C_HR     = (200, 200, 200)

FONT_DIR = Path(__file__).parent.parent / "scripts"

class PDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*C_H2)
        self.cell(0, 6, f"TuringLab Sunum Rehberi — sayfa {self.page_no()}", align="C")

def strip_inline(text):
    """Remove **bold** and `code` markers for plain text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text

def render_inline(pdf, text, base_size=10):
    """Render a line with inline bold and code spans."""
    parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            pdf.set_font("Helvetica", "B", base_size)
            pdf.set_text_color(*C_H2)
            pdf.write(5, part[2:-2])
            pdf.set_font("Helvetica", "", base_size)
            pdf.set_text_color(*C_BLACK)
        elif part.startswith('`') and part.endswith('`'):
            pdf.set_font("Courier", "", base_size - 0.5)
            pdf.set_fill_color(*C_CODE)
            pdf.write(5, part[1:-1])
            pdf.set_font("Helvetica", "", base_size)
            pdf.set_text_color(*C_BLACK)
        else:
            pdf.write(5, part)

def main():
    md_path = Path("docs/SUNUM_MAKINELER.md")
    out_path = Path("docs/SUNUM_MAKINELER.pdf")
    lines = md_path.read_text(encoding="utf-8").split("\n")

    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(18, 18, 18)

    W = pdf.w - 36  # usable width

    in_pre   = False
    in_bq    = False
    in_table = False
    table_header_done = False
    row_idx  = 0

    def end_bq():
        nonlocal in_bq
        if in_bq:
            pdf.ln(2)
            in_bq = False

    def end_table():
        nonlocal in_table, table_header_done, row_idx
        if in_table:
            pdf.ln(3)
            in_table = False
            table_header_done = False
            row_idx = 0

    for raw in lines:
        line = raw.rstrip()

        # ── fenced code block ──────────────────────────────────
        if line.strip().startswith("```"):
            if not in_pre:
                end_bq(); end_table()
                in_pre = True
                pdf.set_fill_color(*C_PRE_BG)
                pdf.set_text_color(*C_PRE_FG)
                pdf.set_font("Courier", "", 8)
                pdf.ln(2)
            else:
                in_pre = False
                pdf.ln(2)
                pdf.set_text_color(*C_BLACK)
            continue

        if in_pre:
            pdf.set_x(18)
            txt = line if line else " "
            pdf.set_fill_color(*C_PRE_BG)
            pdf.multi_cell(W, 4.5, txt, fill=True, new_x="LMARGIN", new_y="NEXT")
            continue

        # ── hr ─────────────────────────────────────────────────
        if re.match(r'^-{3,}$', line.strip()):
            end_bq(); end_table()
            pdf.ln(2)
            pdf.set_draw_color(*C_HR)
            pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y())
            pdf.ln(4)
            continue

        # ── headings ───────────────────────────────────────────
        if line.startswith("# "):
            end_bq(); end_table()
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(*C_H1)
            pdf.set_draw_color(*C_BQ_BAR)
            pdf.multi_cell(W, 8, strip_inline(line[2:]), new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(*C_HR)
            pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y())
            pdf.ln(3)
            pdf.set_text_color(*C_BLACK)
            continue

        if line.startswith("## "):
            end_bq(); end_table()
            pdf.ln(3)
            # left bar
            y = pdf.get_y()
            pdf.set_fill_color(*C_BQ_BAR)
            pdf.rect(18, y, 1.5, 7, style="F")
            pdf.set_xy(21, y)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(*C_H2)
            pdf.multi_cell(W - 3, 7, strip_inline(line[3:]), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            pdf.set_text_color(*C_BLACK)
            continue

        if line.startswith("### "):
            end_bq(); end_table()
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(*C_H2)
            pdf.multi_cell(W, 6, strip_inline(line[4:]), new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(*C_BLACK)
            continue

        # ── table ──────────────────────────────────────────────
        if line.startswith("|"):
            end_bq()
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.match(r'^[-:]+$', c) for c in cells if c):
                table_header_done = True
                continue
            col_w = W / max(len(cells), 1)
            if not table_header_done:
                in_table = True
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_fill_color(*C_TH_BG)
                pdf.set_text_color(*C_TH_FG)
                for c in cells:
                    pdf.cell(col_w, 7, strip_inline(c), border=1, fill=True)
                pdf.ln()
                row_idx = 0
            else:
                in_table = True
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(*C_BLACK)
                if row_idx % 2 == 0:
                    pdf.set_fill_color(*C_TR_ALT)
                else:
                    pdf.set_fill_color(255, 255, 255)
                for c in cells:
                    pdf.cell(col_w, 6, strip_inline(c), border=1, fill=True)
                pdf.ln()
                row_idx += 1
            continue
        else:
            end_table()

        # ── blockquote ─────────────────────────────────────────
        if line.startswith("> ") or line == ">":
            content = line[2:] if line.startswith("> ") else ""
            if not in_bq:
                in_bq = True
                pdf.ln(1)
                pdf.set_fill_color(*C_BQ_BG)
            # bar + background
            y = pdf.get_y()
            pdf.set_fill_color(*C_BQ_BAR)
            pdf.rect(18, y, 1.5, 5.5, style="F")
            pdf.set_fill_color(*C_BQ_BG)
            pdf.rect(19.5, y, W - 1.5, 5.5, style="F")
            pdf.set_xy(22, y)
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(*C_BLACK)
            if content:
                render_inline(pdf, strip_inline(content), base_size=9.5)
            pdf.ln(5.5)
            continue
        else:
            end_bq()

        # ── empty line ─────────────────────────────────────────
        if line.strip() == "":
            pdf.ln(2)
            continue

        # ── normal paragraph ───────────────────────────────────
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*C_BLACK)
        pdf.set_x(18)
        # multi_cell with inline styling (simplified: strip markers)
        pdf.multi_cell(W, 5.5, strip_inline(line), new_x="LMARGIN", new_y="NEXT")

    end_bq()
    end_table()

    pdf.output(str(out_path))
    print(f"Kaydedildi: {out_path}")

if __name__ == "__main__":
    main()
