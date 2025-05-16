import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from core.rag_pipeline import charger_evenements, generer_documents, creer_index
from utils.vector_store import FaissVectorStore
from langchain_mistralai import ChatMistralAI
from utils.config import get_config

def test_recherche_semantique():
    config = get_config()

    # Charger les événements et les documents (avec découpage activé)
    df = charger_evenements("Île-de-France")
    documents = generer_documents(df)

    # Créer l'index et les embeddings
    (index, _), embeddings = creer_index(documents, dimension=config["embedding_dim"], n_lists=10)

    # Initialiser le LLM Mistral
    llm = ChatMistralAI(
        model=config["chat_model"],
        api_key=config["mistral_api_key"],
        temperature=0.7,
        language="fr"
    )

    # Créer le vector store
    store = FaissVectorStore(embeddings, config["index_path"], index, llm)
    store.add_documents(documents)

    # Effectuer une requête
    question = "Quels sont les spectacles de danse cette semaine ?"
    result = store.process_query(question)
    response = result["response"]["current_answer"]

    # Test
    assert isinstance(response, str) and len(response.strip()) > 0, " Aucune réponse générée par le chatbot."

    print("✅ Recherche RAG réussie, réponse générée :")
    print(response)

if __name__ == "__main__":
    test_recherche_semantique()
