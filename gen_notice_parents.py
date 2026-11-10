#!/usr/bin/env python3
"""
PocketSage — Notice détaillée parents (PDF A4)
Source : docs/parents/notice_parents.html  →  guide_parents.pdf (racine, servi sur pocketsage.org/guide_parents.pdf)

Usage : python3 gen_notice_parents.py
(remplace l'ancien gen_guide_parents.py)
"""
import os, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "docs" / "parents" / "notice_parents.html"
OUT = pathlib.Path(os.environ.get("GUIDE_OUT", ROOT / "guide_parents.pdf"))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(SRC.as_uri())
    pg.wait_for_timeout(300)
    pg.pdf(path=str(OUT), format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    b.close()
print("✅ Notice parents :", OUT)
