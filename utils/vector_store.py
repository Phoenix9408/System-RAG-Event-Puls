import os
import json
import faiss
import shutil
import numpy as np
from datetime import datetime
from uuid import uuid4
from typing import TypedDict, List
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langgraph.graph import StateGraph


# État conversationnel utilisé par LangGraph
class State(TypedDict):
    query: str
    documents: List[dict]
    ids: List[uuid4]
    results: List[Document]
    response: str
    chat_history: list
    memory: dict

def create_optimized_index(dimension, embeddings, documents, n_lists=100):
    """Crée un index FAISS optimisé et entraîné à partir de documents"""
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFFlat(quantizer, dimension, n_lists)

    texts = [doc.page_content for doc in documents]
    vectors = embeddings.embed_documents(texts)
    vectors = np.array(vectors).astype('float32')

    index.train(vectors)
    return index, vectors

class FaissVectorStore:
    """Classe de gestion FAISS + LLM + mémoire conversationnelle"""

    def __init__(self, embeddings, index_file, index, llm):
        self.index_file = index_file
        self.embeddings = embeddings
        self.llm = llm

        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=index if index else faiss.IndexFlatL2(1024),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.memory_file = "conversation_memory.json"
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    memory_data = json.load(f)
                    for interaction in memory_data:
                        self.memory.save_context(
                            {"input": interaction["input"]},
                            {"output": interaction["output"]}
                        )
            except json.JSONDecodeError:
                print("⚠️ Erreur lors du chargement de l’historique de conversation.")

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Tu es un assistant qui aide à répondre aux questions en utilisant le contexte fourni."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{context}\n\nQuestion: {query}")
        ])

        self.doc_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.workflow = self._create_search_graph()

    def _create_search_graph(self):
        workflow = StateGraph(State)
        workflow.add_node("search", self._search_node)
        workflow.add_node("process_memory", self._process_memory_node)
        workflow.add_node("process_results", self._process_results_node)
        workflow.set_entry_point("search")
        workflow.add_edge("search", "process_memory")
        workflow.add_edge("process_memory", "process_results")
        return workflow.compile()

    def _search_node(self, state: State) -> State:
        try:
            results = self.vector_store.similarity_search(state["query"])
            state["results"] = results or []
        except Exception as e:
            state["results"] = []
            print(f"Erreur de recherche FAISS : {e}")
        return state

    def _process_memory_node(self, state: State) -> State:
        result_text = state["results"][0].page_content if state["results"] else "Pas de résultat"
        self.memory.save_context({"input": state["query"]}, {"output": result_text})
        memory_data = self.memory.load_memory_variables({})
        state["chat_history"] = memory_data["chat_history"]
        state["memory"] = {
            "last_updated": datetime.now().isoformat(),
            "conversation_length": len(memory_data["chat_history"])
        }
        return state

    def _process_results_node(self, state: State) -> State:
        results = state.get("results", [])
        chat_history = state.get("chat_history", [])
        try:
            response = self.doc_chain.invoke({
                "query": state["query"],
                "context": results,
                "chat_history": chat_history
            })
            state["response"] = {
                "current_answer": response,
                "chat_history": chat_history,
                "context": {"total_interactions": len(chat_history)}
            }
        except Exception as e:
            state["response"] = {
                "current_answer": f"Erreur : {e}",
                "chat_history": chat_history,
                "context": {"total_interactions": len(chat_history)}
            }
        return state

    def process_query(self, query: str):
        initial_state = {
            "query": query,
            "documents": [],
            "results": [],
            "response": "",
            "chat_history": [],
            "memory": {}
        }
        return self.workflow.invoke(initial_state)

    def add_documents(self, documents):
        if not documents:
            raise ValueError("La liste de documents est vide.")
        self.vector_store.add_documents(documents)
        self.vector_store.save_local(self.index_file)
        print(f"{len(documents)} documents ajoutés.")

    def verify_indexing(self, original_df):
        indexed_ids = set(doc.metadata["id"] for doc in self.vector_store.docstore._dict.values())
        original_ids = set(original_df["uid"])
        missing = original_ids - indexed_ids
        if missing:
            print(f"⚠️ {len(missing)} documents non indexés.")
            return False
        return True

    def load_vectorstore(self, index_path):
        self.vector_store = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)

    def remove_index(self):
        if os.path.exists(self.index_file):
            shutil.rmtree(self.index_file)
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
