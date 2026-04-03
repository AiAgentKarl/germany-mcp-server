"""Statistik-Tools — Offizielle deutsche Statistikdaten (Destatis via Eurostat)."""

from mcp.server.fastmcp import FastMCP

from src.clients.destatis import DestatisClient, INDICATORS

_destatis = DestatisClient()


def register_statistik_tools(mcp: FastMCP):
    """Statistik-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def get_destatis_data(
        indicator: str = "bevoelkerung",
        year: int | None = None,
    ) -> dict:
        """Offizielle deutsche Statistikdaten von Destatis abrufen.

        Verfuegbare Indikatoren: bevoelkerung, bip, bip_pro_kopf,
        arbeitslosigkeit, inflation, inflation_index, erwerbstaetigkeit.

        Daten stammen vom Statistischen Bundesamt (via Eurostat).

        Args:
            indicator: Statistik-Indikator. Moegliche Werte:
                - "bevoelkerung" — Einwohnerzahl Deutschland
                - "bip" — Bruttoinlandsprodukt (nominal, Mio. EUR)
                - "bip_pro_kopf" — BIP pro Kopf (EUR)
                - "arbeitslosigkeit" — Arbeitslosenquote (%)
                - "inflation" — Inflationsrate (HVPI, %)
                - "inflation_index" — Verbraucherpreisindex (2015=100)
                - "erwerbstaetigkeit" — Erwerbstaetigenquote 20-64 (%)
            year: Optionales Jahr (z.B. 2023). Ohne = letzte 5 Jahre.
        """
        try:
            data = await _destatis.get_indicator(indicator, year)

            if "error" in data:
                return data

            # Letzten Wert hervorheben
            daten = data.get("daten", {})
            letztes_jahr = None
            letzter_wert = None
            if daten:
                letztes_jahr = max(daten.keys())
                letzter_wert = daten[letztes_jahr]

            return {
                "indikator": data["indikator"],
                "einheit": data["einheit"],
                "aktuellster_wert": letzter_wert,
                "aktuellstes_jahr": letztes_jahr,
                "zeitreihe": daten,
                "quelle": data["quelle"],
            }
        except Exception as e:
            return {
                "error": str(e),
                "verfuegbare_indikatoren": list(INDICATORS.keys()),
            }
