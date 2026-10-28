import pandas as pd

# ─── Sensor locations with pre-set readings (no generation needed) ───
SENSORS = pd.DataFrame([
    {"id": "S01", "name": "Marktplatz", "lat": 49.1427, "lon": 9.2109, "type": "urban_center", "temperature": 35.2, "humidity": 42, "pm25": 18.3, "pm10": 27.5, "comfort": 28},
    {"id": "S02", "name": "Wertwiesenpark", "lat": 49.1520, "lon": 9.2250, "type": "park", "temperature": 28.5, "humidity": 55, "pm25": 8.2, "pm10": 12.3, "comfort": 82},
    {"id": "S03", "name": "Pfuehlpark", "lat": 49.1380, "lon": 9.2020, "type": "park", "temperature": 29.1, "humidity": 53, "pm25": 9.1, "pm10": 13.7, "comfort": 78},
    {"id": "S04", "name": "Hauptbahnhof", "lat": 49.1440, "lon": 9.2180, "type": "transit", "temperature": 34.0, "humidity": 40, "pm25": 22.5, "pm10": 33.8, "comfort": 32},
    {"id": "S05", "name": "Kaiserstrasse", "lat": 49.1410, "lon": 9.2200, "type": "shopping", "temperature": 33.8, "humidity": 41, "pm25": 16.8, "pm10": 25.2, "comfort": 38},
    {"id": "S06", "name": "Neckarufer Sued", "lat": 49.1390, "lon": 9.2100, "type": "waterfront", "temperature": 27.8, "humidity": 58, "pm25": 7.5, "pm10": 11.3, "comfort": 85},
    {"id": "S07", "name": "Neckargartach Industrie", "lat": 49.1600, "lon": 9.1950, "type": "industrial", "temperature": 36.5, "humidity": 38, "pm25": 28.4, "pm10": 42.6, "comfort": 15},
    {"id": "S08", "name": "Frankenstadion", "lat": 49.1530, "lon": 9.2050, "type": "sports", "temperature": 31.2, "humidity": 48, "pm25": 11.3, "pm10": 17.0, "comfort": 62},
    {"id": "S09", "name": "Kilianskirche", "lat": 49.1420, "lon": 9.2190, "type": "old_town", "temperature": 33.5, "humidity": 43, "pm25": 15.2, "pm10": 22.8, "comfort": 40},
    {"id": "S10", "name": "Waldgebiet Jaegerhaus", "lat": 49.1350, "lon": 9.1900, "type": "forest", "temperature": 26.2, "humidity": 62, "pm25": 5.1, "pm10": 7.7, "comfort": 92},
    {"id": "S11", "name": "Boeckingen", "lat": 49.1450, "lon": 9.1850, "type": "residential", "temperature": 31.8, "humidity": 47, "pm25": 12.5, "pm10": 18.8, "comfort": 55},
    {"id": "S12", "name": "Sontheim", "lat": 49.1300, "lon": 9.2300, "type": "residential", "temperature": 31.5, "humidity": 48, "pm25": 11.8, "pm10": 17.7, "comfort": 58},
    {"id": "S13", "name": "Bildungscampus", "lat": 49.1480, "lon": 9.2150, "type": "campus", "temperature": 32.0, "humidity": 45, "pm25": 13.2, "pm10": 19.8, "comfort": 50},
    {"id": "S14", "name": "Theresienwiese", "lat": 49.1460, "lon": 9.2080, "type": "open_field", "temperature": 30.5, "humidity": 50, "pm25": 10.5, "pm10": 15.8, "comfort": 65},
    {"id": "S15", "name": "Neckarufer Nord", "lat": 49.1500, "lon": 9.2100, "type": "waterfront", "temperature": 28.0, "humidity": 57, "pm25": 7.8, "pm10": 11.7, "comfort": 84},
])

DRINKING_WATER = [
    {"name": "Marktplatzbrunnen", "lat": 49.1427, "lon": 9.2109, "status": "working"},
    {"name": "Wertwiesenpark Brunnen", "lat": 49.1525, "lon": 9.2245, "status": "working"},
    {"name": "Bahnhof Wasserspender", "lat": 49.1442, "lon": 9.2175, "status": "working"},
    {"name": "Pfuehlpark Brunnen", "lat": 49.1385, "lon": 9.2015, "status": "broken"},
    {"name": "Campus Wasserspender", "lat": 49.1478, "lon": 9.2155, "status": "working"},
    {"name": "Kiliansplatz Brunnen", "lat": 49.1418, "lon": 9.2195, "status": "working"},
    {"name": "Stadion Trinkwasser", "lat": 49.1535, "lon": 9.2045, "status": "working"},
    {"name": "Sontheim Brunnen", "lat": 49.1305, "lon": 9.2295, "status": "dry"},
    {"name": "Boeckingen Brunnen", "lat": 49.1455, "lon": 9.1845, "status": "working"},
    {"name": "Neckarufer Brunnen", "lat": 49.1395, "lon": 9.2095, "status": "working"},
]

COOL_SPOTS = [
    {"name": "Wertwiesenpark Schattenplatz", "lat": 49.1522, "lon": 9.2240, "desc": "Shaded area with benches under old trees"},
    {"name": "Stadtbibliothek", "lat": 49.1430, "lon": 9.2115, "desc": "Air-conditioned public library, free entry"},
    {"name": "Neckarufer Promenade", "lat": 49.1392, "lon": 9.2105, "desc": "Breezy riverside walk, 2-3 degrees cooler"},
    {"name": "Waldgebiet Trails", "lat": 49.1348, "lon": 9.1905, "desc": "Forest trails, up to 5 degrees cooler"},
    {"name": "Pfuehlpark Schattenweg", "lat": 49.1378, "lon": 9.2025, "desc": "Tree-lined paths with good shade"},
    {"name": "Harmonie Center", "lat": 49.1415, "lon": 9.2175, "desc": "Air-conditioned shopping center"},
    {"name": "Experimenta Vorplatz", "lat": 49.1485, "lon": 9.2205, "desc": "Shaded area near science center"},
]

# Walking paths with natural tree shade: "points" is the route as [lat, lon] pairs
SHADE_PATHS = [
    {"name": "Neckar Riverside Walk", "shade": 80, "length_km": 1.4,
     "desc": "Tree-lined path along the river, cool breeze",
     "points": [[49.1390, 9.2100], [49.1420, 9.2095], [49.1450, 9.2092],
                [49.1475, 9.2095], [49.1500, 9.2100]]},
    {"name": "Pfuehlpark to Forest Trail", "shade": 90, "length_km": 1.3,
     "desc": "Old trees through the park, then into the forest",
     "points": [[49.1378, 9.2025], [49.1370, 9.1995], [49.1360, 9.1960],
                [49.1352, 9.1930], [49.1348, 9.1905]]},
    {"name": "Station to Wertwiesenpark", "shade": 55, "length_km": 1.2,
     "desc": "Partly shaded route past the Experimenta",
     "points": [[49.1440, 9.2180], [49.1460, 9.2195], [49.1485, 9.2205],
                [49.1505, 9.2225], [49.1522, 9.2240]]},
    {"name": "Marktplatz to the River", "shade": 60, "length_km": 0.5,
     "desc": "Quick escape from the hot square to the Neckar",
     "points": [[49.1427, 9.2109], [49.1430, 9.2115], [49.1412, 9.2108],
                [49.1392, 9.2105]]},
]

MEETUPS = [
    {"id": 1, "title": "Morning Jog along Neckar", "activity": "Jogging", "organizer": "Anna M.",
     "date": "2026-07-15", "time": "06:30", "point": "Neckarufer Sued", "joined": 8, "max": 15,
     "desc": "Early morning jog along the river before the heat. ~5km."},
    {"id": 2, "title": "Park Yoga", "activity": "Yoga", "organizer": "Lisa K.",
     "date": "2026-07-18", "time": "07:00", "point": "Wertwiesenpark", "joined": 12, "max": 20,
     "desc": "Outdoor yoga in the shade. Bring your own mat!"},
    {"id": 3, "title": "Cool Spots Walking Tour", "activity": "Walking", "organizer": "Thomas R.",
     "date": "2026-07-20", "time": "18:00", "point": "Marktplatz", "joined": 5, "max": 25,
     "desc": "Guided walk through Heilbronn's coolest spots."},
    {"id": 4, "title": "Forest Cycling", "activity": "Cycling", "organizer": "Max B.",
     "date": "2026-07-22", "time": "17:30", "point": "Waldgebiet Jaegerhaus", "joined": 6, "max": 12,
     "desc": "Shaded forest route. ~10km, moderate."},
]

RATINGS = [
    {"spot": "Waldgebiet Jaegerhaus", "rating": 4.8, "reviews": 15, "comment": "Coolest spot in the city"},
    {"spot": "Wertwiesenpark", "rating": 4.5, "reviews": 23, "comment": "Great shade, always breezy"},
    {"spot": "Neckarufer Sued", "rating": 4.2, "reviews": 18, "comment": "Nice river breeze"},
    {"spot": "Pfuehlpark", "rating": 3.9, "reviews": 12, "comment": "Good but fountain broken"},
    {"spot": "Bildungscampus", "rating": 3.5, "reviews": 8, "comment": "Some shade, mostly concrete"},
    {"spot": "Hauptbahnhof", "rating": 2.5, "reviews": 14, "comment": "Concrete heat trap"},
    {"spot": "Marktplatz", "rating": 2.1, "reviews": 31, "comment": "Too hot, avoid afternoons"},
]

# Simple hourly data for charts (pre-computed, not generated)
HOURLY_TEMPS = pd.DataFrame({
    "hour": list(range(24)) * 3,
    "type": ["Park"]*24 + ["Urban Center"]*24 + ["Waterfront"]*24,
    "temperature": [
        # Park
        18,17,16,16,16,17,19,21,23,25,26,27,28,28,28,27,26,25,23,22,21,20,19,18,
        # Urban Center
        22,21,20,20,20,21,23,26,29,31,33,34,35,35,35,34,33,31,29,27,26,25,24,23,
        # Waterfront
        19,18,17,17,17,18,20,22,24,25,27,27,28,28,27,27,26,25,23,22,21,20,19,19,
    ]
})

HOURLY_PM = pd.DataFrame({
    "hour": list(range(24)) * 3,
    "type": ["Park"]*24 + ["Urban Center"]*24 + ["Industrial"]*24,
    "pm25": [
        # Park
        5,4,4,3,3,4,6,7,8,7,6,6,6,6,6,6,7,8,7,6,5,5,5,5,
        # Urban Center
        10,8,7,6,6,8,14,18,20,16,14,13,13,12,12,13,15,20,18,14,12,11,10,10,
        # Industrial
        15,12,10,9,9,12,20,25,28,22,18,16,15,15,16,17,20,28,25,20,18,16,15,15,
    ]
})