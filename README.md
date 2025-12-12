# 🚀 API Hybrid-Analyzer : Orchestration d'Intelligence Artificielle

## 🎯 Objectif du Projet

Cette API Python est le cœur sécurisé et fiable de l'application Hybrid-Analyzer. Elle orchestre la classification Zero-Shot d'Hugging Face et l'analyse contextuelle de l'API Gemini pour transformer le texte brut en données structurées.

## 🛠️ Stack Technique

- **Backend** : Python (FastAPI / Flask)
- **Base de Données** : PostgreSQL
- **Sécurité** : JWT, `bcrypt`
- **Services IA** : Hugging Face Inference API (`facebook/bart-large-mnli`) & Google Gemini API

## 📂 Structure du Dépôt

| Dossier | Rôle |
|---------|------|
| `api` | Points d'entrée (routes `/analyze`, `/login`, etc.) |
| `core` | Logique métier et configuration globale |
| `db` | Gestion de la persistance (modèles PostgreSQL) |
| `services` | Modules d'intégration des APIs externes (Hugging Face, Gemini) |
| `tests` | Tests unitaires avec mocks des APIs IA |
| `utils` | Fonctions utilitaires (sécurité, logging) |

## 🖼️ Schéma d'Architecture

Le Backend sert de passerelle unique, protégeant l'accès (JWT) et gérant la complexité des appels externes.

## 🔄 Workflow d'Analyse Détaillé

Le processus est exécuté séquentiellement et de manière transactionnelle via l'endpoint protégé `/analyze` :

1. **Réception du Texte** : Le Backend reçoit le texte, valide le token JWT et effectue la journalisation initiale.
2. **Appel Hugging Face (Classification)** : Le texte est envoyé au modèle Zero-Shot. Le Backend attend la réponse pour la catégorie et le score.
3. **Vérification & Contextualisation** : Si la classification HF est réussie, le Backend prépare le prompt pour Gemini, en injectant la catégorie prédite comme contexte.
4. **Appel Gemini (Synthèse & Ton)** : Le prompt contextualisé est envoyé à l'API Gemini. Le Backend attend le résumé et l'évaluation du ton.
5. **Agrégation et Sortie** : Les données de HF et Gemini sont agrégées dans un objet JSON structuré.
6. **Réponse** : Le JSON final est renvoyé au Frontend.

## 🚨 Gestion des Erreurs et Logs

Une gestion d'erreurs complète est essentielle pour un workflow à double dépendance externe :

| Erreur | Détection | Logique de Gestion Backend |
|--------|-----------|----------------------------|
| Auth | Échec de validation JWT | Retour HTTP 401 |
| Erreur HF | Timeout, code HTTP non-200, format de réponse invalide | Log critique, retour HTTP 503 (Service Indisponible) |
| Score Faible | Score de confiance HF < seuil défini | Log d'avertissement, ajout d'un message dans la réponse JSON, ou refus du workflow |
| Erreur Gemini | Format JSON malformé, API Down | Tentative de re-parsing ou retour HTTP 500 avec message d'erreur |

**Logging** : Le module `logging` capture les étapes de l'orchestration, les temps de réponse (performance), et toutes les erreurs critiques dans le dossier `logs/`.

## ⚠️ Limites Techniques Liées à la Double Dépendance IA

Le système introduit deux points de défaillance externes critiques qui doivent être gérés :

1. **Vitesse d'Orchestration** : La latence totale est la somme de (T_HF + T_Gemini + T_Réseau). Des timeouts agressifs doivent être mis en place pour éviter que l'API ne reste bloquée.
2. **Fiabilité de la Classification HF** : La qualité de la synthèse Gemini dépend directement de la pertinence de la catégorie donnée par HF. Si le score de confiance HF est faible, la qualité du résultat final (synthèse) peut être dégradée.
3. **Coûts et Quotas** : Chaque analyse génère deux appels API payants/limités. La table `analysis_logs` (optionnelle) est cruciale pour le monitoring des coûts.

## ⚙️ Instructions de Lancement (Environnement & Docker)

**Pré-requis** : Docker et Docker Compose.

### 1. Configuration

Remplissez le fichier `.env` avec les clés API et les identifiants de base de données.

### 2. Lancement Complet avec Docker Compose
```bash
docker-compose up --build -d
```

Le service `backend` et la base de données `postgres` seront lancés. L'API est accessible sur `http://localhost:8000`.