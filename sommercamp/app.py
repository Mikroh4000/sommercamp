# Hier importieren wir die benötigten Softwarebibliotheken.
from os.path import abspath, exists
from sys import argv
from streamlit import (text_input, header, title, subheader, button,
    container, markdown, link_button, divider, set_page_config, session_state)
from pyterrier import started, init
# Die PyTerrier-Bibliothek muss zuerst gestartet werden,
# um alle seine Bestandteile importieren zu können.
if not started():
    init()
from pyterrier import IndexFactory
from pyterrier.batchretrieve import BatchRetrieve
from pyterrier.text import get_text, snippets

def num_results():
    session_state.num_results += 10

# Diese Funktion baut die App für die Suche im gegebenen Index auf.
def app(index_dir) -> None:
    # Konfiguriere den Titel der Web-App (wird im Browser-Tab angezeigt)
    set_page_config(
        page_title="Schach-Suchmaschine",
        layout="centered",
    )

    # Gib der App einen Titel und eine Kurzbeschreibung:
    title("Schach-Suchmaschine")
    markdown("Hier kannst du unsere neue Schach-Suchmaschine nutzen:")

    # Erstelle ein Text-Feld, mit dem die Suchanfrage (query) 
    # eingegeben werden kann.
    query = text_input(
        label="Suchanfrage",
        placeholder="Suche...",
        value="Schach",
    )

    # Wenn die Suchanfrage leer ist, dann kannst du nichts suchen.
    if query == "":
        markdown("Bitte gib eine Suchanfrage ein.")
        return

    session_state.setdefault("num_results", 10)

    # Öffne den Index.
    index = IndexFactory.of(abspath(index_dir))
    # Initialisiere den Such-Algorithmus. 
    searcher = BatchRetrieve(
        index,
        wmodel="BM25",
        num_results=session_state.num_results,
    )
    # Initialisiere das Modul, zum Abrufen der Texte.
    text_getter = get_text(index, metadata=["url", "title", "text"]) #################################################################
    # Baue die Such-Pipeline zusammen.
    pipeline = searcher >> text_getter
    # Führe die Such-Pipeline aus und suche nach der Suchanfrage.
    results = pipeline.search(query)

    # Zeige eine Unter-Überschrift vor den Suchergebnissen an.
    divider()
    header("Suchergebnisse")

    # Wenn die Ergebnisliste leer ist, gib einen Hinweis aus.
    if len(results) == 0:
        markdown("Keine Suchergebnisse.")
        return

    # Wenn es Suchergebnisse gibt, dann zeige an, wie viele.
    markdown(f"{len(results)} Suchergebnisse.")
    for _, row in results.iterrows():
        # Pro Suchergebnis, erstelle eine Box (container).
        with container(border=True):
            # Zeige den Titel der gefundenen Webseite an.
            subheader(row["title"])
            # Speichere den Text in einer Variablen (text).
            text = row["text"]
            # Schneide den Text nach 500 Zeichen ab.
            text = text[:500]
            # Ersetze Zeilenumbrüche durch Leerzeichen.
            text = text.replace("\n", " ")
            # Zeige den Dokument-Text an.
            markdown(text)
            # Gib Nutzern eine Schaltfläche, um die Seite zu öffnen.
            link_button("Seite öffnen", url=row["url"])

    button("zeig mir bitte mehr :-)", on_click=num_results)

    # if button("zeig mir bitte mehr :-)"):
    #     print(session_state.num_results)
    #     session_state.num_results += 10
    #     if session_state.num_results == 10:
    #         session_state.num_results = 20
        

# Die Hauptfunktion, die beim Ausführen der Datei aufgerufen wird.
def main():
    # Lade den Pfad zum Index aus dem ersten Kommandozeilen-Argument.
    index_dir = argv[1]

    # Wenn es noch keinen Index gibt, kannst du die Suchmaschine nicht starten.
    if not exists(index_dir):
        exit(1)

    # Rufe die App-Funktion von oben auf.
    app(index_dir)


if __name__ == "__main__":
    main()