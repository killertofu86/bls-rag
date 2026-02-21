# bls-rag

RAG-System auf Basis des Bundeslebensmittelschlüssels (BLS) 4.0.

## Über das Projekt

Nährstoffdatenbank (7.140 Lebensmittel, 138 Nährstoffe) als RAG-Wissensbasis.

## Features

- Semantische Suche über Lebensmittel und Nährstoffe
- Natürlichsprachliche Abfragen (z.B. "Welches Gemüse hat am meisten Eisen?")
- Optionales Ernährungstagebuch

## Datenquelle

[Bundeslebensmittelschlüssel 4.0](https://blsdb.de/) - Max Rubner-Institut, kostenlos

## Stack

- Python, pandas
- SentenceTransformers
- ChromaDB
- LLM für Antwortgenerierung
