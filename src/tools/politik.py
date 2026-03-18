"""Politik-Tools — Bundestag-Daten (Drucksachen, Vorgänge, Aktivitäten)."""

from mcp.server.fastmcp import FastMCP

from src.clients.bundestag import BundestagClient

_bundestag = BundestagClient()


def register_politik_tools(mcp: FastMCP):
    """Politik-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def bundestag_suche(
        suchbegriff: str,
        wahlperiode: int = 20,
    ) -> dict:
        """Im Bundestag nach Gesetzentwürfen und Vorgängen suchen.

        Durchsucht Drucksachen und parlamentarische Vorgänge.

        Args:
            suchbegriff: Suchbegriff (z.B. "Klimaschutz", "Digitalisierung")
            wahlperiode: Wahlperiode (20 = aktuell, 19 = vorherige)
        """
        # Vorgänge durchsuchen
        try:
            vorgaenge = await _bundestag.search_vorgaenge(suchbegriff, wahlperiode)
            docs = vorgaenge.get("documents", [])

            items = []
            for v in docs[:15]:
                items.append({
                    "titel": v.get("titel", ""),
                    "typ": v.get("vorgangstyp", ""),
                    "initiative": v.get("initiative", []),
                    "datum": v.get("datum", ""),
                    "abstract": (v.get("abstract", "") or "")[:300],
                })

            return {
                "suchbegriff": suchbegriff,
                "wahlperiode": wahlperiode,
                "anzahl_treffer": vorgaenge.get("numFound", 0),
                "vorgaenge": items,
            }
        except Exception as e:
            return {"error": str(e), "hinweis": "Bundestag DIP API ggf. nicht erreichbar"}

    @mcp.tool()
    async def bundestag_aktivitaeten() -> dict:
        """Letzte parlamentarische Aktivitäten im Bundestag.

        Zeigt aktuelle Debatten, Abstimmungen und Beschlüsse.
        """
        try:
            data = await _bundestag.get_aktivitaeten()
            docs = data.get("documents", [])

            items = []
            for a in docs[:15]:
                items.append({
                    "titel": a.get("titel", ""),
                    "typ": a.get("aktivitaetsart", ""),
                    "datum": a.get("datum", ""),
                    "fundstelle": a.get("fundstelle", {}).get("pdf_url", ""),
                })

            return {
                "anzahl": len(items),
                "aktivitaeten": items,
            }
        except Exception as e:
            return {"error": str(e)}
