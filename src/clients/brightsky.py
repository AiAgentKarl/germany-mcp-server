"""Bright Sky Client — Wetterdaten vom DWD als JSON-API."""

import httpx

from src.config import settings


class BrightSkyClient:
    """Async-Client für Bright Sky (DWD Wetter-API).

    Bright Sky ist eine inoffizielle aber sehr stabile JSON-API
    die DWD Open-Data aufbereitet. Kein API-Key nötig.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)
        self._base = settings.brightsky_base_url

    async def get_current_weather(self, lat: float, lon: float) -> dict:
        """Aktuelles Wetter an einem Standort (lat/lon)."""
        resp = await self._client.get(
            f"{self._base}/current_weather",
            params={"lat": lat, "lon": lon},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_weather(
        self, lat: float, lon: float, date: str, last_date: str | None = None
    ) -> dict:
        """Wetterdaten für Zeitraum (date im Format YYYY-MM-DD)."""
        params = {"lat": lat, "lon": lon, "date": date}
        if last_date:
            params["last_date"] = last_date
        resp = await self._client.get(f"{self._base}/weather", params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_alerts(
        self, lat: float | None = None, lon: float | None = None
    ) -> dict:
        """Aktuelle DWD-Wetterwarnungen (optional nach Standort filtern)."""
        params = {}
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        resp = await self._client.get(f"{self._base}/alerts", params=params)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        """HTTP-Client schließen."""
        await self._client.aclose()
