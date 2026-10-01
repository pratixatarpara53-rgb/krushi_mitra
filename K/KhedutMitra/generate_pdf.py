"""
Generate a professional PDF report for KhedutMitra website.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.colors import HexColor
from app import CROPS, TIPS, CALENDAR

# ── Colors ──────────────────────────────────────────────────────────────────
GREEN_DARK  = HexColor("#1a5c33")
GREEN       = HexColor("#2d8a4e")
GREEN_LIGHT = HexColor("#e8f5ee")
GOLD        = HexColor("#c8952a")
GOLD_LIGHT  = HexColor("#fff8e6")
CREAM       = HexColor("#faf7f0")
WHITE       = colors.white
BLACK       = HexColor("#1a2b1e")
GREY        = HexColor("#6b8c74")
BORDER      = HexColor("#d4e8da")

W, H = A4  # 595 x 842 pts

OUTPUT = os.path.join(os.path.dirname(__file__), "KhedutMitra_Website.pdf")

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def s(name, **kw):
    return ParagraphStyle(name, **kw)

COVER_TITLE = s("CoverTitle", fontSize=36, textColor=WHITE,
                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=44)
COVER_SUB   = s("CoverSub",   fontSize=14, textColor=HexColor("#a8f0c0"),
                fontName="Helvetica", alignment=TA_CENTER, leading=20)
COVER_TAG   = s("CoverTag",   fontSize=10, textColor=WHITE,
                fontName="Helvetica", alignment=TA_CENTER)

H1 = s("H1", fontSize=22, textColor=WHITE, fontName="Helvetica-Bold",
        alignment=TA_CENTER, leading=28)
H2 = s("H2", fontSize=15, textColor=GREEN_DARK, fontName="Helvetica-Bold",
        leading=20, spaceAfter=4)
H3 = s("H3", fontSize=12, textColor=GREEN, fontName="Helvetica-Bold",
        leading=16, spaceAfter=2)
BODY = s("Body2", fontSize=10, textColor=BLACK, fontName="Helvetica",
         leading=15, alignment=TA_JUSTIFY)
BODY_C = s("BodyC", fontSize=10, textColor=BLACK, fontName="Helvetica",
           leading=15, alignment=TA_CENTER)
SMALL = s("Small", fontSize=8.5, textColor=GREY, fontName="Helvetica", leading=13)
BULLET = s("Bullet", fontSize=10, textColor=BLACK, fontName="Helvetica",
           leading=15, leftIndent=14, bulletIndent=4)
LABEL = s("Label", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold",
          alignment=TA_CENTER)

def colored_box(text, style, bg, w, h=0.7*cm, radius=4):
    return Table([[Paragraph(text, style)]],
                 colWidths=[w], rowHeights=[h],
                 style=TableStyle([
                     ("BACKGROUND", (0,0), (-1,-1), bg),
                     ("ROUNDEDCORNERS", [radius]),
                     ("LEFTPADDING",  (0,0), (-1,-1), 6),
                     ("RIGHTPADDING", (0,0), (-1,-1), 6),
                     ("TOPPADDING",   (0,0), (-1,-1), 4),
                     ("BOTTOMPADDING",(0,0), (-1,-1), 4),
                 ]))

def section_header(title, bg=GREEN):
    return Table([[Paragraph(title, H1)]],
                 colWidths=[W - 4*cm],
                 style=TableStyle([
                     ("BACKGROUND",   (0,0), (-1,-1), bg),
                     ("ROUNDEDCORNERS", [8]),
                     ("TOPPADDING",    (0,0), (-1,-1), 10),
                     ("BOTTOMPADDING", (0,0), (-1,-1), 10),
                     ("LEFTPADDING",   (0,0), (-1,-1), 16),
                     ("RIGHTPADDING",  (0,0), (-1,-1), 16),
                 ]))

def hr(color=BORDER, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=6)

# ── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm,  bottomMargin=2*cm,
    title="KhedutMitra – Smart Farming Guide",
    author="KhedutMitra",
    subject="Agricultural Information Website"
)

story = []

# ═══════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════
cover_bg = Table(
    [[Paragraph("🌾 KhedutMitra", COVER_TITLE)],
     [Spacer(1, 0.3*cm)],
     [Paragraph("Smart Farming Guide", COVER_SUB)],
     [Spacer(1, 0.5*cm)],
     [Paragraph("Complete Website Documentation & Crop Information", COVER_TAG)],
     [Spacer(1, 0.4*cm)],
     [Paragraph("Python Flask  •  HTML5  •  CSS3  •  JavaScript", COVER_TAG)],
    ],
    colWidths=[W - 4*cm],
    style=TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), GREEN_DARK),
        ("ROUNDEDCORNERS",[12]),
        ("TOPPADDING",    (0,0), (-1,-1), 40),
        ("BOTTOMPADDING", (0,0), (-1,-1), 40),
        ("LEFTPADDING",   (0,0), (-1,-1), 30),
        ("RIGHTPADDING",  (0,0), (-1,-1), 30),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ])
)
story.append(Spacer(1, 1*cm))
story.append(cover_bg)
story.append(Spacer(1, 1*cm))

# Stats row on cover
stats = [
    ["8+\nCrops", "6\nFarming Guides", "4\nSoil Types", "3\nSeasons"],
]
stats_table = Table(stats, colWidths=[(W-4*cm)/4]*4,
    style=TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), GREEN_LIGHT),
        ("TEXTCOLOR",     (0,0), (-1,-1), GREEN_DARK),
        ("FONTNAME",      (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 13),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [GREEN_LIGHT]),
        ("ROUNDEDCORNERS",[8]),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("GRID",          (0,0), (-1,-1), 1, BORDER),
    ]))
story.append(stats_table)
story.append(Spacer(1, 0.8*cm))

# Pages overview
pages_data = [
    ["Page", "URL", "Description"],
    ["Home",         "/",              "Hero section, stats, featured crops, features"],
    ["Crop Guide",   "/crops",         "8 crop cards with live JavaScript search"],
    ["Crop Details", "/crops/<id>",    "Soil, irrigation, growth stages, farming tips"],
    ["Farming Tips", "/tips",          "6 step-by-step farming guide cards"],
    ["Crop Calendar","/calendar",      "Kharif, Rabi, Zaid seasonal calendar"],
]
pages_table = Table(pages_data,
    colWidths=[3.2*cm, 4*cm, (W-4*cm)-7.2*cm],
    style=TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  GREEN_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREEN_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("ALIGN",         (0,0), (-1,0),  "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
story.append(Paragraph("Website Pages", H2))
story.append(pages_table)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════
# CROP GUIDE SECTION
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("🌾  Crop Guide"))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "Detailed information on 8 major crops grown in Gujarat and across India — "
    "covering season, soil type, irrigation needs, growth stages, harvesting, and key farming tips.",
    BODY))
story.append(Spacer(1, 0.5*cm))

for i, crop in enumerate(CROPS):
    d = crop["details"]
    season_color = GREEN if "Kharif" in crop["season"] else GOLD

    # Crop header bar
    header_row = Table(
        [[Paragraph(f"<b>{crop['name']}</b>  <font size='10' color='#6b8c74'>{crop['gujarati']}</font>", H2),
          colored_box(crop["season"], LABEL, season_color, 3*cm)]],
        colWidths=[W-4*cm-3.5*cm, 3.5*cm],
        style=TableStyle([
            ("VALIGN",  (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN",   (1,0), (1,0),   "RIGHT"),
        ])
    )
    story.append(KeepTogether([
        header_row,
        hr(GREEN_LIGHT, 1.5),
        Paragraph(crop["short_desc"], BODY),
        Spacer(1, 0.2*cm),
    ]))

    # 2-column info
    info_data = [
        [Paragraph("<b>Soil Type</b>", H3),      Paragraph("<b>Suitable Season</b>", H3)],
        [Paragraph(crop["soil"], BODY),           Paragraph(d["suitable_season"], BODY)],
        [Spacer(1,0.2*cm), Spacer(1,0.2*cm)],
        [Paragraph("<b>Irrigation</b>", H3),      Paragraph("<b>Harvesting</b>", H3)],
        [Paragraph(d["irrigation"], BODY),        Paragraph(d["harvesting"], BODY)],
    ]
    info_table = Table(info_data,
        colWidths=[(W-4*cm)/2]*2,
        style=TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
    story.append(info_table)
    story.append(Spacer(1, 0.2*cm))

    # Growth stages
    stages_text = "  →  ".join(d["growth_stages"])
    story.append(Paragraph("<b>Growth Stages:</b>", H3))
    story.append(Paragraph(stages_text, SMALL))
    story.append(Spacer(1, 0.15*cm))

    # Tips
    story.append(Paragraph("<b>Farming Tips:</b>", H3))
    for tip in d["tips"]:
        story.append(Paragraph(f"• {tip}", BULLET))

    story.append(Spacer(1, 0.4*cm))
    if i < len(CROPS) - 1:
        story.append(hr(BORDER, 0.5))
        story.append(Spacer(1, 0.3*cm))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════
# FARMING TIPS SECTION
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("💡  Farming Tips"))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "Practical, step-by-step guidance covering every major stage of the farming cycle.",
    BODY))
story.append(Spacer(1, 0.5*cm))

for tip in TIPS:
    tip_header = Table(
        [[Paragraph(f"{tip['icon']}  {tip['title']}", H2)]],
        colWidths=[W-4*cm],
        style=TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), GREEN_LIGHT),
            ("ROUNDEDCORNERS",[6]),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ])
    )
    story.append(KeepTogether([
        tip_header,
        Spacer(1, 0.2*cm),
        Paragraph(tip["summary"], BODY),
        Spacer(1, 0.15*cm),
    ]))
    for point in tip["points"]:
        story.append(Paragraph(f"→  {point}", BULLET))
    story.append(Spacer(1, 0.4*cm))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════
# CROP CALENDAR SECTION
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("📅  Crop Calendar"))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "Plan your farming year using the Kharif, Rabi, and Zaid seasonal calendar.",
    BODY))
story.append(Spacer(1, 0.5*cm))

# Monthly strip
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
season_map = {
    "Jun":"Kharif","Jul":"Kharif","Aug":"Kharif","Sep":"Kharif","Oct":"Kharif","Nov":"Kharif",
    "Dec":"Rabi","Jan":"Rabi","Feb":"Rabi","Mar":"Rabi",
    "Apr":"Zaid","May":"Zaid",
}
season_colors = {"Kharif": GREEN, "Rabi": GOLD, "Zaid": HexColor("#c0522a")}
month_row = [[Paragraph(f"<b>{m}</b>", s("ml", fontSize=8, textColor=WHITE,
              fontName="Helvetica-Bold", alignment=TA_CENTER)) for m in months]]
month_colors = [season_colors[season_map[m]] for m in months]
month_table = Table(month_row,
    colWidths=[(W-4*cm)/12]*12,
    rowHeights=[1*cm],
    style=TableStyle(
        [("BACKGROUND", (i,0), (i,0), month_colors[i]) for i in range(12)] +
        [("ALIGN",         (0,0), (-1,-1), "CENTER"),
         ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
         ("GRID",          (0,0), (-1,-1), 0.5, WHITE),
         ("ROUNDEDCORNERS",[4]),
        ]
    ))
story.append(month_table)
story.append(Spacer(1, 0.2*cm))

# Legend
legend_data = [[
    colored_box("  Kharif  ", LABEL, GREEN, 2.5*cm, 0.5*cm),
    Spacer(0.3*cm, 0),
    colored_box("  Rabi  ",   LABEL, GOLD,  2.5*cm, 0.5*cm),
    Spacer(0.3*cm, 0),
    colored_box("  Zaid  ",   LABEL, HexColor("#c0522a"), 2.5*cm, 0.5*cm),
]]
story.append(Table([legend_data[0]], colWidths=[2.5*cm,0.3*cm,2.5*cm,0.3*cm,2.5*cm],
    style=TableStyle([("ALIGN",(0,0),(-1,-1),"LEFT"),("VALIGN",(0,0),(-1,-1),"MIDDLE")])))
story.append(Spacer(1, 0.5*cm))

for season_name, season in CALENDAR.items():
    sc = HexColor(season["color"])
    head = Table([[Paragraph(f"<b>{season_name} Season</b>  —  {season['period']}", H2)]],
        colWidths=[W-4*cm],
        style=TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), sc),
            ("ROUNDEDCORNERS",[6]),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 12),
            ("TEXTCOLOR",     (0,0), (-1,-1), WHITE),
        ])
    )
    story.append(KeepTogether([
        head,
        Spacer(1, 0.2*cm),
        Paragraph(season["description"], BODY),
        Spacer(1, 0.15*cm),
        Paragraph("<b>Example Crops:</b>  " + "  •  ".join(season["crops"]), SMALL),
        Spacer(1, 0.15*cm),
        Paragraph("<b>Key Activities:</b>", H3),
    ]))
    for act in season["key_activities"]:
        story.append(Paragraph(f"→  {act}", BULLET))
    story.append(Spacer(1, 0.4*cm))

# ── Footer note ──────────────────────────────────────────────────────────────
story.append(PageBreak())
footer_box = Table(
    [[Paragraph("🌾 KhedutMitra – Smart Farming Guide", s("ft", fontSize=14,
                textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))],
     [Paragraph("Educational farming information for students and farmers.<br/>"
                "Built with Python Flask · HTML5 · CSS3 · JavaScript<br/>"
                "© 2024 KhedutMitra – Educational Use Only",
                s("fb", fontSize=10, textColor=HexColor("#a8f0c0"),
                  fontName="Helvetica", alignment=TA_CENTER, leading=16))]],
    colWidths=[W-4*cm],
    style=TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), GREEN_DARK),
        ("ROUNDEDCORNERS",[10]),
        ("TOPPADDING",    (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 20),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ])
)
story.append(Spacer(1, 3*cm))
story.append(footer_box)

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved: {OUTPUT}")
