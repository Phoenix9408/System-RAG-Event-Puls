import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from core.rag_pipeline import charger_evenements, generer_documents, creer_index

def test_index_creation():
    df = charger_evenements("Île-de-France")
    documents = generer_documents(df)
    (index, vectors), _ = creer_index(documents, dimension=1024, n_lists=10)

    assert vectors.shape[0] == len(documents), "❌ Nombre de vecteurs incorrect."
    assert index.is_trained, "❌ L’index FAISS n’est pas entraîné."

    print(f"✅ Index FAISS entraîné avec {vectors.shape[0]} vecteurs.")

if __name__ == "__main__":
    test_index_creation()
