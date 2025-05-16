import streamlit as st
import pandas as pd
import os
import json

FEEDBACK_FILE = "feedback_store.json"

st.set_page_config(page_title="📊 Feedback Viewer")

st.title("📊 Feedback utilisateur")
st.markdown("Liste des retours fournis par les utilisateurs sur les réponses du chatbot.")

if os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "r") as f:
        try:
            data = json.load(f)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Aucun feedback enregistré pour le moment.")
        except json.JSONDecodeError:
            st.error("Le fichier de feedback est corrompu ou vide.")
else:
    st.warning("Aucun fichier de feedback trouvé.")
