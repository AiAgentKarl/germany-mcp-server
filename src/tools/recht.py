"""Recht-Tools — Deutsche Bundesgesetze durchsuchen."""

from mcp.server.fastmcp import FastMCP

from src.clients.gesetze import GesetzeClient

_gesetze = GesetzeClient()


def register_recht_tools(mcp: FastMCP):
    """Rechts-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def search_german_laws(
        query: str,
        limit: int = 10,
    ) -> dict:
        """Deutsche Bundesgesetze durchsuchen (gesetze-im-internet.de).

        Durchsucht alle 6000+ Bundesgesetze und Verordnungen nach Titel.
        Man kann auch Abkuerzungen nutzen (z.B. "gg", "stgb", "bgb").

        Args:
            query: Suchbegriff oder Abkuerzung
                (z.B. "Grundgesetz", "Mietrecht", "bgb", "Datenschutz")
            limit: Max. Ergebnisse (Standard: 10, Max: 50)
        """
        limit = min(limit, 50)

        try:
            treffer = await _gesetze.search(query, limit)
            gesamt = await _gesetze.get_law_count()

            items = []
            for t in treffer:
                items.append({
                    "titel": t["titel"],
                    "abkuerzung": t["abkuerzung"],
                    "url": t["url"],
                })

            return {
                "suchbegriff": query,
                "anzahl_treffer": len(items),
                "gesetze_gesamt": gesamt,
                "treffer": items,
                "quelle": "gesetze-im-internet.de (BMJ)",
            }
        except Exception as e:
            return {"error": str(e)}
