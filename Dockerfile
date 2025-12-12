# --- Dockerfile simple pour le backend FastAPI ---

# 1) Image Python officielle
FROM python:3.11-slim

# 2) Définir un dossier de travail dans le conteneur
WORKDIR /app

# 4) Copier le requirements.txt
COPY requirements.txt .

# 5) Installer paquets Python
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copier tout le code backend dans le conteneur
COPY . .

# 7) Exposer le port FastAPI
EXPOSE 8000

# 8) Lancer FastAPI avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
