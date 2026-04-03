"""Energiepreise-Tools — Deutsche Strom- und Gaspreise via SMARD."""

from mcp.server.fastmcp import FastMCP

from src.clients.smard import SmardClient

_smard = SmardClient()

# SMARD Filter-IDs fuer Preisdaten
PREIS_FILTER = {
    "strom": {
        "filter_id": 4170,
        "label": "Day-Ahead-Strompreis (Boerse)",
        "einheit": "EUR/MWh",
    },
    "electricity": {
        "filter_id": 4170,
        "label": "Day-Ahead-Strompreis (Boerse)",
        "einheit": "EUR/MWh",
    },
    "gas": {
        "filter_id": 4996,
        "label": "Gasimportpreis (BAFA)",
        "einheit": "EUR/MWh",
    },
}


def register_energiepreise_tools(mcp: FastMCP):
    """Energiepreis-Tools registrieren."""

    @mcp.tool()
    async def get_energy_prices(
        type: str = "electricity",
    ) -> dict:
        """Aktuelle deutsche Energiepreise (Strom, Gas) abrufen.

        Zeigt Boersenpreise fuer Strom (Day-Ahead, EPEX Spot)
        und Gasimportpreise (BAFA). Daten der Bundesnetzagentur (SMARD).

        Args:
            type: Art des Energietraegers.
                - "electricity" oder "strom" — Boersenstrompreis
                - "gas" — Gasimportpreis
        """
        type_lower = type.lower().strip()
        config = PREIS_FILTER.get(type_lower)

        if not config:
            return {
                "error": f"Unbekannter Typ: {type}",
                "verfuegbare_typen": ["electricity", "strom", "gas"],
            }

        try:
            # Tagesdaten abrufen
            data = await _smard.get_chart_data(
                config["filter_id"],
                resolution="day",
            )
            series = data.get("series", [])

            # Letzte Werte mit Daten sammeln (max 14 Tage)
            werte = []
            for ts, val in reversed(series):
                if val is not None:
                    werte.append({
                        "timestamp": ts,
                        "preis": round(val, 2),
                    })
                    if len(werte) >= 14:
                        break

            werte.reverse()

            # Statistik berechnen
            preise = [w["preis"] for w in werte]
            aktuell = preise[-1] if preise else None
            durchschnitt = round(sum(preise) / len(preise), 2) if preise else None
            minimum = min(preise) if preise else None
            maximum = max(preise) if preise else None

            # Trend
            trend = "unbekannt"
            if len(preise) >= 2:
                diff = preise[-1] - preise[-2]
                if diff > 1:
                    trend = f"steigend (+{diff:.1f} {config['einheit']})"
                elif diff < -1:
                    trend = f"fallend ({diff:.1f} {config['einheit']})"
                else:
                    trend = f"stabil ({diff:+.1f} {config['einheit']})"

            return {
                "typ": config["label"],
                "einheit": config["einheit"],
                "aktueller_preis": aktuell,
                "durchschnitt_14_tage": durchschnitt,
                "minimum_14_tage": minimum,
                "maximum_14_tage": maximum,
                "trend": trend,
                "verlauf": werte,
                "quelle": "SMARD / Bundesnetzagentur",
            }
        except Exception as e:
            return {"error": str(e)}
