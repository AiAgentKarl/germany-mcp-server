"""Bundestag DIP Client — Parlamentarische Daten (Drucksachen, Vorgänge, Plenarprotokolle)."""

import httpx

from src.config import settings


class BundestagClient:
    """Async-Client für die Bundestag DIP API.

    Braucht optional einen API-Key (kostenlos registrierbar).
    Ohne Key: eingeschränktes Rate-Limit.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)
        self._base = settings.bundestag_base_url

    def _headers(self) -> dict:
        """Request-Headers mit optionalem API-Key."""
        headers = {"Accept": "application/json"}
        key = settings.bundestag_api_key
        if key:
            headers["Authorization"] = f"ApiKey {key}"
        return headers

    async def search_drucksachen(
        self, query: str, wahlperiode: int = 20, limit: int = 10
    ) -> dict:
        """Bundestagsdrucksachen durchsuchen.

        Args:
            query: Suchbegriff
            wahlperiode: Wahlperiode (20 = aktuell)
            limit: Max. Ergebnisse
        """
        resp = await self._client.get(
            f"{self._base}/drucksache",
            params={
                "f.zuordnung": "BT",
                "f.wahlperiode": wahlperiode,
                "f.drucksachetyp": "Gesetzentwurf",
                "cursor": query,
                "format": "json",
            },
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()

    async def search_vorgaenge(
        self, query: str, wahlperiode: int = 20, limit: int = 10
    ) -> dict:
        """Parlamentarische Vorgänge durchsuchen."""
        params = {
            "f.wahlperiode": wahlperiode,
            "format": "json",
        }
        if query:
            params["f.titel"] = query
        resp = await self._client.get(
            f"{self._base}/vorgang",
            params=params,
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()

    async def get_aktivitaeten(self, limit: int = 10) -> dict:
        """Letzte parlamentarische Aktivitäten."""
        resp = await self._client.get(
            f"{self._base}/aktivitaet",
            params={"format": "json"},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        """HTTP-Client schließen."""
        await self._client.aclose()
