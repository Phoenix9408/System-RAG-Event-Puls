import sys
import os
from dotenv import load_dotenv
from langchain_core.documents import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from core.rag_pipeline import charger_evenements, generer_documents

def test_document_transformation():
    df = charger_evenements("Île-de-France")
    documents = generer_documents(df)

    assert isinstance(documents, list), " La sortie n’est pas une liste."
    assert all(isinstance(doc, Document) for doc in documents), " Certains éléments ne sont pas des Documents LangChain."
    assert all(doc.page_content for doc in documents), " Certains documents n’ont pas de contenu."
    assert all("id" in doc.metadata for doc in documents), " Certains documents n’ont pas de métadonnée 'id'."
    assert all("title" in doc.metadata for doc in documents), " Certains documents n’ont pas de 'title'."

    print(f" {len(documents)} documents créés avec succès.")

if __name__ == "__main__":
    test_document_transformation()
