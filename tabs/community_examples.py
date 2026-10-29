# ─── Example community content (made up, shown as demo posts) ───
# Meetups listed in the Community tab, spot ratings and Ideas Board places in the Rate & Report tab
 
# Where each idea on the Ideas Board would be built: street names from the road network,
# drawn on the City Map by its "Show on Map" button ([] = city-wide, shows the whole map)
IDEA_PLACES = {
    1: ["Marktplatz", "Kaiserstraße", "Hauptbahnhof"],  # Cooling water walls
    2: [],                                               # Lamp post sensors, city-wide
    3: ["Wertwiesen", "Am Neckaruferpark"],              # Pet-friendly water stations
    4: ["Kaiserstraße", "Dammstraße"],                   # Sapling Squad
    5: ["Marktplatz", "Kaiserstraße"],                   # Crochet shade canopy
}
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
# rating = average stars (1-5), reviews = how many people rated the spot
RATINGS = [
    {"spot": "Waldgebiet Jaegerhaus", "rating": 4.8, "reviews": 15, "comment": "Coolest spot in the city"},
    {"spot": "Wertwiesenpark", "rating": 4.5, "reviews": 23, "comment": "Great shade, always breezy"},
    {"spot": "Neckarufer Sued", "rating": 4.2, "reviews": 18, "comment": "Nice river breeze"},
    {"spot": "Pfuehlpark", "rating": 3.9, "reviews": 12, "comment": "Good but fountain broken"},
    {"spot": "Bildungscampus", "rating": 3.5, "reviews": 8, "comment": "Some shade, mostly concrete"},
    {"spot": "Hauptbahnhof", "rating": 2.5, "reviews": 14, "comment": "Concrete heat trap"},
    {"spot": "Marktplatz", "rating": 2.1, "reviews": 31, "comment": "Too hot, avoid afternoons"},
]
