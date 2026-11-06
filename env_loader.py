"""Lecture des clés secrètes pour les scripts de génération audio.

Les clés ne sont JAMAIS écrites dans le code. Elles viennent :
  1. des variables d'environnement, ou
  2. du fichier `.env` placé à la racine du projet (ignoré par git).

Voir `.env.example` pour la liste des noms attendus.
"""
import os
import sys
from pathlib import Path

_ENV_FILE = Path(__file__).resolve().parent / ".env"


def _load_env_file():
    if not _ENV_FILE.exists():
        return
    for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        # une variable déjà définie dans l'environnement garde la priorité
        os.environ.setdefault(name.strip(), value)


_load_env_file()


def get(name, required=True):
    """Retourne la valeur de `name`, ou arrête le script avec un message clair."""
    value = os.environ.get(name, "").strip()
    if not value and required:
        sys.exit(
            f"❌ Clé manquante : {name}\n"
            f"   Ajoute-la dans le fichier .env (voir .env.example) puis relance."
        )
    return value
