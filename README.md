# 🌿 EcoCity HN
 
**Making Heilbronn liveable: a climate and cycling map built from real sensor data.**
 
EcoCity HN is a Streamlit web app made for the **Green City Heilbronn Hackathon 2026**. It shows where Heilbronn is hot, where the air is dusty, which bike streets are smooth and where the roads are bumpy. Everything on the map comes from real measurements: senseBox sensors on bikes (openSenseMap) and the OpenStreetMap road network. The whole website is available in **English and German** (switch in the top bar).
 
---
 
## Contents
 
- [Features](#features)
- [Quick start](#quick-start)
- [Project structure](#project-structure)
- [Data](#data)
- [How the analysis works](#how-the-analysis-works)
- [Updating the data](#updating-the-data)
- [Configuration](#configuration)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [Credits](#credits)
---
 
## Features
 
### 🏠 Home
What EcoCity HN is for, the key numbers of the data, the coolest, cleanest and most livable area, and how your input helps the city.
 
### 🗺️ City Map
| Layer | What it shows |
|---|---|
| **Measured Areas 📡** | 18 areas of Heilbronn as circles, colored by **livability score**, **temperature** or **fine dust (PM2.5)**. Click a name for all values. |
| **Bike Sensor Tracks** | Where the sensor bikes rode (heatmap). |
| **Bike Lane Streets 🚲** | The 9 streets with the most bike infrastructure, drawn in violet along their real course. Click one to see the **smoothest route to the next bike lane** (green). |
| **Accessible Routes ♿** | The parts of the bike streets that the sensor bikes rode often and that are not on a bumpy road (dark blue = own bike lane, light blue = shared with cars). |
| **Bumpy Roads 🛣️** | Streets with a rough surface, drawn in black. |
 
**Area popups** show the livability score and its parts, temperature (average and compared with the city at the same hour), air quality, the bike lanes and bumpy roads in the area, and, if the area has no bike lane, the nearest one reachable by a smooth route.
 
**Time period** (sidebar): all data, or one month (December 2025 to October 2026). Map, popups, ranks and scores show the chosen month. Areas without enough data that month are grey, and the app warns when fewer than 3 bikes rode.
 
### 👥 Community and ⭐ Rate & Report
Meetups, spot ratings, improvement suggestions and a Community Ideas Board, with example posts for the demo. The forms use the 18 real areas as locations.
 
### 📊 Dashboard
- **Overall result:** temperature and fine dust per area, the full area ranking with livability, and "Where Heilbronn needs help" (warmest areas, most fine dust, bumpiest roads).
- **Month by month:** city averages per month, a livability grid (area × month, same colors as the map), and a monthly view of one area.
- **Where the sensor bikes measured:** coverage map of all rides.
---
 
## Quick start
 
**Requirements:** Python 3.10+, `make`, and the `venv` module (on Ubuntu / WSL: `sudo apt install python3-venv`).
 
```bash
make run
```
 
This checks that all files are there, creates a virtual environment in `.venv`, installs the packages from `requirements.txt` and starts the app. Open the address it prints (usually http://localhost:8501). On WSL, open it in your Windows browser.
 
| Command | What it does |
|---|---|
| `make` / `make install` | Check that all files are there, create `.venv`, install the packages (only again when `requirements.txt` changes) |
| `make run` | Install if needed, then start the app |
| `make data` | Rebuild the area tables from the raw sensor data ([see below](#updating-the-data)) |
| `make check` | List missing project files |
| `make clean` | Remove caches |
| `make fclean` | Also remove `.venv` |
| `make re` | Rebuild from scratch |
 
> **"Missing in this folder: …"?** The files listed under [Project structure](#project-structure) must be in the same places, relative to the Makefile.
 
---
 
## Project structure
 
```
├── app.py                          The website frame: page setup, ENG / DE switch, sidebar, tabs
├── prepare_data.py                 Raw sensor data → area tables        (make data)
├── Makefile, requirements.txt, README.md
│
├── tabs/
│   ├── home_tab.py                 🏠 Home
│   ├── map_tab.py                  🗺️ City Map
│   ├── community_tab.py            👥 Community
│   ├── rate_report_tab.py          ⭐ Rate & Report and the Ideas Board
│   ├── dashboard_tab.py            📊 Dashboard
│   ├── real_data.py                Loads all data; street courses from the road network
│   ├── periods.py                  The chosen time period: areas, tracks and totals for it
│   ├── livability.py               Livability score and map colors
│   ├── routing.py                  Road graph and smooth routes between bike lanes
│   ├── translation.py              Every text in English and German
│   └── community_examples.py       Example meetups and ratings for the demo
│
├── csv/
│   ├── area_centers.csv            Fixed center of each of the 18 areas
│   ├── heilbronn_area_ranking.csv  Results per area, all dates          ┐
│   ├── area_months.csv             Results per area and month           │ made by
│   ├── tracks.csv                  Where the bikes rode, per month      │ make data
│   ├── data_info.json              Rules and totals                     ┘
│   └── bike_road_network_heilbronn.csv  OpenStreetMap road network
│
└── images/canopy-5.jpg             Photo for the Ideas Board (optional, a note is shown if missing)
```
 
Not in the repository because of its size (needed only for `make data`): `csv/osem_bike_data.csv` (105 MB).
 
---
 
## Data
 
| Data | Source | Content |
|---|---|---|
| Bike sensor readings | openSenseMap, senseBox:bike | 475,614 rows from 30 bikes, 14 Dec 2025 – 19 Oct 2026, one per second: GPS, temperature, humidity, PM1–PM10, overtaking distance, surface, speed |
| Road network | OpenStreetMap | 34,243 street pieces of Heilbronn with names, course and bike lane tags |
| Bike lane streets | Team list + road network | 9 streets; their lane type and number of segments are counted from the network's bike lane tags |
| Bumpy roads | Team list | 11 streets with average and peak roughness |
 
After cleaning, **201,156 readings** from 26 bikes are assigned to the 18 areas.
 
---
 
## How the analysis works
 
The full method, with all formulas and worked examples, is in **`EcoCity_HN_Method.pdf`**. In short:
 
### 1. Cleaning (`prepare_data.py`)
- Keep readings with temperature, PM2.5 and a position.
- Drop readings above **85 % humidity** (fine dust sensors read too high in humid air) and PM2.5 above **100 µg/m³** (sensor faults).
- Each reading belongs to the **nearest of the 18 area centers**, if it is within **2.5 km**.
- An area needs **300 readings on 3 days** overall, and **100 readings on 3 days** in a month. Otherwise it is shown grey for that month.
### 2. Comparing areas fairly: the same-hour method
The bikes ride at different times, so a plain average compares seasons and times of day instead of places. Every reading is therefore compared with **the median of all sensors in the same hour**:
 
```
difference = reading − median of all readings in that hour
```
 
`temp_anom` (°C) and `pm25_anom` (µg/m³) are the averages of these differences per area. A negative temperature difference means the area is cooler than the rest of the city at the same moment, which is less heat island.
 
### 3. Livability score (`tabs/livability.py`)
```
Livability = 40 % air + 40 % heat + 20 % bike        (each part 0–100)
```
| Part | 100 points | 0 points |
|---|---|---|
| **Air** | 0 µg/m³ average PM2.5 | 10 µg/m³ or more (2× the WHO yearly guideline) |
| **Heat** | 0.5 °C cooler than the city at the same hour | 0.5 °C warmer |
| **Bike** | bike lane street in the area | nearest bike lane 5 km or more away (smooth route); −20 if a bumpy road is in the area |
 
The same score is calculated for every month. The bike part is the same in every month.
 
**Map colors:** above 60 green (darker = better), 50–60 white, below 50 red (redder = worse).
 
### 4. Smooth routes (`tabs/routing.py`)
The road network becomes a graph of crossings and street pieces. Routes minimize the length, but **a meter of bumpy road counts like 10 meters**, so routes avoid bumpy roads whenever possible (Dijkstra's algorithm, `networkx`).
 
### 5. Accessible routes (`tabs/real_data.py`)
A piece of a bike street counts as accessible when at least half of it lies on ~55 m cells that the sensor bikes rode **20 times or more** (so it has a rideable surface), and it is not part of a bumpy road.
 
---
 
## Updating the data
 
When new sensor data arrives:
 
1. Download the openSenseMap export as `csv/osem_bike_data.csv` (same columns as before).
2. `make data` rebuilds the area results, monthly tables, tracks and `data_info.json` (a few seconds).
3. `make run`.
---
 
## Configuration
 
All rules are constants at the top of their file:
 
| File | Constant | Default | Meaning |
|---|---|---|---|
| `prepare_data.py` | `START_DATE` | `2025-12-01` | Use data from this date on (e.g. `2026-06-01` for summer only) |
| | `MAX_HUMIDITY`, `MAX_PM25`, `MAX_KM` | 85 %, 100 µg/m³, 2.5 km | Cleaning rules |
| | `MIN_READINGS`, `MIN_DAYS` | 300, 3 | Minimum data for an area overall |
| | `MIN_MONTH_READINGS`, `MIN_MONTH_DAYS` | 100, 3 | Minimum data for an area in one month |
| `tabs/livability.py` | `WEIGHTS` | air 0.4, heat 0.4, bike 0.2 | Share of each part in the score |
| | `PM25_WORST`, `HEAT_RANGE`, `BIKE_MAX_KM` | 10, 0.5, 5 | Limits of the part scores |
| `tabs/routing.py` | `BUMPY_PENALTY` | 10 | How much a bumpy meter counts in routing |
| `tabs/real_data.py` | `AREA_RADIUS_M` | 450 m | Area circle radius |
| | `MIN_RIDES` | 20 | Readings a cell needs to count as ridden (accessible routes) |
| `tabs/translation.py` | `T` | | Every text on the website (English, German) |
 
After changing a constant in `prepare_data.py`, run `make data`. If you change the track cell size (`CELL_LAT`, `CELL_LON`), change it in `tabs/real_data.py` too.
 
---
 
## Limitations
 
- **Sensor offsets:** sensors standing side by side differed by about 1.7 °C on average, which is larger than the differences between areas (tenths of a degree). Read area temperatures as tendencies.
- **Uneven coverage:** December to May have only 1 bike, so heat comparisons in those months are not meaningful (the app warns). Some areas have only 4–5 riding days (Nordheim, Weinsberg).
- **Season mix:** areas measured in winter (Innenstadt, Nordstadt, Bahnhofsvorstadt, Ost) include the January smog in their overall fine dust average. Use the time period filter for fair comparisons.
- **No amenities yet:** parks, fountains and shade are not part of the livability score; there is no real data for them.
- **The bikes are not all cyclists:** the data shows where 30 sensor bikes rode, not all bike traffic in Heilbronn.
- **Community content is demo data:** meetups, ratings and Ideas Board posts are examples and are not saved.
---
 
## Roadmap
 
### Map visualization
- [ ] Light base map (CartoDB Positron) so the data layers stand out
- [ ] Legend, layer switcher and fullscreen button on the map
- [ ] Hexagon grid (~150 m) instead of circles, for street-level detail
- [ ] Real area shapes instead of overlapping circles
- [ ] Bike paths colored by the temperature or fine dust measured along them
- [ ] 3D map (pydeck) and an animation of the city heating up over the day
- [ ] Side-by-side maps (e.g. July vs. January)
### Data and analysis
- [ ] Correct each sensor's temperature offset, using moments when two bikes were at the same place
- [ ] Add the September walks (`datasets.zip`, 61,546 readings) after offset correction
- [ ] Use the THW Heilbronn weather station as a fixed reference (needs the full export) and filter readings taken in rain
- [ ] Raise the minimum to 7 riding days per month for more reliable monthly scores
- [ ] Use the same-hour PM2.5 difference in the air score, so the season mix no longer matters
- [ ] Add amenities (parks, fountains, shade) to the livability score
### App
- [ ] Save community posts, ratings and ideas in a database
- [ ] Update the Ideas Board texts with the real measured values
---
 
## Documentation
 
| File | Content |
|---|---|
| `EcoCity_HN_Method.pdf` | All rules and formulas behind the analysis and the livability score |
| `EcoCity_HN_Changelog.pdf` | All changes since the first version |
 
---
 
## Credits
 
Built for the **Green City Heilbronn Hackathon 2026**.
 
- Sensor data: [openSenseMap](https://opensensemap.org) (senseBox:bike)
- Road network: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors
- Built with [Streamlit](https://streamlit.io), [folium](https://python-visualization.github.io/folium/), [Plotly](https://plotly.com/python/), [pandas](https://pandas.pydata.org), [NetworkX](https://networkx.org) and [NumPy](https://numpy.org)
 