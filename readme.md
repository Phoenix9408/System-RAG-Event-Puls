# 🎭 Projet Puls Events – Chatbot Culturel avec Mistral et LangChain

## 🧭 Objectif

Ce projet permet de répondre aux questions des citoyens concernant les événements culturels en temps réel, en s’appuyant sur des données 
ouvertes et une recherche sémantique via RAG (Retrieval-Augmented Generation).

---

## 🗂️ Structure du projet

Projet/
│
├── main.py # Entrée principale de l'application (Streamlit)
├── indexer.py # Script pour indexer les documents (FAISS)
├── core/
│ ├── chatbot.py # Moteur du bot (RAG)
│ ├── rag_pipeline.py # Pipeline complet : data → embeddings → index
├── utils/
│ ├── config.py # Chargement des paramètres
│ ├── vector_store.py # Stockage vectoriel et mémoire conversationnelle
│ ├── data_loader.py # Chargement et transformation des événements
│ ├── database.py # Sauvegarde du feedback utilisateur
│ ├── logging_config.py # Configuration du logging
│
├── tests/ # Dossier de tests automatisés
├── requirements.txt # Dépendances du projet
├── .env # Variables d’environnement (clé API Mistral


---

## 🚀 Lancer l’application

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-projet/chatbot-culturel.git
cd chatbot-culturel



---


## 🚀 Lancer l’application

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-projet/chatbot-culturel.git
cd chatbot-culturel


2. Créer un environnement virtuel
Avec pip :

python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate sur Windows



3. Installer les dépendances

pip install -r requirements.txt

4. Ajouter un fichier .env
Créez un fichier .env à la racine avec votre clé Mistral :

MISTRAL_AI_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxx


5. Lancer l'application

streamlit run main.py

🧪 Tests disponibles
test_event_retrieval : vérifie la récupération d’événements depuis OpenDataSoft

test_document_transformation : vérifie la transformation en documents LangChain

test_index_creation : vérifie que les documents sont correctement vectorisés et indexés


