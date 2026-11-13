#!/usr/bin/env python3
"""PocketSage — Présentation du jeu Mon Monde (PDF paysage)
Source : docs/jeux/presentation/presentation_mon_monde.html → docs/jeux/presentation/Mon_Monde_presentation.pdf
Usage : python3 gen_presentation_monde.py"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/"docs"/"jeux"/"presentation"/"presentation_mon_monde.html"
OUT=ROOT/"docs"/"jeux"/"presentation"/"Mon_Monde_presentation.pdf"
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto(SRC.as_uri());pg.wait_for_timeout(500)
    pg.pdf(path=str(OUT),width="297mm",height="167mm",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"});b.close()
print("✅",OUT)
