"""Energie-Tools — SMARD Energiemarktdaten (Bundesnetzagentur)."""

from mcp.server.fastmcp import FastMCP

from src.clients.smard import SmardClient, SMARD_FILTERS

_smard = SmardClient()


def register_energie_tools(mcp: FastMCP):
    """Energie-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def strom_erzeugung() -> dict:
        """Aktuelle Stromerzeugung in Deutschland nach Energieträger.

        Zeigt wie viel Strom gerade aus Wind, Solar, Kohle, Gas etc.
        erzeugt wird. Daten der Bundesnetzagentur (SMARD).
        """
        ergebnisse = {}

        # Wichtigste Energieträger abfragen
        wichtige = {
            "wind_onshore": 4067,
            "wind_offshore": 1225,
            "photovoltaik": 4068,
            "biomasse": 4169,
            "wasserkraft": 4070,
            "braunkohle": 1223,
            "steinkohle": 4071,
            "erdgas": 4072,
            "kernenergie": 1224,
        }

        for name, filter_id in wichtige.items():
            try:
                data = await _smard.get_chart_data(filter_id, resolution="day")
                series = data.get("series", [])
                # Letzten Wert nehmen der nicht None ist
                last_value = None
                last_timestamp = None
                for ts, val in reversed(series):
                    if val is not None:
                        last_value = val
                        last_timestamp = ts
                        break
                ergebnisse[name] = {
                    "mwh": last_value,
                    "timestamp": last_timestamp,
                }
            except Exception:
                ergebnisse[name] = {"mwh": None, "error": "Daten nicht verfügbar"}

        # Erneuerbare vs. Konventionelle berechnen
        erneuerbare = sum(
            v.get("mwh", 0) or 0
            for k, v in ergebnisse.items()
            if k in ("wind_onshore", "wind_offshore", "photovoltaik", "biomasse", "wasserkraft")
        )
        konventionelle = sum(
            v.get("mwh", 0) or 0
            for k, v in ergebnisse.items()
            if k in ("braunkohle", "steinkohle", "erdgas", "kernenergie")
        )
        gesamt = erneuerbare + konventionelle

        return {
            "erzeugung_nach_traeger": ergebnisse,
            "erneuerbare_mwh": erneuerbare,
            "konventionelle_mwh": konventionelle,
            "gesamt_mwh": gesamt,
            "erneuerbare_anteil_pct": round(erneuerbare / gesamt * 100, 1) if gesamt > 0 else 0,
        }

    @mcp.tool()
    async def stromverbrauch() -> dict:
        """Aktueller Stromverbrauch in Deutschland.

        Zeigt den Gesamtverbrauch und Trend. Daten der Bundesnetzagentur.
        """
        try:
            data = await _smard.get_chart_data(410, resolution="day")
            series = data.get("series", [])

            # Letzte Werte mit Daten
            recent = []
            for ts, val in reversed(series):
                if val is not None:
                    recent.append({"timestamp": ts, "mwh": val})
                    if len(recent) >= 7:
                        break

            recent.reverse()

            return {
                "letzte_werte": recent,
                "aktuell_mwh": recent[-1]["mwh"] if recent else None,
                "trend": _berechne_trend(recent),
            }
        except Exception as e:
            return {"error": str(e)}


def _berechne_trend(werte: list[dict]) -> str:
    """Einfachen Trend aus den letzten Werten berechnen."""
    if len(werte) < 2:
        return "unbekannt"
    aktuell = werte[-1].get("mwh", 0) or 0
    vorher = werte[-2].get("mwh", 0) or 0
    if vorher == 0:
        return "unbekannt"
    diff_pct = ((aktuell - vorher) / vorher) * 100
    if diff_pct > 5:
        return f"steigend ({diff_pct:+.1f}%)"
    elif diff_pct < -5:
        return f"fallend ({diff_pct:+.1f}%)"
    return f"stabil ({diff_pct:+.1f}%)"
