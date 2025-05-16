import sys
import os
import streamlit as st

# Ajouter le chemin vers le dossier core pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "core")))

from core.chatbot import ask_bot
from utils.database import save_feedback

st.set_page_config(page_title="Chatbot Culturel", layout="centered")

st.title("🎭 Chatbot Culturel - Puls Events : Réalisé dans le cadre du projet OpenClassrooms")
st.markdown("Pose une question pour découvrir des événements culturels recommandés en temps réel.")

# Zone de saisie utilisateur
query = st.text_input("💬 Que veux-tu savoir ?", placeholder="Ex: Quels concerts à Paris cette semaine ?", key="query")

if query:
    with st.spinner("Recherche en cours..."):
        try:
            response = ask_bot(query)
            st.success("🤖 Réponse du bot :")
            st.markdown(response)

            # Formulaire de feedback
            with st.form(key="feedback_form"):
                st.markdown("🔁 Que penses-tu de cette réponse ?")
                feedback = st.radio("Feedback :", ["👍 Utile", "👎 Pas pertinent"], horizontal=True)
                comment = st.text_area("✍️ Commentaire (facultatif)")
                submitted = st.form_submit_button("Envoyer le feedback")

                if submitted:
                    save_feedback(query, response, feedback, comment)
                    st.success("✅ Merci pour ton retour !")


        except Exception as e:
            st.error(f"❌ Erreur : {e}")
