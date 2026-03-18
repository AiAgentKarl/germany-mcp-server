"""Germany MCP Server — Deutsche Behörden-Daten für AI-Agents.

Bündelt 6 kostenlose deutsche APIs:
- Autobahn (Staus, Baustellen, Sperrungen, Ladestationen)
- Wetter (DWD via Bright Sky)
- NINA Katastrophenwarnungen
- Energiemarkt (SMARD/Bundesnetzagentur)
- Bundestag (Drucksachen, Vorgänge)
- Pollenflug (DWD)
"""

from mcp.server.fastmcp import FastMCP

from src.tools.verkehr import register_verkehr_tools
from src.tools.wetter import register_wetter_tools
from src.tools.warnungen import register_warnungen_tools
from src.tools.energie import register_energie_tools
from src.tools.politik import register_politik_tools
from src.tools.gesundheit import register_gesundheit_tools

# FastMCP Server erstellen
mcp = FastMCP(
    "Germany MCP Server",
    instructions=(
        "Gibt AI-Agents Zugriff auf deutsche Behörden-Daten: "
        "Autobahn-Verkehr, Wetter, Katastrophenwarnungen, "
        "Energiemarkt, Bundestag und Pollenflug."
    ),
)

# Alle Tool-Gruppen registrieren
register_verkehr_tools(mcp)
register_wetter_tools(mcp)
register_warnungen_tools(mcp)
register_energie_tools(mcp)
register_politik_tools(mcp)
register_gesundheit_tools(mcp)


if __name__ == "__main__":
    mcp.run()
