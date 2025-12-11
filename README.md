# Hybrid-Analyzer — Backend (Python / FastAPI)

## 🎯 Objectif
Orchestrer :
- la classification Zero-Shot (Hugging Face — `facebook/bart-large-mnli`)
- puis une synthèse contextuelle (API Gemini)

via un endpoint sécurisé `/analyze` retournant :
- `category`
- `category_score`
- `summary`
- `tone`
- `meta` (timings + réponses brutes)

---

## 📌 Table des matières
1. Contexte
2. Stack technique
3. Arborescence
4. Prérequis
5. Variables d'environnement
6. Installation & lancement
7. Endpoints (exemples cURL)
8. Orchestration IA (HF + Gemini)
9. Authentification JWT
10. Logs & Monitoring
11. Tests (mocks HF + Gemini)
12. Documentation / livrables
13. Limitations

---

## 1. Contexte
Le backend reçoit un texte brut, appelle Hugging Face pour déterminer une catégorie, transmet cette catégorie à Gemini, consolide le tout, et renvoie un JSON structuré.  
La sécurité est assurée par JWT.

---

## 2. Stack technique
- **Python 3.11**
- **FastAPI**
- **HTTPX (async)**
- **PostgreSQL + SQLAlchemy + asyncpg**
- **Alembic**
- **JWT (PyJWT)**
- **bcrypt/passlib**
- **pytest + respx** (mocks IA)
- **Docker + docker-compose**

---

## 3. Arborescence recommandée

    backend/
    ├─ app/
    │ ├─ main.py
    │ ├─ api/v1/
    │ │ ├─ auth.py
    │ │ └─ analyze.py
    │ ├─ core/
    │ │ ├─ config.py
    │ │ ├─ security.py
    │ │ └─ logging.py
    │ ├─ db/
    │ │ ├─ models.py
    │ │ ├─ crud.py
    │ │ └─ session.py
    │ ├─ services/
    │ │ ├─ hf_client.py
    │ │ ├─ gemini_client.py
    │ │ └─ orchestrator.py
    │ ├─ schemas/
    │ └─ tests/
    ├─ alembic/
    ├─ Dockerfile
    ├─ docker-compose.yml
    ├─ requirements.txt
    └─ README.md


---

## 4. Prérequis
- Python 3.11+
- Docker & docker-compose
- Hugging Face API Key
- Gemini API Key
- PostgreSQL (dockerisé inclus)

---

## 5. Variables d'environnement `.env`
```env
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql+asyncpg://hybrid_user:securepassword@db:5432/hybrid_db

JWT_SECRET=very_secret_jwt_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

HF_API_URL=https://api-inference.huggingface.co/models/facebook/bart-large-mnli
HF_API_TOKEN=hf_xxx

GEMINI_API_URL=https://api.gemini.example/v1/generate
GEMINI_API_KEY=gemini_xxx

HF_TIMEOUT_SECONDS=10
GEMINI_TIMEOUT_SECONDS=12
REQUEST_RETRIES=2

```

## **6. Installation & lancement**
#### ▶️ Local

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    cp .env.example .env
    alembic upgrade head

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

#### ▶️ Docker
    docker-compose up --build -d
    docker-compose logs -f backend

## **7. Endpoints (exemples cURL)**
**🔐 POST /register**

    curl -X POST http://localhost:8000/api/v1/register \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"secret"}'

**🔐 POST /login**

Obtenir un JWT.

    curl -X POST http://localhost:8000/api/v1/login \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"secret"}'

🔒 POST /analyze

    curl -X POST http://localhost:8000/api/v1/analyze \
    -H "Authorization: Bearer <JWT>" \
    -H "Content-Type: application/json" \
    -d '{ "text": "Apple annonce des résultats financiers..." }'


**Réponse attendue :**

```badh
{
  "category": "Finance",
  "category_score": 0.87,
  "summary": "Résumé généré…",
  "tone": "neutre",
  "meta": {
    "hf_raw": {},
    "gemini_raw": {},
    "timings": {
      "hf_ms": 240,
      "gemini_ms": 390,
      "total_ms": 650
    }
  }
}
```

## **8. Orchestration IA — détails techniques**

### **Hugging Face**

- Zero-Shot classification

- Timeout + retries

- Score minimal configurable (0.4)

- Si score < seuil → catégorie "Incertitude"

### **Prompt Gemini (exemple)**

    Contexte: catégorie prédite = {{CATEGORY}}, score={{SCORE}}.
    Texte:
    {{TEXT}}

    Tâches :
    1) Résumé (3–5 phrases).
    2) Ton: positif|neutre|negatif.
    3) JSON strict :
    {
    "summary": "...",
    "tone": "...",
    "notes": "..."
    }

## **9. Authentification JWT**

- Hash mots de passe : bcrypt

- Token signé (HS256)

- Endpoint protégé : /analyze

## **10. Logs & Monitoring**

- Logs JSON structurés

- X-Request-ID

- Métriques internes :

- hf_latency_ms

- gemini_errors

- total_pipeline_ms

## **11. Tests (mocks HF + Gemini)**

    Lancer tests
    pytest -q

**Exemple de mock**
```bash
import respx
from httpx import Response

@respx.mock
def test_chain(client):
    respx.post("https://api-inference.huggingface.co/").mock(
        return_value=Response(200, json={
            "labels": ["Finance", "IT"],
            "scores": [0.87, 0.1]
        })
    )
    respx.post("https://api.gemini.example/").mock(
        return_value=Response(200, json={
            "summary": "...",
            "tone": "neutre",
            "notes": ""
        })
    )
```

## **13. Limitations**

- Dépendance forte aux APIs externes

- Coûts IA à surveiller

- Mode dégradé recommandé si HF/Gemini indisponibles