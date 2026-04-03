# Germany MCP Server

MCP-Server der AI-Agents Zugriff auf deutsche Behörden-Daten gibt — 16 Tools in 10 Kategorien, alles kostenlos und ohne API-Key nutzbar.

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

### DWD-Wetterwarnungen (NEU in v0.2.0)
- `get_german_weather_warnings` — Amtliche Wetterwarnungen direkt vom DWD (Sturm, Starkregen, Glatteis, Hitze). Filtern nach Bundesland möglich.

### Katastrophenwarnungen
- `nina_warnungen` — NINA/BBK: Hochwasser, Unwetter, Stromausfälle, Brände

### Energie (SMARD)
- `strom_erzeugung` — Stromerzeugung nach Energieträger (Wind, Solar, Kohle, Gas)
- `stromverbrauch` — Aktueller Stromverbrauch und Trend

### Energiepreise (NEU in v0.2.0)
- `get_energy_prices` — Aktuelle Strom- und Gaspreise (Day-Ahead-Börsenpreis, Gasimportpreis). 14-Tage-Verlauf mit Trend.

### Politik (Bundestag)
- `bundestag_suche` — Gesetzentwürfe und Vorgänge durchsuchen
- `bundestag_aktivitaeten` — Letzte parlamentarische Aktivitäten

### Gesundheit
- `pollenflug` — Pollenflug-Vorhersage für 27 Regionen (Birke, Gräser, Hasel etc.)

### Statistik (NEU in v0.2.0)
- `get_destatis_data` — Offizielle Destatis-Statistiken: Bevölkerung, BIP, Arbeitslosenquote, Inflation, Erwerbstätigkeit. Zeitreihen ab 2020.

### Recht (NEU in v0.2.0)
- `search_german_laws` — 6000+ Bundesgesetze durchsuchen (Titel, Abkürzung). Direkt-Links zu gesetze-im-internet.de.

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

## Beispiel-Abfragen

```
"Wie ist das Wetter in München?"
"Gibt es Unwetterwarnungen in Bayern?"
"Zeig mir die Arbeitslosenquote der letzten 5 Jahre"
"Suche nach Gesetzen zum Thema Datenschutz"
"Was ist der aktuelle Börsenstrompreis?"
"Gibt es Baustellen auf der A7?"
"Wie hoch ist die aktuelle Pollenbelastung in NRW?"
"Zeig mir das BIP pro Kopf für 2023"
```

## Datenquellen

Alle APIs sind **kostenlos und ohne API-Key** nutzbar (Bundestag optional mit Key):

| API | Quelle | Daten |
|-----|--------|-------|
| Autobahn | verkehr.autobahn.de | Verkehr, Baustellen, Ladestationen |
| Bright Sky | brightsky.dev (DWD) | Wetter, Temperatur, Niederschlag |
| DWD Warnungen | dwd.de | Amtliche Wetterwarnungen |
| NINA | warnung.bund.de | Katastrophenwarnungen (5 Kanäle) |
| SMARD | smard.de | Energiemarkt, Stromerzeugung, Preise |
| Bundestag DIP | dip.bundestag.de | Parlamentarische Daten |
| DWD Pollenflug | opendata.dwd.de | Pollenbelastung, 27 Regionen |
| Eurostat/Destatis | ec.europa.eu/eurostat | BIP, Bevölkerung, Inflation, Arbeitsmarkt |
| Gesetze-im-Internet | gesetze-im-internet.de | 6000+ Bundesgesetze und Verordnungen |

## Optionale API-Keys

```bash
# Bundestag DIP API (kostenlos registrierbar bei dip.bundestag.de)
BUNDESTAG_API_KEY=dein-key-hier
```

## Changelog

### v0.2.0 (April 2026)
- 4 neue Tools: `get_destatis_data`, `search_german_laws`, `get_german_weather_warnings`, `get_energy_prices`
- 3 neue Clients: Destatis/Eurostat, Gesetze-im-Internet, DWD-Warnungen
- Energiepreise-Modul (Strom- und Gaspreise)
- 16 Tools in 10 Kategorien (vorher 12 in 6)

### v0.1.2
- Initiale Version mit 12 Tools

## Lizenz

MIT

---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Fraud Prevention](https://github.com/AiAgentKarl/fraud-prevention-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) · [Insurance](https://github.com/AiAgentKarl/agent-insurance-mcp-server) |
| Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) · [Patent](https://github.com/AiAgentKarl/patent-mcp-server) |

[Full catalog (55+ servers)](https://github.com/AiAgentKarl)
