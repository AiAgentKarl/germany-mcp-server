"""DWD-Warnungen-Tools — Offizielle Wetterwarnungen des Deutschen Wetterdienstes."""

from mcp.server.fastmcp import FastMCP

from src.clients.dwd_warnings import DwdWarningsClient, WARN_LEVELS

_dwd = DwdWarningsClient()


def register_dwd_warnungen_tools(mcp: FastMCP):
    """DWD-Warnungs-Tools registrieren."""

    @mcp.tool()
    async def get_german_weather_warnings(
        region: str = "",
    ) -> dict:
        """Aktuelle Wetterwarnungen vom Deutschen Wetterdienst (DWD).

        Zeigt amtliche Warnungen: Sturm, Gewitter, Starkregen, Hitze,
        Frost, Glatteis, Schneefall etc. Direkt vom DWD.

        Args:
            region: Bundesland oder Region zum Filtern
                (z.B. "Bayern", "NRW", "Sachsen", "Berlin").
                Leer = alle Warnungen bundesweit.
        """
        try:
            data = await _dwd.get_warnings(region or None)
            warnungen_raw = data.get("warnungen", [])

            # Deduplizieren nach headline+regionName (DWD liefert Dopplungen)
            seen = set()
            items = []
            for w in warnungen_raw:
                key = f"{w.get('headline', '')}-{w.get('regionName', '')}"
                if key in seen:
                    continue
                seen.add(key)

                level = w.get("level", 0)
                items.append({
                    "ueberschrift": w.get("headline", ""),
                    "ereignis": w.get("event", ""),
                    "beschreibung": w.get("description", ""),
                    "schweregrad": WARN_LEVELS.get(level, f"Stufe {level}"),
                    "level": level,
                    "region": w.get("regionName", ""),
                    "bundesland": w.get("state", ""),
                    "beginn": w.get("start"),
                    "ende": w.get("end"),
                    "handlungsempfehlung": w.get("instruction", ""),
                    "hoehe_ab_m": w.get("altitudeStart"),
                    "vorab_info": w.get("_vorab", False),
                })

            # Nach Schweregrad sortieren (schlimmste zuerst)
            items.sort(key=lambda x: x.get("level", 0), reverse=True)

            # Statistik
            nach_level = {}
            for item in items:
                lvl_name = item["schweregrad"]
                nach_level[lvl_name] = nach_level.get(lvl_name, 0) + 1

            return {
                "region": region or "bundesweit",
                "anzahl_warnungen": len(items),
                "nach_schweregrad": nach_level,
                "warnungen": items[:50],  # Max 50 Warnungen zurueckgeben
                "quelle": "Deutscher Wetterdienst (DWD)",
            }
        except Exception as e:
            return {"error": str(e)}
