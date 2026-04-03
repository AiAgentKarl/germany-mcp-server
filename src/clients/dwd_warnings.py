"""DWD Wetterwarnungen Client — Offizielle Warnungen vom Deutschen Wetterdienst.

Nutzt den DWD Warnungen-Endpoint (JSONP), der die aktuellen
amtlichen Wetterwarnungen fuer ganz Deutschland liefert.
Kein API-Key noetig.
"""

import json

import httpx

from src.config import settings


# Schweregrad-Mapping
WARN_LEVELS = {
    1: "Wetterwarnung (gelb)",
    2: "Warnung vor markantem Wetter (orange)",
    3: "Unwetterwarnung (rot)",
    4: "Warnung vor extremem Unwetter (violett)",
}

# Bundeslaender-Mapping (Kuerzel -> voller Name)
BUNDESLAENDER = {
    "SH": "Schleswig-Holstein",
    "HH": "Hamburg",
    "NI": "Niedersachsen",
    "HB": "Bremen",
    "NW": "Nordrhein-Westfalen",
    "NRW": "Nordrhein-Westfalen",
    "HE": "Hessen",
    "RP": "Rheinland-Pfalz",
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "SL": "Saarland",
    "BE": "Berlin",
    "BB": "Brandenburg",
    "MV": "Mecklenburg-Vorpommern",
    "SN": "Sachsen",
    "ST": "Sachsen-Anhalt",
    "TH": "Thüringen",
}


class DwdWarningsClient:
    """Async-Client fuer DWD Wetterwarnungen.

    Kein API-Key noetig. Offizielle Daten des Deutschen Wetterdienstes.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)
        self._url = settings.dwd_warnings_url

    async def get_warnings(self, region: str | None = None) -> dict:
        """Aktuelle DWD-Wetterwarnungen abrufen.

        Args:
            region: Optionaler Filter — Bundesland-Name oder Kuerzel
                    (z.B. "Bayern", "NRW", "Sachsen")
        """
        resp = await self._client.get(self._url)
        resp.raise_for_status()

        # JSONP-Wrapper entfernen: warnWetter.loadWarnings({...})
        text = resp.text.strip()
        if text.startswith("warnWetter.loadWarnings("):
            text = text[len("warnWetter.loadWarnings("):]
            if text.endswith(")"):
                text = text[:-1]
            elif text.endswith(");"):
                text = text[:-2]

        data = json.loads(text)

        # Warnungen sammeln (verschachtelt nach Region-Code)
        all_warnings = []
        warnings_dict = data.get("warnings", {})

        for region_code, region_warnings in warnings_dict.items():
            if isinstance(region_warnings, list):
                for w in region_warnings:
                    all_warnings.append(w)

        # Vorab-Informationen auch einbeziehen
        vorab = data.get("vorabInformation", {})
        for region_code, vorab_warnings in vorab.items():
            if isinstance(vorab_warnings, list):
                for w in vorab_warnings:
                    w["_vorab"] = True
                    all_warnings.append(w)

        # Regional filtern wenn angegeben
        if region:
            region_lower = region.lower().strip()
            # Kuerzel in vollen Namen umwandeln
            region_full = BUNDESLAENDER.get(region.upper(), "")
            if region_full:
                region_lower = region_full.lower()

            filtered = []
            for w in all_warnings:
                state = (w.get("state", "") or "").lower()
                region_name = (w.get("regionName", "") or "").lower()
                state_short = (w.get("stateShort", "") or "").lower()

                if (
                    region_lower in state
                    or region_lower in region_name
                    or region_lower == state_short
                ):
                    filtered.append(w)

            all_warnings = filtered

        return {
            "zeitpunkt": data.get("time"),
            "warnungen": all_warnings,
        }

    async def close(self):
        """HTTP-Client schliessen."""
        await self._client.aclose()
