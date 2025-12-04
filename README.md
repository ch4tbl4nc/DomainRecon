# DomainRecon

> Outil OSINT pour la reconnaissance de domaines — interface web conteneurisée

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Description

`DomainRecon` est une petite application web qui automatise la collecte d'informations publiques sur un domaine :

- Résolution DNS (adresses IP)
- Relevé des headers HTTP et contrôles basiques de sécurité
- Récupération des données DomainRecon (registrar, dates, serveurs DNS)
- Persistance des résultats dans une base de données PostgreSQL

L'application se compose d'un backend (`FastAPI`) exposant une API pour lancer des scans et consulter l'historique, et d'un frontend statique servi par `nginx`.

---

## 🛠️ Stack technique

- Backend : `FastAPI` (+ SQLAlchemy pour la persistance)
- Base de données : `PostgreSQL`
- Frontend : HTML + JavaScript (serveur `nginx` dans le conteneur frontend)
- Conteneurisation : `Docker` + `docker-compose`

---

## 🚀 Installation et exécution

### Prérequis

- Docker et Docker Compose installés sur la machine.

### Lancer via Docker Compose (recommandé)

Ouvrir un terminal (PowerShell) à la racine du dépôt puis :

```powershell
git clone https://github.com/ch4tbl4nc/DomainRecon.git
cd DomainRecon
# Copier le fichier d'exemple d'environnement si nécessaire
copy .env.example .env

# Construire et lancer les services
docker-compose up --build
```

Par défaut, les services exposent :

- Frontend : http://localhost
- API : http://localhost:8000
- Documentation (Swagger) : http://localhost:8000/docs

> Remarque : si un port est déjà pris, adaptez `docker-compose.yml` ou arrêtez le service concurrent.

### Exécution locale du backend (sans Docker)

Si vous souhaitez exécuter seulement le backend en local pour développement :

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Lancer le serveur (supposant que l'app expose l'objet FastAPI `app` dans `app/main.py`)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📁 Structure du projet

```
DomainRecon/
├── docker-compose.yml
├── .env.example
├── LICENSE
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       └── scanner.py
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    └── index.html
```

---

## 🔌 API (principales routes)

- `POST /scan` : lancer un scan pour un domaine (payload JSON: `{ "domain": "example.com" }`).
- `GET /history` : récupérer l'historique des scans.
- `GET /scan/{id}` : récupérer les détails d'un scan par son identifiant.
- `GET /health` : état de santé de l'API.

Exemple (curl) :

```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

---

## 📝 Contribution

- Ouvrez une issue pour proposer une amélioration ou signaler un bug.
- Faites une branche, ajoutez des tests si possible, et soumettez une pull request.

---

## ⚖️ Licence

Ce projet est distribué sous la licence MIT — voir le fichier `LICENSE`.

---

Si vous voulez que je précise des exemples d'usage, que j'ajoute des captures d'écran ou que j'adapte les instructions Windows/Mac, dites-le et je mets à jour le `README.md`.
