import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_mistralai import ChatMistralAI
from utils.vector_store import FaissVectorStore
from langchain_mistralai import MistralAIEmbeddings
from core.rag_pipeline import charger_evenements, generer_documents, creer_index
from utils.config import get_config

load_dotenv()

config = get_config()

def load_chatbot_components():
    api_key = config["mistral_api_key"]
    embeddings = MistralAIEmbeddings(model=config["embedding_model"], api_key=api_key)
    llm = ChatMistralAI(
        model=config["chat_model"],
        api_key=api_key,
        temperature=0.7
    )
    index_path = config["index_path"]
    # Si l’index FAISS est déjà sauvegardé, on le charge
    if os.path.exists(index_path):
        vector_store = FaissVectorStore(embeddings, index_path, None, llm)
        vector_store.load_vectorstore(index_path)
    else:
        # Sinon on le génère une fois
        df = charger_evenements(config["default_region"])
        documents = generer_documents(df)
        (index, _)= creer_index(documents, dimension=1024, n_lists=10)
        vector_store = FaissVectorStore(embeddings, index_path, index, llm)
        vector_store.add_documents(documents)

    return vector_store, llm


def ask_bot(query: str) -> str:
    vector_store, llm = load_chatbot_components()

    results = vector_store.vector_store.similarity_search(query, k=3)
    if not results:
        return "Je n’ai trouvé aucun événement correspondant à votre demande."

    # Prompt : on injecte le contexte + la question
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant culturel qui recommande des événements à partir d'une base de données."),
        ("human", "{context}\n\nQuestion: {query}")
    ])

    chain = create_stuff_documents_chain(llm, prompt)

    response = chain.invoke({
        "context": results,
        "query": query
    })

    return response
