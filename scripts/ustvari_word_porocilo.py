import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

MD_PATH = os.path.join("dokumentacija", "porocilo-o-implementaciji-s-posnetki.md")
SLIKE_DIR = os.path.join("dokumentacija", "slike")
DOCX_OUT_1 = os.path.join("dokumentacija", "Porocilo_Solski_IS_Mitja_Jancic_Nal_Dobravc.docx")
DOCX_OUT_2 = "Porocilo_Solski_IS_Mitja_Jancic_Nal_Dobravc.docx"
ARTIFACT_MD = r"C:\Users\mitja\.gemini\antigravity\brain\8c2df798-d23b-4eaa-a436-1d0a1974712d\porocilo_solski_is.md"

CAPTIONS = {
    1: "Slika 1: Shema arhitekture vsebnikov Docker Compose v skupnem omrežju (lasten vir)",
    2: "Slika 2: Konceptualni in logični ER diagram relacijske baze podatkov (lasten vir)",
    3: "Slika 3: Seznam vseh 10 predmetov z administrativnimi dejanji (lasten vir)",
    4: "Slika 4: Seznam 20 učiteljev z razvidnimi večpredmetnimi povezavami (lasten vir)",
    5: "Slika 5: Obrazec za dodeljevanje več predmetov posameznemu učitelju (lasten vir)",
    6: "Slika 6: Seznam 120 učencev z razredi (1.A–4.A) in iskalnim filtrom (lasten vir)",
    7: "Slika 7: Obrazec za vpis novega učenca z izbiro razreda in predmetnika (lasten vir)",
    8: "Slika 8: Dinamično filtriranje učencev po razredu in priimku (lasten vir)",
    9: "Slika 9: Učiteljev pregled dodeljenih predmetov in upravljanje gradiv (lasten vir)",
    10: "Slika 10: Obrazec za varno nalaganje učnega gradiva z avtorizacijo (lasten vir)",
    11: "Slika 11: Učiteljev pregled oddanih nalog s stanjem rokov (lasten vir)",
    12: "Slika 12: Vmesnik za ocenjevanje oddaje z vnosom ocene in komentarja (lasten vir)",
    13: "Slika 13: Izvoz ocen nalog v formatu CSV in pregled oddaj (lasten vir)",
    14: "Slika 14: Obrazec za samoregistracijo novega učenca (lasten vir)",
    15: "Slika 15: Urejanje lastnega profila prijavljenega učenca (lasten vir)",
    16: "Slika 16: Učenčev modul za izbiro in posodabljanje predmetov (Moji predmeti) (lasten vir)",
    17: "Slika 17: Učenčev pregled gradiv z gumbi za varen prenos (lasten vir)",
    18: "Slika 18: Učenčeva oddaja domače naloge z izbiro PDF datoteke (lasten vir)",
    19: "Slika 19: Seznam oddaj s pravilno poimenovano datoteko »Priimek Ime – Naslov naloge.pdf« (lasten vir)",
    20: "Slika 20: Opozorilo in zahtevana potrditev ob poskusu povozitve oddaje (lasten vir)",
    21: "Slika 21: Center za obvestila z rdečo značko neprebranih obvestil (lasten vir)",
    22: "Slika 22: Zavrnitev nepooblaščenega dostopa do zaščitenih pogledov (HTTP 403) (lasten vir)",
    23: "Slika 23: Prijavno okno z overitvijo v formatu »I.Priimek« (lasten vir)",
    24: "Slika 24: Baza podatkov z zgoščenimi gesli PBKDF2-SHA256 v orodju Adminer (lasten vir)",
    25: "Slika 25: Status vseh 5 delujočih Docker vsebnikov (docker compose ps) (lasten vir)",
    26: "Slika 26: Javna domena z veljavnim HTTPS potrdilom v brskalniku (lasten vir)",
    27: "Slika 27: Odzivni mobilni prikaz aplikacije s temnim načinom (lasten vir)",
    28: "Slika 28: Združeni vlečni zahtevki (Pull Requests) in veje na GitHubu (lasten vir)",
    29: "Slika 29: Uspešna izvedba vseh 26 avtomatiziranih testov v terminalu (lasten vir)",
}


def update_markdown():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace Slika 1 and Slika 2 placeholders with embedded images too
    for idx in range(1, 30):
        img_rel = f"slike/slika_{idx:02d}.png"
        marker = f"![Slika {idx}]({img_rel})"
        if marker in text:
            continue

        if idx in (1, 2):
            target = f"*Slika {idx}:"
            if target in text:
                text = text.replace(target, f"![Slika {idx}]({img_rel})\n\n*Slika {idx}:", 1)
        else:
            # Find Podnapis line for Slika idx
            pattern = rf"(\*Podnapis:\*\s*\*\*Slika {idx}:[^\n]+\*\*)"
            replacement = rf"\1\n\n![Slika {idx}]({img_rel})"
            text = re.sub(pattern, replacement, text, count=1)

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated Markdown file: {MD_PATH}")


def add_image_with_caption(doc, idx):
    img_path = os.path.join(SLIKE_DIR, f"slika_{idx:02d}.png")
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run()
        width = Inches(3.2) if idx == 27 else Inches(6.0)
        run_img.add_picture(img_path, width=width)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run(CAPTIONS[idx])
        run_cap.italic = True
        run_cap.font.size = Pt(10)
        run_cap.font.color.rgb = RGBColor(80, 80, 80)


def build_docx():
    doc = Document()

    # Set default font
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    # --- NASLOVNA STRAN ---
    p_school = doc.add_paragraph()
    p_school.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sc = p_school.add_run("ŠOLSKI CENTER CELJE\nSrednja šola za kemijo, elektrotehniko in računalništvo\nProgram: Tehnik računalništva")
    r_sc.font.size = Pt(13)
    r_sc.bold = True

    for _ in range(4):
        doc.add_paragraph()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("ŠOLSKI INFORMACIJSKI SISTEM (Šolski IS+)\n")
    r_t.font.size = Pt(22)
    r_t.bold = True
    r_t.font.color.rgb = RGBColor(13, 110, 253)

    r_sub = p_title.add_run("Zaključno poročilo o izvedbi projekta in implementaciji vseh kriterijev")
    r_sub.font.size = Pt(14)
    r_sub.italic = True

    for _ in range(5):
        doc.add_paragraph()

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_m = p_meta.add_run(
        "Avtorja: Mitja Jančič, Nal Dobravc\n"
        "Razred: 4. A\n"
        "Mentor: prof. Matic Holobar\n"
        "Repozitorij: https://github.com/MitjaJancic/solski_sistem\n"
        "Kraj in datum: Celje, november 2026"
    )
    r_m.font.size = Pt(11)

    doc.add_page_break()

    # Parse markdown lines and build structured document
    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_code = False
    for raw_line in lines:
        line = raw_line.rstrip("\n")

        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        # Check for embedded image syntax ![Slika X](...)
        m_img = re.match(r"^!\[Slika (\d+)\]\(", line)
        if m_img:
            idx = int(m_img.group(1))
            add_image_with_caption(doc, idx)
            continue

        # Skip duplicate manual caption lines if image already adds it
        if line.startswith("*Slika 1:") or line.startswith("*Slika 2:"):
            continue
        if "*Podnapis:*" in line:
            continue

        if line.startswith("# "):
            continue  # Already on title page
        elif line.startswith("## "):
            h_text = line[3:].strip()
            if h_text.startswith("Poročilo o izvedbi"):
                continue
            doc.add_heading(h_text, level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=2)
        elif line.startswith("---"):
            continue
        elif line.startswith("- ") or line.startswith("  - "):
            clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", line.lstrip(" -"))
            clean = re.sub(r"\*([^*]+)\*", r"\1", clean)
            clean = clean.replace("`", "")
            doc.add_paragraph(clean, style="List Bullet")
        elif re.match(r"^\d+\.\s", line):
            clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
            clean = clean.replace("`", "")
            doc.add_paragraph(clean, style="List Number")
        elif line.strip():
            clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", line.strip())
            clean = re.sub(r"\*([^*]+)\*", r"\1", clean)
            clean = clean.replace("`", "")
            doc.add_paragraph(clean)

    doc.save(DOCX_OUT_1)
    doc.save(DOCX_OUT_2)
    print(f"Saved Word reports:\n  - {DOCX_OUT_1}\n  - {DOCX_OUT_2}")


if __name__ == "__main__":
    update_markdown()
    build_docx()
