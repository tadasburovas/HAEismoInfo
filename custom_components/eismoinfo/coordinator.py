"""DataUpdateCoordinator for the EismoInfo integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import EismoInfoApiClient, EismoInfoApiError, Station
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, STALE_AFTER

_LOGGER = logging.getLogger(__name__)


class EismoInfoCoordinator(DataUpdateCoordinator[dict[str, Station]]):
    """Coordinator that fetches all weather stations in a single request.

    A single instance is shared by every config entry because the upstream
    API always returns the full list of stations regardless of any query
    parameters.
    """

    def __init__(self, hass: HomeAssistant, client: EismoInfoApiClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Shared by all config entries, so it is not owned by any one of
            # them (otherwise unloading that entry would shut it down).
            config_entry=None,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self._client = client
        # When each station was last present in a successful API response.
        self._last_seen: dict[str, datetime] = {}

    async def _async_update_data(self) -> dict[str, Station]:
        """Fetch the latest data for all stations.

        Failed, empty or partial responses are tolerated: a station keeps its
        last known values until STALE_AFTER has passed since it was last seen,
        and only then drops out of the data (its entities become unavailable).
        """
        now = dt_util.utcnow()
        error: EismoInfoApiError | None = None
        try:
            fresh = await self._client.async_get_stations()
        except EismoInfoApiError as err:
            fresh = {}
            error = err

        for station_id in fresh:
            self._last_seen[station_id] = now

        data = dict(fresh)
        for station_id, station in (self.data or {}).items():
            if station_id in data:
                continue
            if now - self._last_seen.get(station_id, now) < STALE_AFTER:
                data[station_id] = station
            else:
                self._last_seen.pop(station_id, None)

        if error is not None:
            if not data:
                raise UpdateFailed(
                    f"Error communicating with eismoinfo.lt: {error}"
                ) from error
            _LOGGER.warning(
                "eismoinfo.lt update failed (%s); keeping last known data for up to %s",
                error,
                STALE_AFTER,
            )
        return data
