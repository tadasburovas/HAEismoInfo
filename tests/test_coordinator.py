"""Tests for the shared coordinator's outage tolerance."""

from __future__ import annotations

from datetime import timedelta

from homeassistant import config_entries
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.eismoinfo.const import API_URL, CONF_STATION_ID, DOMAIN, STALE_AFTER


async def _add_station(hass, station_id: str) -> None:
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_STATION_ID: station_id}
    )
    await hass.async_block_till_done()


def _air_temp_state(hass):
    entity_id = next(
        e for e in hass.states.async_entity_ids("sensor") if e.endswith("_air_temperature")
    )
    return hass.states.get(entity_id)


async def _poll(hass, freezer, delta: timedelta) -> None:
    freezer.tick(delta)
    async_fire_time_changed(hass)
    await hass.async_block_till_done()


async def test_outage_keeps_values_until_stale(
    hass, aioclient_mock, stations_payload, freezer
):
    """Empty/failed responses keep last values; unavailable only after STALE_AFTER."""
    aioclient_mock.get(API_URL, json=stations_payload)
    await _add_station(hass, "206")
    assert _air_temp_state(hass).state == "16.5"

    # API starts returning an empty list (the real-world outage).
    aioclient_mock.clear_requests()
    aioclient_mock.get(API_URL, json=[])

    await _poll(hass, freezer, timedelta(minutes=6))
    assert _air_temp_state(hass).state == "16.5"

    await _poll(hass, freezer, timedelta(minutes=50))
    assert _air_temp_state(hass).state == "16.5"

    await _poll(hass, freezer, STALE_AFTER)
    assert _air_temp_state(hass).state == "unavailable"

    # API recovers.
    aioclient_mock.clear_requests()
    aioclient_mock.get(API_URL, json=stations_payload)
    await _poll(hass, freezer, timedelta(minutes=6))
    assert _air_temp_state(hass).state == "16.5"


async def test_reload_refreshes_stale_coordinator(
    hass, aioclient_mock, stations_payload
):
    """Reloading an entry must refetch when the station is missing from the data."""
    aioclient_mock.get(API_URL, json=stations_payload)
    await _add_station(hass, "206")
    await _add_station(hass, "157")

    coordinator = hass.data[DOMAIN]["coordinator"]
    del coordinator.data["157"]

    entry = next(
        e for e in hass.config_entries.async_entries(DOMAIN)
        if e.data[CONF_STATION_ID] == "157"
    )
    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()

    assert "157" in hass.data[DOMAIN]["coordinator"].data
