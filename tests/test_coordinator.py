"""Tests for the shared coordinator's outage tolerance."""

from __future__ import annotations

from datetime import timedelta

import aiohttp
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_time_changed,
)

from custom_components.eismoinfo.const import (
    API_URL,
    CONF_SCAN_INTERVAL,
    CONF_STATION_ID,
    DOMAIN,
    STALE_AFTER,
)


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


def _entry_air_temp(hass, entry):
    """Return the air temperature state of one specific station entry."""
    registry = er.async_get(hass)
    entity_id = next(
        e.entity_id
        for e in er.async_entries_for_config_entry(registry, entry.entry_id)
        if e.entity_id.endswith("_air_temperature")
    )
    return hass.states.get(entity_id)


def _entry_for(hass, station_id: str):
    return next(
        e
        for e in hass.config_entries.async_entries(DOMAIN)
        if e.data[CONF_STATION_ID] == station_id
    )


def _payload_with_temp(stations_payload, station_id: str, temp: str):
    return [
        {**s, "oro_temperatura": temp} if s["id"] == station_id else s
        for s in stations_payload
    ]


async def test_unloading_first_entry_keeps_other_station_polling(
    hass, aioclient_mock, stations_payload, freezer
):
    """Unloading the entry that created the shared coordinator must not stop polling."""
    aioclient_mock.get(API_URL, json=stations_payload)
    await _add_station(hass, "206")
    await _add_station(hass, "157")
    other = _entry_for(hass, "157")
    assert _entry_air_temp(hass, other).state == "17.4"

    await hass.config_entries.async_unload(_entry_for(hass, "206").entry_id)
    await hass.async_block_till_done()

    aioclient_mock.clear_requests()
    aioclient_mock.get(API_URL, json=_payload_with_temp(stations_payload, "157", "3.2"))
    await _poll(hass, freezer, timedelta(minutes=6))

    assert _entry_air_temp(hass, other).state == "3.2"


async def test_options_change_keeps_other_station_polling(
    hass, aioclient_mock, stations_payload, freezer
):
    """Changing options (entry reload) on one station must not freeze the others."""
    aioclient_mock.get(API_URL, json=stations_payload)
    await _add_station(hass, "206")
    await _add_station(hass, "157")
    first = _entry_for(hass, "206")
    other = _entry_for(hass, "157")

    hass.config_entries.async_update_entry(
        first, options={**first.options, CONF_SCAN_INTERVAL: 600}
    )
    await hass.async_block_till_done()

    aioclient_mock.clear_requests()
    aioclient_mock.get(API_URL, json=_payload_with_temp(stations_payload, "157", "4.4"))
    await _poll(hass, freezer, timedelta(minutes=11))

    assert _entry_air_temp(hass, other).state == "4.4"


async def test_last_entry_unload_shuts_coordinator_down(
    hass, aioclient_mock, stations_payload
):
    """Unloading the final entry drops and shuts down the shared coordinator."""
    aioclient_mock.get(API_URL, json=stations_payload)
    await _add_station(hass, "206")
    coordinator = hass.data[DOMAIN]["coordinator"]

    await hass.config_entries.async_unload(_entry_for(hass, "206").entry_id)
    await hass.async_block_till_done()

    assert DOMAIN not in hass.data
    assert coordinator._shutdown_requested


async def test_setup_not_ready_when_api_down(hass, aioclient_mock):
    """A failing first fetch puts the entry into setup-retry and leaves no coordinator."""
    aioclient_mock.get(API_URL, exc=aiohttp.ClientError("boom"))
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_STATION_ID: "206"},
        unique_id="206",
        options={},
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert "coordinator" not in hass.data.get(DOMAIN, {})
