import requests

def wikipedia_search(user_query):
    """
    Sucht nach einem Wikipedia-Artikel und gibt eine Zusammenfassung zurück.
    """
    query = user_query.replace(" ", "_")  # Wikipedia-URLs verwenden Unterstriche
    url = f"https://de.wikipedia.org/api/rest_v1/page/summary/{query}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Unbekannt")
            extract = data.get("extract", "Keine Zusammenfassung verfügbar.")
            page_url = data["content_urls"]["desktop"]["page"]

            return f"**Wikipedia: {title}**\n\n{extract}\n\n[Mehr lesen]({page_url})"
        else:
            return "Wikipedia-Artikel nicht gefunden."
    except Exception as e:
        return f"Fehler beim Abruf von Wikipedia: {str(e)}"

def run_pipeline(context):
    """
    OpenWebUI-Pipeline: Holt Wikipedia-Daten und gibt sie an das LLM weiter.
    """
    user_input = context["input"]
    
    # Prüfen, ob der Nutzer nach Wikipedia fragt
    if user_input.lower().startswith("wikipedia:"):
        search_term = user_input[10:].strip()  # Entfernt "wikipedia: " aus der Anfrage
        result = wikipedia_search(search_term)
        return {"output": result}
    
    return {"output": "Bitte 'wikipedia: Suchbegriff' verwenden."}

