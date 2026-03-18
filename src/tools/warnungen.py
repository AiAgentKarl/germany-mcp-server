"""Warnungen-Tools — NINA Katastrophenwarnungen."""

from mcp.server.fastmcp import FastMCP

from src.clients.nina import NinaClient

_nina = NinaClient()


def register_warnungen_tools(mcp: FastMCP):
    """Warnungs-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def nina_warnungen() -> dict:
        """Aktuelle Katastrophen-Warnungen in Deutschland (NINA/BBK).

        Zeigt Hochwasser, Unwetter, Stromausfälle, Brände und andere
        Gefahrenlagen. Quelle: Bundesamt für Bevölkerungsschutz.
        """
        warnings = await _nina.get_warnings()

        items = []
        for w in warnings[:30]:
            payload = w.get("payload", {})
            data_list = payload.get("data", {})
            headline = ""
            area = ""

            if isinstance(data_list, dict):
                headline = data_list.get("headline", "")
                area = data_list.get("area", {}).get("description", "")

            items.append({
                "id": w.get("id", ""),
                "titel": headline or w.get("i18nTitle", {}).get("de", ""),
                "kanal": w.get("_channel", ""),
                "typ": payload.get("type", ""),
                "schweregrad": payload.get("severity", ""),
                "gebiet": area,
                "gesendet": payload.get("sent", ""),
            })

        return {
            "anzahl_warnungen": len(warnings),
            "warnungen": items,
        }
