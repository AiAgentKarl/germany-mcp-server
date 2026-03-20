# Germany MCP Server

MCP-Server der AI-Agents Zugriff auf deutsche Behörden-Daten gibt — Autobahn-Verkehr, Wetter, Katastrophenwarnungen, Energiemarkt, Bundestag und Pollenflug.

[![germany-mcp-server MCP server](https://glama.ai/mcp/servers/AiAgentKarl/germany-mcp-server/badges/card.svg)](https://glama.ai/mcp/servers/AiAgentKarl/germany-mcp-server)

## 16 Tools in 10 Kategorien

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

### DWD-Wetterwarnungen (NEU v0.2.0)
- `get_german_weather_warnings` — Amtliche Wetterwarnungen (Sturm, Gewitter, Starkregen, Hitze etc.)

### Energiepreise (NEU v0.2.0)
- `get_energy_prices` — Strom-/Gaspreise (Day-Ahead Börse, BAFA Gasimport)

### Statistik (NEU v0.2.0)
- `get_destatis_data` — Offizielle Destatis-Statistiken (BIP, Bevölkerung, Inflation, Arbeitslosigkeit)

### Recht (NEU v0.2.0)
- `search_german_laws` — 6000+ Bundesgesetze durchsuchen (gesetze-im-internet.de)

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
| DWD Warnungen | dwd.de | Amtliche Wetterwarnungen |
| Eurostat/Destatis | ec.europa.eu/eurostat | BIP, Bevölkerung, Inflation |
| Gesetze | gesetze-im-internet.de | 6000+ Bundesgesetze |

## Optionale API-Keys

```bash
# Bundestag DIP API (kostenlos registrierbar bei dip.bundestag.de)
BUNDESTAG_API_KEY=dein-key-hier
```

## Lizenz

MIT

---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| 🔗 Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| 🌍 Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| 🔒 Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| 🤖 Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) |
| 🔬 Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) |

[→ Full catalog (55+ servers)](https://github.com/AiAgentKarl)
