# 🎭 Projet Puls Events – Chatbot Culturel avec Mistral et LangChain

## 🧭 Objectif

Ce projet permet de répondre aux questions des citoyens concernant les événements culturels en temps réel, en s’appuyant sur des données 
ouvertes et une recherche sémantique via RAG (Retrieval-Augmented Generation).

---

Projet/
│
├── main.py                      # 🎯 Interface principale avec Streamlit (chatbot utilisateur)
├── indexer.py                   # 🛠️ Script d’indexation initiale des documents (pipeline RAG)
│
├── core/                        # 🔁 Composants cœur du système RAG
│   ├── chatbot.py               # Appel principal au moteur RAG (ask_bot)
│   └── rag_pipeline.py          # Pipeline : extraction → embedding → FAISS index
│
├── utils/                       # 🔧 Outils techniques & services
│   ├── config.py                # Paramétrage centralisé (API clés, chemins...)
│   ├── vector_store.py          # Intégration FAISS, recherche sémantique & mémoire
│   ├── data_loader.py           # Chargement, nettoyage et transformation des événements
│   ├── database.py              # Gestion du stockage de feedback utilisateur
│   └── logging_config.py        # Configuration du système de logs (optionnel)
│
├── tests/                       # ✅ Scripts de test unitaire (extraction, transformation, indexation)
│
├── requirements.txt             # 📦 Liste des dépendances du projet
├── .env                         # 🔐 Fichier d’environnement (non versionné) avec clé API Mistral
└── README.md                    # 📘 Documentation du projet


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


