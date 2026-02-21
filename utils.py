import pandas as pd

NUTRIENTS = ["ENERCJ","ENERCC","WATER","PROT625","FAT","CHO","SUGAR","FIBT","NA","CA","FE","MG","K","VITD","VITB12","VITC","VITB6","FOL","VITE"]

CAT_MAP = dict(B="Getreide",C="Getreide",D="Backwaren",E="Teigwaren",F="Obst",G="Gemüse",H="Sprossen",K="Stärke",M="Milchprodukte",N="Getränke",P="Alkohol",Q="Öle",R="Gewürze",S="Süßmittel",T="Fisch",U="Fleisch",V="Fleisch",W="Fleisch",X="Fertiggerichte",Y="Fertiggerichte")

comp = pd.read_excel("data/BLS_4_0_Components_DE_EN.xlsx", keep_default_na=False)
df = pd.read_excel("data/BLS_4_0_Daten_2025_DE.xlsx")
wert_cols = [c for c in df.columns if "Datenherkunft" not in c and "Referenz" not in c]
nutrient_cols = {col.split()[0]: col for col in wert_cols if col.split()[0] in NUTRIENTS}
code_map = {row["Nährstoffcode / Component code"]: f"{row['Nährstoffbezeichnung']} [{row['Einheit / Unit']}/100g]" for _, row in comp.iterrows()}

def to_float(val):
    try: return float(val)
    except: return 0.0

def make_chunk(row):
    lines = [f"Lebensmittel: {row['Lebensmittelbezeichnung']} ({row['Food name']})"]
    for col in wert_cols[3:]:
        code = col.split()[0]
        if code not in NUTRIENTS: continue
        val = row[col]
        if pd.notna(val): lines.append(f"  {code_map.get(code, col)}: {val}")
    return "\n".join(lines)
