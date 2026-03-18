"""Gesundheit-Tools — Pollenflug-Vorhersage."""

from mcp.server.fastmcp import FastMCP

from src.clients.pollen import PollenClient, POLLEN_LEVELS

_pollen = PollenClient()

# Regionen-Mapping (Region-ID → Name)
REGIONEN = {
    "10": "Schleswig-Holstein und Hamburg",
    "11": "Mecklenburg-Vorpommern",
    "12": "Niedersachsen und Bremen",
    "20": "Nordrhein-Westfalen (Tiefland)",
    "21": "Nordrhein-Westfalen (Mittelgebirge)",
    "30": "Hessen",
    "31": "Rheinland-Pfalz und Saarland",
    "40": "Baden-Württemberg",
    "41": "Bayern (Nord, Franken)",
    "42": "Bayern (Süd)",
    "50": "Brandenburg und Berlin",
    "51": "Sachsen-Anhalt",
    "52": "Thüringen",
    "53": "Sachsen",
}


def register_gesundheit_tools(mcp: FastMCP):
    """Gesundheits-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def pollenflug(region: str = "") -> dict:
        """Aktuelle Pollenflug-Vorhersage für eine Region in Deutschland.

        Zeigt Belastung durch Ambrosia, Birke, Gräser, Hasel etc.
        Vorhersage für heute, morgen und übermorgen.

        Args:
            region: Region oder Bundesland (z.B. "Bayern", "NRW", "Berlin").
                    Leer = alle Regionen.
        """
        data = await _pollen.get_forecast()
        content = data.get("content", [])

        # Region filtern wenn angegeben
        if region:
            region_lower = region.lower()
            content = [
                r for r in content
                if region_lower in (r.get("region_name", "") or "").lower()
                or region_lower in (r.get("partregion_name", "") or "").lower()
            ]

        items = []
        for r in content:
            region_name = r.get("partregion_name") or r.get("region_name", "")
            pollen = r.get("Pollen", {})

            pollen_daten = {}
            for pollenart, werte in pollen.items():
                heute = werte.get("today", "-1")
                morgen = werte.get("tomorrow", "-1")
                uebermorgen = werte.get("dayafter_to", "-1")
                pollen_daten[pollenart] = {
                    "heute": POLLEN_LEVELS.get(str(heute), "unbekannt"),
                    "morgen": POLLEN_LEVELS.get(str(morgen), "unbekannt"),
                    "uebermorgen": POLLEN_LEVELS.get(str(uebermorgen), "unbekannt"),
                }

            items.append({
                "region": region_name,
                "pollen": pollen_daten,
            })

        aktualisiert = data.get("last_update", "")

        return {
            "aktualisiert": aktualisiert,
            "anzahl_regionen": len(items),
            "regionen": items,
        }
