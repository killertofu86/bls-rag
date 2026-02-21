import os
from utils import *
from sentence_transformers import SentenceTransformer
import chromadb
from lisette import Chat
import logging, warnings
logging.disable(logging.WARNING)
warnings.filterwarnings("ignore")


embed_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("bls")

def search_bls(query: str) -> str:
    "Search the BLS food database for nutrition information"
    results = collection.query(query_embeddings=[embed_model.encode(query).tolist()], n_results=5)
    return "\n\n".join(results["documents"][0])

def filter_by_nutrient(nutrient_code: str, min_value: float, max_value: float = None) -> str:
    "Filter foods by nutrient value. nutrient_code e.g. 'FE', 'VITC'. Returns matching foods."
    where = {nutrient_code: {"$gte": min_value}} if max_value is None else {"$and": [{nutrient_code: {"$gte": min_value}}, {nutrient_code: {"$lte": max_value}}]}
    results = collection.get(where=where)
    if not results["documents"]: return "Keine Lebensmittel gefunden."
    return "\n\n".join(results["documents"][:10])

def get_food_details(name: str) -> str:
    "Get all nutrient details for a specific food by name."
    results = collection.query(query_embeddings=embed_model.encode(name).tolist(), n_results=1)
    if not results["documents"][0]: return "Lebensmittel nicht gefunden."
    return results["documents"][0][0]

def compare_foods(food1: str, food2: str) -> str:
    "Compare nutritional values of two foods by name."
    results = []
    for name in [food1, food2]:
        match = df[df["Lebensmittelbezeichnung"].str.contains(name, case=False, na=False)]
        results.append(make_chunk(match.iloc[0]) if not match.empty else f"{name}: nicht gefunden.")
    return "\n\n".join(results)

def filter_by_category(category: str) -> str:
    "Filter foods by category e.g. 'Gemüse', 'Fleisch', 'Obst', 'Milchprodukte'."
    results = collection.get(where={"kategorie": {"$eq": category}})
    if not results["documents"]: return "Keine Lebensmittel in dieser Kategorie gefunden."
    return "\n\n".join(results["documents"][:10])

chat = Chat("gemini/gemini-2.5-flash", tools=[search_bls, filter_by_nutrient, get_food_details, compare_foods, filter_by_category],
            sp="Du bist ein Ernährungs-Assistent mit Zugriff auf die BLS Nährstoffdatenbank. Nutze IMMER zuerst die verfügbaren Tools bevor du antwortest, auch bei allgemeinen Ernährungsfragen.")

while True:
    frage = input("\nFrage: ")
    if frage.lower() in ("exit", "quit"): break
    response = chat(frage)
    print(response.choices[0].message.content)
