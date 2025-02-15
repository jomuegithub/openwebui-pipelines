"""
title: Wikipedia Pipeline
author: Ihr Name
date: 2025-02-15
version: 1.0
license: MIT
description: Eine Pipeline zur Abfrage von Wikipedia-Artikeln in OpenWebUI.
requirements: wikipedia
"""

from typing import List, Union
from pydantic import BaseModel, Field
import wikipedia
import os

class Pipeline:
    """
    Wikipedia-Pipeline für OpenWebUI.
    """

    class Valves(BaseModel):
        """
        Konfigurierbare Parameter für die Pipeline.
        """
        LANGUAGE: str = Field(default="de", description="Sprache für Wikipedia-Abfragen")

    def __init__(self):
        """
        Initialisierung der Pipeline.
        """
        self.id = "wikipedia_pipeline"
        self.name = "Wikipedia Pipeline"
        self.valves = self.Valves(
            **{k: os.getenv(k, v.default) for k, v in self.Valves.__fields__.items()}
        )
        wikipedia.set_lang(self.valves.LANGUAGE)

    async def on_startup(self):
        """
        Wird beim Start des Servers aufgerufen.
        """
        print(f"Pipeline '{self.name}' gestartet.")

    async def on_shutdown(self):
        """
        Wird beim Stoppen des Servers aufgerufen.
        """
        print(f"Pipeline '{self.name}' gestoppt.")

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, dict]:
        """
        Hauptfunktion der Pipeline. Verarbeitet Benutzereingaben und gibt Wikipedia-Informationen zurück.
        """
        if user_message.lower().startswith("wikipedia:"):
            search_term = user_message[10:].strip()
            if not search_term:
                return "Bitte geben Sie einen Suchbegriff nach 'wikipedia:' ein."

            try:
                summary = wikipedia.summary(search_term, sentences=3)
                page = wikipedia.page(search_term)
                response = f"**{page.title}**\n\n{summary}\n\n[Mehr erfahren]({page.url})"
                return response
            except wikipedia.exceptions.DisambiguationError as e:
                return f"Der Suchbegriff ist mehrdeutig. Mögliche Optionen sind:\n{', '.join(e.options)}"
            except wikipedia.exceptions.PageError:
                return "Kein Wikipedia-Artikel mit diesem Titel gefunden."
            except Exception as e:
                return f"Fehler bei der Abfrage: {str(e)}"
        else:
            return "Um eine Wikipedia-Suche durchzuführen, beginnen Sie Ihre Anfrage mit 'wikipedia:'."


