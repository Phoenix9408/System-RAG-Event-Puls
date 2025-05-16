from core.rag_pipeline import run_pipeline
from utils.vector_store import FaissVectorStore
from langchain_mistralai import ChatMistralAI
from utils.config import get_config

def main():
    config = get_config()
    df, documents, embeddings, index = run_pipeline(config["default_region"])

    llm = ChatMistralAI(model=config["chat_model"], api_key=config["mistral_api_key"], temperature=0.7, language="fr")
    store = FaissVectorStore(embeddings, config["index_path"], index, llm)

    store.add_documents(documents)
    if store.verify_indexing(df):
        print("✅ Indexation complète")
    else:
        print("❌ Problèmes d’indexation")

if __name__ == "__main__":
    main()
