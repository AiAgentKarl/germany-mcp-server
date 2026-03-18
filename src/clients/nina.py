"""NINA Client — Warnungen des BBK (Bundesamt für Bevölkerungsschutz)."""

import httpx

from src.config import settings


class NinaClient:
    """Async-Client für die NINA Warn-API.

    Liefert Katastrophen-Warnungen, Hochwasser, Unwetter etc.
    Kein API-Key nötig.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)
        self._base = settings.nina_base_url

    async def get_warnings(self) -> list[dict]:
        """Alle aktuellen Warnungen (bundesweit, Mowas + Katwarn + DWD + Hochwasser)."""
        all_warnings = []
        # Verschiedene Warn-Kanäle abfragen
        for channel in ("mowas", "katwarn", "biwapp", "dwd", "lhp"):
            try:
                resp = await self._client.get(
                    f"{self._base}/{channel}/mapData.json"
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for w in data:
                        w["_channel"] = channel
                    all_warnings.extend(data)
            except Exception:
                continue
        return all_warnings

    async def get_warning_details(self, warning_id: str) -> dict:
        """Details zu einer bestimmten Warnung abrufen."""
        resp = await self._client.get(
            f"{self._base}/warnings/{warning_id}.json"
        )
        resp.raise_for_status()
        return resp.json()

    async def get_ags_warnings(self, ags: str) -> list[dict]:
        """Warnungen für einen bestimmten Ort via AGS-Code.

        AGS = Amtlicher Gemeindeschlüssel (z.B. '091620000000' für München).
        Die ersten 5 Stellen reichen oft (Kreis-Ebene).
        """
        resp = await self._client.get(
            f"{self._base}/dashboard/{ags}.json"
        )
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        """HTTP-Client schließen."""
        await self._client.aclose()
