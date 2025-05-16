import os
from dotenv import load_dotenv
import pandas as pd
from langchain_mistralai import MistralAIEmbeddings
from utils.data_loader import get_culture_event_agenda, get_documents,splitter_documents
from utils.vector_store import create_optimized_index
from utils.config import get_config

load_dotenv()
api_key = os.getenv("MISTRAL_AI_KEY")
config = get_config()



if not api_key:
    raise ValueError("❌ La clé MISTRAL_AI_KEY est vide ou manquante. Vérifie ton fichier .env")
embeddings = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=api_key
)


def charger_evenements(region: str = None) -> pd.DataFrame:
    """
    Récupère les événements culturels récents depuis OpenAgenda (via OpenDataSoft)
    """
    region = region or config["default_region"]
    return get_culture_event_agenda(region)

def generer_documents(df: pd.DataFrame):

    """
    Transforme un DataFrame d’événements en liste de Documents LangChain,
    puis découpe chaque texte en chunks sémantiques.
    """

    documents = get_documents(df)
    documents = splitter_documents(documents)

    return documents

def creer_index(documents, dimension: int = None, n_lists: int = 50):
    dimension = dimension or config["embedding_dim"]

    index, vectors = create_optimized_index(
        dimension=dimension,
        embeddings=embeddings,
        documents=documents,
        n_lists=n_lists
    )

    return (index, vectors)

def run_pipeline(region: str = None):
    print("▶️ Chargement des événements...")
    region = region or config["default_region"]
    df = charger_evenements(region)
    print(f"  {len(df)} événements récupérés.")

    print(" Génération des documents...")
    documents = generer_documents(df)
    print(f" {len(documents)} documents générés (avec chunks).")

    print(" Création de l’index FAISS (embedding + training)...")
    (index, _), _embeddings = creer_index(documents, dimension=config["embedding_dim"], n_lists=50)
    print(" Index FAISS prêt.")

    return df, documents, _embeddings, index


