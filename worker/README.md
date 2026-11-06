# Worker proxy ElevenLabs (onglet Nuit)

Ce petit serveur Cloudflare garde la clé ElevenLabs à l'abri : la page publique l'appelle, lui seul parle à ElevenLabs.

## Mise en place (une seule fois)

1. Dans ElevenLabs : **régénère la clé** (l'ancienne a été publique) et mets un **plafond de dépense**.
2. Dans un terminal, depuis ce dossier `worker/` :
   ```
   npx wrangler login
   npx wrangler secret put ELEVEN_API_KEY     # colle la NOUVELLE clé quand on te la demande
   npx wrangler deploy
   ```
3. Wrangler affiche l'adresse du Worker (du type `https://pocketsage-tts.xxxx.workers.dev`).
4. Dans `index.html`, remplace `https://REMPLACER-PAR-URL-DU-WORKER` par cette adresse, puis publie.

## Ce que ça protège

- Clé ElevenLabs jamais visible dans la page.
- Seul `pocketsage.org` est accepté (origine vérifiée), voix et modèle fixés côté serveur.
- Texte limité à 3000 caractères, 20 appels par minute et par IP.
- Ce n'est pas une barrière absolue (l'origine peut être imitée hors navigateur) : garde le plafond de dépense ElevenLabs et une alerte d'usage.
