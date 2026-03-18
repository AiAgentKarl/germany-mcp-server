"""SMARD Client — Energiemarktdaten der Bundesnetzagentur."""

import httpx

from src.config import settings


# SMARD Filter-IDs für verschiedene Datenreihen
SMARD_FILTERS = {
    # Stromerzeugung
    "biomasse": 4169,
    "wasserkraft": 4070,
    "wind_offshore": 1225,
    "wind_onshore": 4067,
    "photovoltaik": 4068,
    "sonstige_erneuerbare": 4069,
    "kernenergie": 1224,
    "braunkohle": 1223,
    "steinkohle": 4071,
    "erdgas": 4072,
    "pumpspeicher": 4073,
    "sonstige_konventionelle": 4074,
    # Stromverbrauch
    "stromverbrauch_gesamt": 410,
    # Marktpreise
    "grosshandelspreise": 4169,
    "day_ahead_preis": 4170,
}

# Auflösungen
SMARD_RESOLUTIONS = {
    "stunde": "hour",
    "viertelstunde": "quarterhour",
    "tag": "day",
    "woche": "week",
    "monat": "month",
}


class SmardClient:
    """Async-Client für SMARD Energiemarktdaten.

    Kein API-Key nötig. Daten der Bundesnetzagentur.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)
        self._base = settings.smard_base_url

    async def get_chart_data(
        self,
        filter_id: int,
        resolution: str = "day",
        region: str = "DE",
        timestamp: int | None = None,
    ) -> dict:
        """Zeitreihendaten für einen bestimmten Filter abrufen.

        Args:
            filter_id: SMARD Filter-ID (siehe SMARD_FILTERS)
            resolution: Zeitauflösung (hour, quarterhour, day, week, month)
            region: Ländercode (DE, AT, LU, DE-50HZ, DE-AMPRION, etc.)
            timestamp: Unix-Timestamp für den Startzeitpunkt (optional)
        """
        # Verfügbare Timestamps abrufen wenn keiner angegeben
        if timestamp is None:
            ts_resp = await self._client.get(
                f"{self._base}/{filter_id}/{region}/index_{resolution}.json"
            )
            ts_resp.raise_for_status()
            timestamps = ts_resp.json().get("timestamps", [])
            if not timestamps:
                return {"error": "Keine Daten verfügbar"}
            timestamp = timestamps[-1]  # Neueste Daten

        resp = await self._client.get(
            f"{self._base}/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{timestamp}.json"
        )
        resp.raise_for_status()
        return resp.json()

    async def get_available_timestamps(
        self,
        filter_id: int,
        resolution: str = "day",
        region: str = "DE",
    ) -> list[int]:
        """Verfügbare Zeitstempel für eine Datenreihe."""
        resp = await self._client.get(
            f"{self._base}/{filter_id}/{region}/index_{resolution}.json"
        )
        resp.raise_for_status()
        return resp.json().get("timestamps", [])

    async def close(self):
        """HTTP-Client schließen."""
        await self._client.aclose()
