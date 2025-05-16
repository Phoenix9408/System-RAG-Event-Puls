import json
import os

FEEDBACK_FILE = "feedback_store.json"

def save_feedback(question, answer, feedback , comment=""):
    """Enregistre un feedback utilisateur"""
    record = {
        "question": question,
        "answer": answer,
        "feedback": feedback,
        "comment": comment
    }

    data = []
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(record)

    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_feedback():
    """Charge tous les feedbacks enregistrés"""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
