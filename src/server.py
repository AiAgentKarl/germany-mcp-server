"""Germany MCP Server — Deutsche Behoerden-Daten fuer AI-Agents.

Buendelt 10 kostenlose deutsche APIs:
- Autobahn (Staus, Baustellen, Sperrungen, Ladestationen)
- Wetter (DWD via Bright Sky)
- DWD-Wetterwarnungen (Sturm, Gewitter, Starkregen etc.)
- NINA Katastrophenwarnungen
- Energiemarkt (SMARD/Bundesnetzagentur)
- Energiepreise (Strom-/Gaspreise via SMARD)
- Bundestag (Drucksachen, Vorgaenge)
- Pollenflug (DWD)
- Statistik (Destatis via Eurostat — BIP, Bevoelkerung, Inflation)
- Bundesgesetze (gesetze-im-internet.de — 6000+ Gesetze)
"""

from mcp.server.fastmcp import FastMCP

from src.tools.verkehr import register_verkehr_tools
from src.tools.wetter import register_wetter_tools
from src.tools.warnungen import register_warnungen_tools
from src.tools.dwd_warnungen import register_dwd_warnungen_tools
from src.tools.energie import register_energie_tools
from src.tools.energiepreise import register_energiepreise_tools
from src.tools.politik import register_politik_tools
from src.tools.gesundheit import register_gesundheit_tools
from src.tools.statistik import register_statistik_tools
from src.tools.recht import register_recht_tools

# FastMCP Server erstellen
mcp = FastMCP(
    "Germany MCP Server",
    instructions=(
        "Gibt AI-Agents Zugriff auf deutsche Behoerden-Daten: "
        "Autobahn-Verkehr, Wetter, DWD-Wetterwarnungen, Katastrophenwarnungen, "
        "Energiemarkt, Energiepreise, Bundestag, Pollenflug, "
        "Destatis-Statistiken und Bundesgesetze."
    ),
)

# Alle Tool-Gruppen registrieren
register_verkehr_tools(mcp)
register_wetter_tools(mcp)
register_warnungen_tools(mcp)
register_dwd_warnungen_tools(mcp)
register_energie_tools(mcp)
register_energiepreise_tools(mcp)
register_politik_tools(mcp)
register_gesundheit_tools(mcp)
register_statistik_tools(mcp)
register_recht_tools(mcp)


def main():
    """Server starten."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
