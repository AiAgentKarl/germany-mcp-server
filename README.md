# Germany MCP Server

MCP-Server der AI-Agents Zugriff auf deutsche Behörden-Daten gibt — Autobahn-Verkehr, Wetter, Katastrophenwarnungen, Energiemarkt, Bundestag und Pollenflug.

## 12 Tools in 6 Kategorien

### Verkehr (Autobahn)
- `autobahn_baustellen` — Aktuelle Baustellen auf einer Autobahn
- `autobahn_warnungen` — Staus und Verkehrswarnungen
- `autobahn_sperrungen` — Gesperrte Abschnitte
- `autobahn_ladestationen` — E-Auto-Ladestationen entlang einer Autobahn

### Wetter (DWD)
- `wetter_aktuell` — Aktuelles Wetter an einem Ort (30+ deutsche Städte vordefiniert)
- `wetter_warnungen` — DWD-Unwetterwarnungen (Sturm, Gewitter, Hitze etc.)

### Katastrophenwarnungen
- `nina_warnungen` — NINA/BBK: Hochwasser, Unwetter, Stromausfälle, Brände

### Energie (SMARD)
- `strom_erzeugung` — Stromerzeugung nach Energieträger (Wind, Solar, Kohle, Gas)
- `stromverbrauch` — Aktueller Stromverbrauch und Trend

### Politik (Bundestag)
- `bundestag_suche` — Gesetzentwürfe und Vorgänge durchsuchen
- `bundestag_aktivitaeten` — Letzte parlamentarische Aktivitäten

### Gesundheit
- `pollenflug` — Pollenflug-Vorhersage für 27 Regionen (Birke, Gräser, Hasel etc.)

## Installation

```bash
pip install germany-mcp-server
```

Oder direkt von GitHub:

```bash
pip install git+https://github.com/AiAgentKarl/germany-mcp-server.git
```

## Nutzung mit Claude Code

`.mcp.json` im Projektverzeichnis:

```json
{
  "mcpServers": {
    "germany": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "src.server"]
    }
  }
}
```

Alternativ mit `uvx` (kein lokales Install nötig):

```json
{
  "mcpServers": {
    "germany": {
      "type": "stdio",
      "command": "uvx",
      "args": ["germany-mcp-server"]
    }
  }
}
```

## Datenquellen

Alle APIs sind **kostenlos und ohne API-Key** nutzbar (Bundestag optional mit Key):

| API | Quelle | Daten |
|-----|--------|-------|
| Autobahn | verkehr.autobahn.de | Verkehr, Baustellen, Ladestationen |
| Bright Sky | brightsky.dev (DWD) | Wetter, Temperatur, Niederschlag |
| NINA | warnung.bund.de | Katastrophenwarnungen (5 Kanäle) |
| SMARD | smard.de | Energiemarkt, Stromerzeugung |
| Bundestag DIP | dip.bundestag.de | Parlamentarische Daten |
| DWD Pollenflug | opendata.dwd.de | Pollenbelastung, 27 Regionen |

## Optionale API-Keys

```bash
# Bundestag DIP API (kostenlos registrierbar bei dip.bundestag.de)
BUNDESTAG_API_KEY=dein-key-hier
```

## Lizenz

MIT
