"""Verkehr-Tools — Autobahn-Daten (Staus, Baustellen, Sperrungen)."""

from mcp.server.fastmcp import FastMCP

from src.clients.autobahn import AutobahnClient

_autobahn = AutobahnClient()

# Bekannte Autobahnen für Schnellzugriff
MAJOR_AUTOBAHNS = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]


def register_verkehr_tools(mcp: FastMCP):
    """Verkehr-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def autobahn_baustellen(autobahn: str = "A1") -> dict:
        """Aktuelle Baustellen auf einer deutschen Autobahn abrufen.

        Zeigt alle aktuellen Baustellen mit Ort, Richtung und Details.

        Args:
            autobahn: Autobahn-Bezeichnung (z.B. "A1", "A7", "A61")
        """
        road = autobahn.upper()
        roadworks = await _autobahn.get_roadworks(road)

        items = []
        for rw in roadworks[:20]:
            items.append({
                "titel": rw.get("title", ""),
                "beschreibung": rw.get("subtitle", ""),
                "auswirkung": rw.get("display_type", ""),
                "ort": rw.get("point", ""),
                "startzeit": rw.get("startTimestamp", ""),
            })

        return {
            "autobahn": road,
            "anzahl_baustellen": len(roadworks),
            "baustellen": items,
        }

    @mcp.tool()
    async def autobahn_warnungen(autobahn: str = "A1") -> dict:
        """Aktuelle Verkehrswarnungen auf einer Autobahn.

        Zeigt Staus, Unfälle und Verkehrsbehinderungen.

        Args:
            autobahn: Autobahn-Bezeichnung (z.B. "A3", "A9")
        """
        road = autobahn.upper()
        warnings = await _autobahn.get_warnings(road)

        items = []
        for w in warnings[:20]:
            items.append({
                "titel": w.get("title", ""),
                "beschreibung": w.get("subtitle", ""),
                "typ": w.get("display_type", ""),
                "ort": w.get("point", ""),
            })

        return {
            "autobahn": road,
            "anzahl_warnungen": len(warnings),
            "warnungen": items,
        }

    @mcp.tool()
    async def autobahn_sperrungen(autobahn: str = "A1") -> dict:
        """Aktuelle Sperrungen auf einer Autobahn.

        Args:
            autobahn: Autobahn-Bezeichnung (z.B. "A5", "A8")
        """
        road = autobahn.upper()
        closures = await _autobahn.get_closures(road)

        items = []
        for c in closures[:20]:
            items.append({
                "titel": c.get("title", ""),
                "beschreibung": c.get("subtitle", ""),
                "ort": c.get("point", ""),
            })

        return {
            "autobahn": road,
            "anzahl_sperrungen": len(closures),
            "sperrungen": items,
        }

    @mcp.tool()
    async def autobahn_ladestationen(autobahn: str = "A1") -> dict:
        """E-Auto-Ladestationen entlang einer Autobahn finden.

        Args:
            autobahn: Autobahn-Bezeichnung (z.B. "A2", "A7")
        """
        road = autobahn.upper()
        stations = await _autobahn.get_charging_stations(road)

        items = []
        for s in stations[:30]:
            items.append({
                "titel": s.get("title", ""),
                "beschreibung": s.get("subtitle", ""),
                "ort": s.get("point", ""),
            })

        return {
            "autobahn": road,
            "anzahl_ladestationen": len(stations),
            "ladestationen": items,
        }
