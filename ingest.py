from utils import *
from sentence_transformers import SentenceTransformer
import chromadb
import logging

logging.disable(logging.WARNING)

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
chunks = [make_chunk(row) for _, row in df.iterrows()]
ids = df["BLS Code"].astype(str).tolist()
embeddings = model.encode(chunks, show_progress_bar=True)

client = chromadb.PersistentClient(path="./chroma_db")
try:
    collection = client.get_collection("bls")
    if collection.count() == 7140:
        print("DB bereits vorhanden, überspringe Ingestion.")
        exit()
    client.delete_collection("bls")
except: pass
collection = client.get_or_create_collection("bls")

metadatas = [{code: to_float(row[col]) for code, col in nutrient_cols.items()} | {"kategorie": CAT_MAP.get(str(row["BLS Code"])[0], "Sonstige")} for _, row in df.iterrows()]

batch_size = 500
for i in range(0, len(chunks), batch_size):
    collection.add(documents=chunks[i:i+batch_size], embeddings=embeddings[i:i+batch_size].tolist(), ids=ids[i:i+batch_size], metadatas=metadatas[i:i+batch_size])
print(f"Fertig! {collection.count()} Einträge in der DB.")
