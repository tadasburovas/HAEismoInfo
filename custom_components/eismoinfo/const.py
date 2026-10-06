"""Constants for the EismoInfo integration."""

from __future__ import annotations

from datetime import timedelta
from typing import Final

DOMAIN: Final = "eismoinfo"

API_URL: Final = "https://eismoinfo.lt/weather-conditions-service"

CONF_STATION_ID: Final = "station_id"
CONF_CUSTOM_NAME: Final = "custom_name"
CONF_SCAN_INTERVAL: Final = "scan_interval"

DEFAULT_SCAN_INTERVAL: Final = 300  # seconds
MIN_SCAN_INTERVAL: Final = 60
MAX_SCAN_INTERVAL: Final = 3600

# A station keeps its last known values (and stays available) for this long
# after it was last present in a successful API response. Covers eismoinfo.lt
# outages, empty or partial responses; only after this does it go unavailable.
STALE_AFTER: Final = timedelta(hours=1)

MANUFACTURER: Final = "Lietuvos automobilių kelių direkcija"
MODEL: Final = "Kelių orų stotelė"
