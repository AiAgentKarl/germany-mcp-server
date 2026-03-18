"""Lebensmittelwarnung Client — Produktrückrufe und Warnungen."""

import httpx

from src.config import settings


class FoodWarningsClient:
    """Async-Client für Lebensmittelwarnungen (lebensmittelwarnung.de).

    Kein API-Key nötig. Liefert aktuelle Produktrückrufe
    und Lebensmittelwarnungen in Deutschland.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)
        self._base = settings.food_warnings_base_url

    async def get_warnings(self, rows: int = 20) -> list[dict]:
        """Aktuelle Lebensmittelwarnungen und Produktrückrufe."""
        resp = await self._client.get(
            f"{self._base}/warnings/merged",
            params={
                "rows": rows,
                "sort": "publishedDate desc, title asc",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", {}).get("docs", [])

    async def close(self):
        """HTTP-Client schließen."""
        await self._client.aclose()
