import re
import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()
api_key = os.getenv('MISTRAL_AI_KEY')
embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=api_key)

def clean_text(text):
    """Nettoie une description HTML pour usage NLP"""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    text = re.sub(r'[^\w\s.,!?;:\'\"À-ÿ]', ' ', text)
    return ' '.join(text.split())

def get_culture_event_agenda(location):
    """
    Récupère les événements culturels < 1 an pour une région donnée
    """
    start_year = 2024
    results = []
    event_list = [
        "cinema", "festival", "culture", "concert", "danse", "spectacle", "theatre", "jazz",
        "exposition", "animation", "rock", "humour", "jeu", "atelier", "peinture", "cirque",
        "chanson", "lecture", "livre", "photographie", "film", "conte", "dessin", "chant", "art",
        "musique", "poésie"
    ]

    for event_type in event_list:
        url = (
            f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
            f"evenements-publics-openagenda/records?limit=1&refine=keywords_fr%3A%22{event_type}%22"
            f"&refine=firstdate_begin%3A%22{start_year}%22"
            f"&refine=location_region%3A%22{location}%22"
        )
        response = requests.get(url)
        total_count = response.json().get("total_count", 0)

        for offset_index in range(int(total_count / 100) + 1):
            offset_url = (
                f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
                f"evenements-publics-openagenda/records?limit=100&offset={offset_index * 100}"
                f"&refine=keywords_fr%3A%22{event_type}%22"
                f"&refine=firstdate_begin%3A%222024%22"
                f"&refine=location_region%3A%22{location}%22"
            )
            offset_response = requests.get(offset_url)
            offset_results = offset_response.json().get("results", [])
            results.extend(offset_results)
            time.sleep(0.5)

    df = pd.DataFrame(results)
    if df.empty:
        return pd.DataFrame()

    df.drop_duplicates(subset="uid", inplace=True)
    df.dropna(subset=["uid", "title_fr", "description_fr"], inplace=True)
    df["firstdate_begin"] = pd.to_datetime(df["firstdate_begin"], errors="coerce")
    df = df[df["firstdate_begin"] > pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=365)]

    df["description_fr"] = df["description_fr"].apply(clean_text)
    df["content"] = (
        df["description_fr"] + " lieu: " + df["location_name"] +
        " adresse: " + df["location_address"] + " " + df["location_city"] +
        " " + df["location_postalcode"] + " dates: " + df["daterange_fr"] +
        " début: " + df["firstdate_begin"].astype(str) +
        " fin: " + df["lastdate_end"] +
        " mots clés: " + df["keywords_fr"].astype(str)
    )

    return df

def get_documents(df):
    """Transforme un DataFrame en liste de Documents LangChain"""
    documents = []
    for _, row in df.iterrows():
        content = row["content"] if pd.notna(row["content"]) else row["description_fr"]
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": "opendatasoft",
                    "id": row["uid"],
                    "title": clean_text(row["title_fr"]),
                    "description": row["description_fr"],
                    "firstdate_begin": row.get("firstdate_begin"),
                    "location_city": row.get("location_city"),
                    "location_address": row.get("location_address"),
                }
            )
        )
    return documents


def splitter_documents(documents):
    api_key = os.getenv("MISTRAL_AI_KEY")
    if not api_key:
        raise ValueError("MISTRAL_AI_KEY manquante dans splitter_documents()")

    text_splitter = SemanticChunker(MistralAIEmbeddings(
        model="mistral-embed",
        api_key=api_key
    ))

    texts = [doc.page_content for doc in documents]
    return text_splitter.create_documents(texts)
