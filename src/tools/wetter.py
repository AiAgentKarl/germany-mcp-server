"""Wetter-Tools — DWD-Wetterdaten und Warnungen über Bright Sky."""

from mcp.server.fastmcp import FastMCP

from src.clients.brightsky import BrightSkyClient

_brightsky = BrightSkyClient()

# Bekannte deutsche Städte mit Koordinaten
STAEDTE = {
    "berlin": (52.52, 13.405),
    "hamburg": (53.551, 9.994),
    "münchen": (48.137, 11.576),
    "muenchen": (48.137, 11.576),
    "köln": (50.938, 6.957),
    "koeln": (50.938, 6.957),
    "frankfurt": (50.110, 8.682),
    "stuttgart": (48.776, 9.183),
    "düsseldorf": (51.228, 6.773),
    "duesseldorf": (51.228, 6.773),
    "dortmund": (51.514, 7.468),
    "essen": (51.456, 7.012),
    "leipzig": (51.340, 12.375),
    "bremen": (53.080, 8.813),
    "dresden": (51.051, 13.738),
    "hannover": (52.376, 9.739),
    "nürnberg": (49.452, 11.077),
    "nuernberg": (49.452, 11.077),
    "duisburg": (51.435, 6.763),
    "bochum": (51.482, 7.216),
    "wuppertal": (51.256, 7.151),
    "bielefeld": (52.022, 8.532),
    "bonn": (50.737, 7.099),
    "mannheim": (49.489, 8.467),
    "augsburg": (48.370, 10.898),
    "wiesbaden": (50.083, 8.240),
    "mainz": (49.993, 8.247),
    "freiburg": (47.999, 7.842),
    "kiel": (54.323, 10.123),
    "rostock": (54.088, 12.131),
}


def _resolve_coords(ort: str, lat: float | None, lon: float | None):
    """Stadt-Name in Koordinaten auflösen oder übergebene nutzen."""
    if lat is not None and lon is not None:
        return lat, lon

    key = ort.lower().strip()
    if key in STAEDTE:
        return STAEDTE[key]

    raise ValueError(
        f"Unbekannter Ort: '{ort}'. Nutze einen bekannten Stadtnamen "
        f"oder gib lat/lon direkt an. Bekannte Städte: "
        f"{', '.join(sorted(set(s.title() for s in STAEDTE.keys())))}"
    )


def register_wetter_tools(mcp: FastMCP):
    """Wetter-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def wetter_aktuell(
        ort: str = "",
        lat: float | None = None,
        lon: float | None = None,
    ) -> dict:
        """Aktuelles Wetter an einem Ort in Deutschland.

        Zeigt Temperatur, Niederschlag, Wind, Bewölkung etc.
        Entweder einen Stadtnamen ODER lat/lon angeben.

        Args:
            ort: Stadtname (z.B. "Berlin", "München", "Hamburg")
            lat: Breitengrad (optional, statt Stadtname)
            lon: Längengrad (optional, statt Stadtname)
        """
        resolved_lat, resolved_lon = _resolve_coords(ort, lat, lon)
        data = await _brightsky.get_current_weather(resolved_lat, resolved_lon)

        weather = data.get("weather", {})
        sources = data.get("sources", [{}])
        station = sources[0].get("station_name", "unbekannt") if sources else "unbekannt"

        return {
            "ort": ort or f"{resolved_lat},{resolved_lon}",
            "station": station,
            "zeitpunkt": weather.get("timestamp", ""),
            "temperatur_c": weather.get("temperature", None),
            "gefuehlte_temperatur_c": weather.get("wind_chill", None),
            "niederschlag_mm": weather.get("precipitation_60", None),
            "wind_km_h": weather.get("wind_speed_60", None),
            "windrichtung_grad": weather.get("wind_direction_60", None),
            "luftfeuchtigkeit_pct": weather.get("relative_humidity", None),
            "bewoelkung_pct": weather.get("cloud_cover", None),
            "sonnenschein_min": weather.get("sunshine_60", None),
            "icon": weather.get("icon", ""),
        }

    @mcp.tool()
    async def wetter_warnungen(
        ort: str = "",
        lat: float | None = None,
        lon: float | None = None,
    ) -> dict:
        """Aktuelle DWD-Wetterwarnungen für einen Ort.

        Zeigt Unwetter, Sturm, Gewitter, Hitze etc.
        Ohne Ort: alle Warnungen bundesweit.

        Args:
            ort: Stadtname (optional, z.B. "Frankfurt")
            lat: Breitengrad (optional)
            lon: Längengrad (optional)
        """
        resolved_lat, resolved_lon = None, None
        if ort or (lat is not None and lon is not None):
            resolved_lat, resolved_lon = _resolve_coords(ort, lat, lon)

        data = await _brightsky.get_alerts(resolved_lat, resolved_lon)
        alerts = data.get("alerts", [])

        items = []
        for a in alerts[:20]:
            items.append({
                "titel": a.get("headline", ""),
                "beschreibung": a.get("description", ""),
                "schweregrad": a.get("severity", ""),
                "typ": a.get("event", ""),
                "beginn": a.get("onset", ""),
                "ende": a.get("expires", ""),
            })

        return {
            "ort": ort or "bundesweit",
            "anzahl_warnungen": len(alerts),
            "warnungen": items,
        }
