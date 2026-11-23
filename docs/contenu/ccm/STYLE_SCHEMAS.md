# Style des schémas « Comment ça marche ? » (SVG)

- Un fichier par carte : assets/ccm/<id-leçon>-<n° carte>.svg (ex. CM-01-03-2.svg), n° de carte à partir de 1.
- viewBox="0 0 400 260", pas de width/height fixes, fond transparent (la carte a déjà un fond clair #F7F9FC).
- Style « schéma de vulgarisation » plat, lisible en petit sur téléphone : traits arrondis (stroke-linecap/linejoin round),
  épaisseur 3 à 4 pour les objets, 2 pour les détails. Formes simples, pas de dégradés complexes, pas de photo.
- Palette (toujours la même) :
  encre #2B3A55 (traits, texte) · bleu #3B82F6 · cyan #06B6D4 · vert #10B981 · jaune #F59E0B · rouge #EF4444 ·
  violet #8B5CF6 · gris #94A3B8 · fond d'objet #FFFFFF · surface douce #E2E8F0.
  Courant/électricité = jaune ; eau = bleu ; chaleur = rouge/orange ; froid = cyan ; danger = rouge ; ok/sécurité = vert.
- Texte dans le schéma : seulement des étiquettes courtes (1 à 4 mots), font-family="system-ui, sans-serif",
  font-size 13 à 16, font-weight 600, couleur encre. Pas de phrases (le texte est dans la carte).
- Animation quand la description en parle (flux, mouvement, étapes) : SMIL ou CSS dans le SVG
  (<animate>, <animateMotion>, stroke-dashoffset), en boucle, lente (2 à 4 s), discrète.
  Ajoute toujours un <style>@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>.
- Accessibilité : <title> court décrivant le schéma.
- Taille : moins de 6 Ko par fichier si possible. SVG valide (vérifié avec python xml.etree).
- Sécurité : ne jamais dessiner l'intérieur d'un appareil comme si on pouvait l'ouvrir pour bricoler ;
  un symbole ⚠ rouge si la description parle de danger.
- Respecte la description « schema » de la carte ET le texte de la carte : rien de faux (sens des flèches, ordre des étapes).
