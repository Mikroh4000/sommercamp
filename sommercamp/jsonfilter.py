import json

# JSON-Datei einlesen
with open("data/documents.jsonl", "r", encoding="utf-8") as f:
    daten = []
    for line in f:
        eintrag = json.loads(line)
        daten.append(eintrag)
    # daten = list(f)

# Filtern: Nur URLs mit "chessbase.com/post/"
gefilterte_daten = [eintrag for eintrag in daten if "chessbase.com/post/" in eintrag["url"]]

# Gefilterte Daten speichern (optional)
with open("gefiltert.json", "w", encoding="utf-8") as f:
    for record in gefilterte_daten:
        json_line = json.dumps(record)
        f.write(json_line + "\n")

