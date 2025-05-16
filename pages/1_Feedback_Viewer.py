import streamlit as st
from utils.database import load_feedback

st.title("🗂️ Feedback Utilisateurs")
data = load_feedback()
if data:
    for fb in data:
        st.markdown(f"**Q:** {fb['question']}")
        st.markdown(f"**R:** {fb['answer']}")
        st.markdown(f"**Avis:** {fb['feedback']}")
        st.markdown("---")
else:
    st.info("Aucun feedback enregistré pour le moment.")
