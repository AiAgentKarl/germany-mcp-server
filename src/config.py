"""Konfiguration — lädt optionale API-Keys und stellt Settings bereit."""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env oder keys.env aus dem Projektverzeichnis laden
_project_root = Path(__file__).resolve().parent.parent
_env_path = _project_root / "keys.env"
if not _env_path.exists():
    _env_path = _project_root / ".env"
load_dotenv(_env_path)


class Settings:
    """Zentrale Konfiguration für alle API-Clients.

    Die meisten deutschen Behörden-APIs brauchen KEINEN API-Key.
    Nur Bundestag DIP und Destatis Genesis brauchen Registration.
    """

    # Autobahn (Staus, Baustellen, Webcams, Ladestationen)
    autobahn_base_url: str = "https://verkehr.autobahn.de/o/autobahn"

    # Bright Sky (DWD Wetter — inoffizielle aber stabile JSON-API)
    brightsky_base_url: str = "https://api.brightsky.dev"

    # NINA (Warnungen — Katastrophenschutz, BBK)
    nina_base_url: str = "https://warnung.bund.de/api31"

    # SMARD (Energiemarkt — Bundesnetzagentur)
    smard_base_url: str = "https://www.smard.de/app/chart_data"

    # Bundestag DIP (Drucksachen, Abgeordnete, Plenarprotokolle)
    bundestag_api_key: str = os.getenv("BUNDESTAG_API_KEY", "")
    bundestag_base_url: str = "https://search.dip.bundestag.de/api/v1"

    # Lebensmittelwarnungen (Bayern/Bund Portal)
    food_warnings_base_url: str = "https://megov.bayern.de/verbraucherschutz/baystmuv-verbraucherschutz/rest/api"

    # Pollenflug (DWD Open Data)
    pollen_base_url: str = "https://opendata.dwd.de/climate_environment/health/alerts"

    # Eurostat (offizielle Destatis-Daten als freie JSON-API)
    eurostat_base_url: str = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0"

    # Gesetze-im-Internet (BMJ — Bundesgesetze)
    gesetze_base_url: str = "https://www.gesetze-im-internet.de"

    # DWD Wetterwarnungen (JSONP-Endpoint)
    dwd_warnings_url: str = "https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json"

    # HTTP-Client Defaults
    http_timeout: float = 30.0


# Globale Settings-Instanz
settings = Settings()
