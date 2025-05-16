import sys
import os
import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from core.rag_pipeline import charger_evenements

def test_event_retrieval():
    df = charger_evenements("Île-de-France")

    print(f"Nombre d'événements récupérés : {len(df)}")

    assert not df.empty, "❌ Aucun événement récupéré."
    assert df["firstdate_begin"].notna().all(), "❌ Certains événements n'ont pas de date."
    assert df["firstdate_begin"].apply(
        lambda d: pd.to_datetime(d).tz_localize(None) >= pd.Timestamp.now().tz_localize(None) - pd.Timedelta(days=365)
    ).all(), "❌ Certains événements ont plus d’un an."
    assert df["description_fr"].notna().all(), "❌ Des événements n'ont pas de description."

    print("✅ Test passé : événements récupérés et valides.")

if __name__ == "__main__":
    test_event_retrieval()
