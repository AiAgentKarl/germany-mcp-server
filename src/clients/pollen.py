"""Pollenflug Client — DWD Pollenflugvorhersage."""

import httpx

from src.config import settings


# Pollenarten im DWD-Datensatz
POLLEN_TYPES = [
    "Ambrosia", "Beifuss", "Birke", "Erle", "Esche",
    "Graeser", "Hasel", "Roggen",
]

# Belastungsstufen
POLLEN_LEVELS = {
    "0": "keine Belastung",
    "0-1": "keine bis geringe Belastung",
    "1": "geringe Belastung",
    "1-2": "geringe bis mittlere Belastung",
    "2": "mittlere Belastung",
    "2-3": "mittlere bis hohe Belastung",
    "3": "hohe Belastung",
}


class PollenClient:
    """Async-Client für DWD Pollenflug-Vorhersage.

    Kein API-Key nötig. Daten aus DWD Open Data.
    Vorhersage für 27 Regionen in Deutschland.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)
        self._base = settings.pollen_base_url

    async def get_forecast(self) -> dict:
        """Aktuelle Pollenflug-Vorhersage für alle Regionen.

        Gibt Vorhersage für heute, morgen und übermorgen zurück,
        aufgeschlüsselt nach Region und Pollenart.
        """
        resp = await self._client.get(f"{self._base}/s31fg.json")
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        """HTTP-Client schließen."""
        await self._client.aclose()
