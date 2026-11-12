# Sciences & Nature / Logique — classes (12/11/2026)

- Plus de curseur d'âge (son étiquette ne suivait pas le bouton, et il mélangeait les classes) → **3 choix** : ↩️ Réviser (classe d'en dessous) · 🎯 Ma classe (selon l'âge du profil, présélectionnée) · 🚀 En avance (classe au-dessus). GS : pas de « Réviser » ; Lycée / adultes : pas de « En avance ».
- Âge → classe : ≤5 GS · 6 CP · 7 CE1 · 8 CE2 · 9 CM1 · 10 CM2 · 11 6ème · 12 5ème · 13 4ème · 14 3ème · 15+ Lycée (`_profClasse`, `CLASS_MODS` dans index.html).
- Les sous-menus sans question pour la classe choisie sont masqués (ex. Logique au lycée : seulement Suites et Labyrinthes).
- Curseur des autres modules (Ateliers, Flash, Histoires…) : l'âge affiché suit maintenant le bouton.
- ⚠️ À revoir : certaines questions sont mal classées (ex. en « 3ème » : théorème de Bayes, rang d'une matrice → niveau lycée/supérieur). Prévoir une relecture du classement. Logique a très peu de contenu au lycée (10 questions).
- ✅ 13/11 : en changeant de classe (ou de niveau, d'âge, de groupe), on **reste sur le sous-menu choisi** (Intrus reste Intrus, Histoire reste Histoire, Espagnol reste Espagnol) — fonction `_restoreTab`, pour tous les modules.
- ✅ 13/11 : onglet **Tables** filtré aussi par la classe choisie : méthodes (Bâtonnets 6-9, Perles 4-8, Pythagore 7-10, Histoires 7-11, Trachtenberg 10-15, Flash 8-15) et tables ×N (8+, 9+, 10+) affichées seulement si elles conviennent à l'âge de la classe ; si la méthode choisie n'existe pas pour cette classe, on bascule sur la première disponible.
