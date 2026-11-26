# Eismo Info – Lithuanian road weather stations for Home Assistant

[![Validate](https://github.com/triumfas/HAEismoInfo/actions/workflows/validate.yml/badge.svg)](https://github.com/triumfas/HAEismoInfo/actions/workflows/validate.yml)
[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=triumfas&repository=HAEismoInfo&category=integration)

> 🇱🇹 **Lithuania only.** This integration uses the public [eismoinfo.lt](https://eismoinfo.lt) API
> – the road traffic information service of the **Lithuanian Road Administration
> (Lietuvos automobilių kelių direkcija)**. It only covers weather stations on **Lithuanian
> roads** and is not useful outside Lithuania. 🇱🇹 Lietuviškas aprašymas – [žemiau](#lietuviškai).

Eismo Info creates sensors for the road weather stations (KOS) you choose: air and road surface
temperature, wind, precipitation, visibility, road condition, grip, and road warnings.

Requires **Home Assistant 2024.11 or newer**.

## Features

- No account or API key needed – the public eismoinfo.lt weather-conditions API is used.
- Add any number of stations; each one becomes its own device.
- When adding a station, the list is sorted **by distance from your Home Assistant home location**
  (if set), so the nearest stations come first (there are ~165 in total).
- Give each station your own name, and change the name or update interval any time in Options;
  switch to another station with **Reconfigure**.
- Sensors per station: air temperature, road surface temperature, dew point, wind speed
  (average/maximum) and direction, precipitation type and amount, visibility, road condition,
  grip coefficient, warnings, and last update time.
- **Road hazard** binary sensor – on whenever the station reports any warning other than
  "good"/"easy" conditions; handy for automations.
- Optional (disabled by default, most stations don't report them): freezing point and road
  construction temperatures at several depths.
- Measurements a station doesn't provide show as **Unavailable**, not an ambiguous "Unknown".
- If eismoinfo.lt is down or returns incomplete data, stations keep their last known values for
  up to **1 hour**. A station that disappears from the API is reported in **Repairs**.
- Diagnostics download is supported.

## Installation

### Home Assistant Marketplace / HACS

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=triumfas&repository=HAEismoInfo&category=integration)

1. Open the Marketplace (HACS), search for **Eismo Info** and install it.
   Until it is listed in the default catalog: **Add from link** (custom repository) →
   `triumfas/HAEismoInfo`, type **Integration**.
2. Restart Home Assistant.

### Manual

Copy `custom_components/eismoinfo` to your `config/custom_components/` folder and restart.

## Setup

1. **Settings → Devices & services → Add integration** → search for **Eismo Info**.
2. Pick a weather station from the list (nearest first).
3. Optionally enter your own name for the station.
4. Repeat for every station you want.

## Data source

Data comes from the public, unauthenticated eismoinfo.lt API (Lithuanian Road Administration).
The integration makes one shared request for all stations (every ~5 minutes by default),
no matter how many stations you add. This is an unofficial community integration and is not
affiliated with or endorsed by the Lithuanian Road Administration.

## License

[GPL-3.0](LICENSE)

---

# Lietuviškai

## Eismo Info Home Assistant integracija

[![Validate](https://github.com/triumfas/HAEismoInfo/actions/workflows/validate.yml/badge.svg)](https://github.com/triumfas/HAEismoInfo/actions/workflows/validate.yml)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant custom integracija, kuri naudoja viešą [eismoinfo.lt](https://eismoinfo.lt) API (Lietuvos automobilių kelių direkcijos kelių eismo informacija, **tik Lietuvos keliai**) ir
sukuria sensorius pasirinktoms kelių orų stotelėms (KOS).

Reikalinga **Home Assistant 2024.11 arba naujesnė** (dėl Reconfigure config flow API).

### Galimybės

- Prisijungiama prie viešo eismoinfo.lt „weather-conditions“ API (autentifikacijos nereikia).
- Galima pridėti bet kiek stotelių – kiekvienai sukuriamas atskiras įrenginys (device).
- Stotelių sąrašas pridedant rūšiuojamas **pagal atstumą nuo jūsų HA namų lokacijos** (jei ji
  nustatyta), kad artimiausios stotelės būtų sąrašo viršuje, o ne abėcėlės tvarka iš ~165.
- Kiekvienai stotelei galima nustatyti **savo pavadinimą**, nebūtinai tą, kurį grąžina API.
- Pavadinimą ir atnaujinimo intervalą bet kada galima pakeisti per integracijos nustatymus
  (Options); pačią stotelę galima pakeisti per **Reconfigure**.
- Kiekvienai stotelei sukuriami sensoriai: oro temperatūra, kelio dangos temperatūra, rasos
  taškas, vėjo greitis (vidutinis/maksimalus) ir kryptis, kritulių tipas ir kiekis, matomumas,
  kelio dangos būklė, sukibimo koeficientas, įspėjimai ir paskutinio atnaujinimo laikas.
  Kritulių tipo ir kelio dangos sensorių ikonos keičiasi pagal reikšmę (pvz. sninga/lyja/sausa).
- **„Kelio pavojus“ (binary_sensor)** – įjungtas, kai stotelė praneša bet kokį įspėjimą, kitokį
  nei „geros“/„nesudėtingos“ sąlygos – patogu automatizacijoms be teksto sensoriaus parsinimo.
- Papildomai (išjungti pagal nutylėjimą, nes daugumoje stotelių duomenų nėra): užšalimo taškas ir
  kelio konstrukcijos temperatūros keliuose gyliuose.
- Kai stotelė nustoja grąžinti duomenis, apie tai aiškiai pranešama **Repairs** skydelyje (ne
  vien tylus sensorių pilkėjimas).
- Palaikomas **diagnostikos eksportas** (Nustatymai → Įrenginiai → stotelė → „Atsisiųsti
  diagnostiką“) – naudinga pranešant apie klaidas.

### Diegimas

#### Per HACS (rekomenduojama)

[![Atidaryti HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=triumfas&repository=HAEismoInfo&category=integration)

1. HACS → Integrations → meniu (⋮) → **Custom repositories**.
2. Įveskite `https://github.com/triumfas/HAEismoInfo`, kategorija **Integration**.
3. Susiraskite „Eismo Info“ sąraše ir įdiekite.
4. Perkraukite Home Assistant.

#### Rankiniu būdu

1. Nukopijuokite `custom_components/eismoinfo` aplanką į savo HA `config/custom_components/`.
2. Perkraukite Home Assistant.

### Konfigūravimas

1. **Nustatymai → Įrenginiai ir paslaugos → Pridėti integraciją** → ieškokite „Eismo Info“.
2. Pasirinkite norimą stotelę iš sąrašo.
3. Nebūtina: įveskite savo pavadinimą stotelei (jei paliksite tuščią, bus naudojamas API
   pavadinimas).
4. Kartokite žingsnius kiekvienai norimai stotelei.

Norėdami pervadinti stotelę arba pakeisti atnaujinimo dažnį vėliau, eikite į integracijos kortelę
→ **Konfigūruoti** (Options). Norėdami pakeisti pačią stotelę (nekeičiant pavadinimo/istorijos),
naudokite **Reconfigure** (integracijos kortelės meniu ⋮).

> Reconfigure žingsniui reikia Home Assistant **2024.11+**.

### Sensoriai

| Sensorius | Vienetas | Pagal nutylėjimą |
|---|---|---|
| Oro temperatūra | °C | ✅ |
| Kelio dangos temperatūra | °C | ✅ |
| Rasos taškas | °C | ✅ |
| Vidutinis / maksimalus vėjo greitis | m/s | ✅ |
| Vėjo kryptis | – | ✅ |
| Kritulių tipas / kiekis | – / mm | ✅ |
| Matomumas | m | ✅ |
| Kelio danga | – | ✅ |
| Sukibimo koeficientas | – | ✅ |
| Įspėjimai | – | ✅ |
| Paskutinis atnaujinimas | – | ✅ |
| **Kelio pavojus** (binary_sensor) | on/off | ✅ |
| Užšalimo taškas | °C | ❌ |
| Konstrukcijos temperatūra (7–200 cm) | °C | ❌ |

> **„Unavailable“ vs „Unknown“:** jei konkreti stotelė tiesiog neturi tam tikro matavimo
> (pvz., dauguma stotelių neturi rasos taško ar konstrukcijos temperatūros jutiklių),
> atitinkamas sensorius bus rodomas kaip **„Unavailable“** (pilkas, aiškiai matoma priežastis),
> o ne dviprasmiškas „Unknown“. „Įspėjimų“ sensorius – išimtis: kai stotelė nepraneša jokių
> įspėjimų, tai yra teisėta, žinoma būsena, o ne trūkstami duomenys.

> **Eismoinfo.lt sutrikimai:** jei eismoinfo.lt nepasiekiamas, grąžina tuščią ar nepilną
> sąrašą, stotelė išlaiko paskutines žinomas reikšmes ir lieka prieinama iki **1 valandos**
> nuo paskutinio sėkmingo atnaujinimo. Tik po to jos sensoriai tampa **„Unavailable“**.

### Pavyzdinė Lovelace kortelė

```yaml
type: entities
title: Kelio stotelė
entities:
  - entity: sensor.mano_stotele_air_temperature
  - entity: sensor.mano_stotele_road_surface_temperature
  - entity: sensor.mano_stotele_road_condition
  - entity: binary_sensor.mano_stotele_road_hazard
  - entity: sensor.mano_stotele_last_update
```

(Pakeiskite `mano_stotele` į jūsų stotelės entity_id prefiksą.)

### Duomenų šaltinis

Duomenys imami iš viešo, neautorizuoto eismoinfo.lt API. Integracija naudoja vieną bendrą
užklausą visoms stotelėms (kas ~5 min pagal nutylėjimą), nepriklausomai nuo to, kiek stotelių
pridėta Home Assistant'e.

### Ikonėlė

`custom_components/eismoinfo/brand/icon.png` (256×256, permatomas fonas) – integracijos ikonėlė.

Nuo Home Assistant **2026.3** custom integracijos gali turėti savo `brand/`
katalogą tiesiai integracijos aplanke – HA/HACS tokius vietinius vaizdus
naudoja automatiškai, jokio atskiro PR ar konfigūracijos nereikia. Senesnėse
HA versijose ikonėlė bus rodoma bendrinė (placeholder), bet tai neturi
įtakos integracijos veikimui.

Galimi failai kataloge `brand/`: `icon.png`, `icon@2x.png`, `logo.png`,
`logo@2x.png`, bei tamsios temos variantai `dark_icon.png` / `dark_logo.png`
(nebūtina).

### Licencija

[GPL-3.0](LICENSE)
