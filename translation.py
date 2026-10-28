import streamlit as st

# ─── UI texts: key -> (English, German) ───
T = {
    # Sidebar
    "tagline": ("Making Heilbronn liveable", "Heilbronn lebenswert machen"),
    "map_layers": ("Map Layers", "Kartenebenen"),
    "layer_real": ("Measured Areas 📡", "Gemessene Gebiete 📡"),
    "color_by": ("Color areas by", "Gebiete einfärben nach"),
    "color_livability": ("Livability score", "Lebensqualität"),
    "color_temperature": ("Temperature", "Temperatur"),
    "color_pm25": ("Fine dust (PM2.5)", "Feinstaub (PM2.5)"),
    "livability_legend": ("🟢 above 60 (darker = better) · ⚪ 50–60 · 🔴 below 50 (redder = worse)",
                          "🟢 über 60 (dunkler = besser) · ⚪ 50–60 · 🔴 unter 50 (röter = schlechter)"),
    "layer_tracks": ("Bike Sensor Tracks", "Fahrten der Sensor-Räder"),
    "layer_bike_streets": ("Bike Lane Streets 🚲", "Straßen mit Radweg 🚲"),
    "layer_bumpy": ("Bumpy Roads 🛣️", "Holprige Straßen 🛣️"),
    "layer_access": ("Accessible Routes ♿", "Barrierearme Wege ♿"),
    "bumpy_missing": ("{missing} of {total} bumpy roads were not found in the road network",
                      "{missing} von {total} holprigen Straßen wurden im Straßennetz nicht gefunden"),

    # Tabs
    "tab_map": ("🗺️ City Map", "🗺️ Stadtkarte"),
    "tab_community": ("👥 Community", "👥 Community"),
    "tab_rate": ("⭐ Rate & Report", "⭐ Bewerten & Melden"),
    "tab_dashboard": ("📊 Dashboard", "📊 Dashboard"),

    # Map tab
    "map_header": ("☀️ Heilbronn Climate Map", "☀️ Klimakarte Heilbronn"),
    "measured_by": ("Measured by {sensors} openSenseMap sensor bikes, {first} to {last}",
                    "Gemessen von {sensors} openSenseMap-Sensor-Rädern, {first} bis {last}"),
    "avg_temp": ("Avg Temp", "Ø Temperatur"),
    "avg_pm25": ("Avg PM2.5", "Ø PM2.5"),
    "sensor_bikes": ("Sensor Bikes", "Sensor-Räder"),
    "readings": ("Readings", "Messwerte"),
    "warmest_areas": ("🔥 Warmest Areas", "🔥 Wärmste Gebiete"),
    "vs_city_now": ("Compared with the whole city at the same hour",
                    "Im Vergleich zur ganzen Stadt zur selben Uhrzeit"),
    "coolest_areas": ("❄️ Coolest Areas", "❄️ Kühlste Gebiete"),
    "reset_view": ("🔄 Reset View", "🔄 Ansicht zurücksetzen"),
    "selected": ("📍 Selected: {name}", "📍 Ausgewählt: {name}"),
    "area_info": ("📍 **{area}** — rank {rank} of {total} | {temp:.1f}°C ({anom:+.2f}°C vs. city) | "
                  "PM2.5: {pm25:.1f} µg/m³ | PM10: {pm10:.1f} µg/m³",
                  "📍 **{area}** — Rang {rank} von {total} | {temp:.1f} °C ({anom:+.2f} °C ggü. Stadt) | "
                  "PM2.5: {pm25:.1f} µg/m³ | PM10: {pm10:.1f} µg/m³"),

    # Area popup
    "air_cleaner": ("🟢 Cleaner than average", "🟢 Sauberer als der Durchschnitt"),
    "air_slightly_worse": ("🟠 Slightly worse", "🟠 Etwas schlechter"),
    "air_more_dust": ("🔴 More fine dust", "🔴 Mehr Feinstaub"),
    "rank_of": ("Rank {rank} of {total}", "Rang {rank} von {total}"),
    "livability": ("Livability", "Lebensqualität"),
    "livability_parts": ("air {air:.0f} · heat {heat:.0f} · bike {bike:.0f}",
                         "Luft {air:.0f} · Hitze {heat:.0f} · Rad {bike:.0f}"),
    "temperature": ("Temperature", "Temperatur"),
    "vs_city_same_hour": ("{anom:+.2f}°C vs. city at the same hour", "{anom:+.2f} °C ggü. der Stadt zur selben Uhrzeit"),
    "air_quality": ("Air quality", "Luftqualität"),
    "vs_city": ("vs. city", "ggü. Stadt"),
    "bike_lanes": ("Bike lanes", "Radwege"),
    "bumpy_roads": ("Bumpy roads", "Holprige Straßen"),
    "own_lane": ("own bike lane", "eigener Radweg"),
    "shared_lane": ("shared with cars", "mit Autos geteilt"),
    "bike_in_area": ("{name}: {kind}, {n} segments", "{name}: {kind}, {n} Abschnitte"),
    "no_bike_street": ("No listed bike street in this area", "Keine gelistete Radstraße in diesem Gebiet"),
    "nearest_link": ("♿ Nearest: <b>{target}</b>, {km:.1f} km smooth route{via}{warn}",
                     "♿ Nächste: <b>{target}</b>, {km:.1f} km glatter Weg{via}{warn}"),
    "via": (" via {streets}", " über {streets}"),
    "crosses_bumpy": (" ⚠️ crosses a bumpy road", " ⚠️ führt über eine holprige Straße"),
    "bumpy_in_area": ("{name}: roughness {avg:.0f} (peak {peak:.0f})", "{name}: Rauheit {avg:.0f} (Spitze {peak:.0f})"),
    "no_bumpy": ("No listed bumpy road in this area", "Keine gelistete holprige Straße in diesem Gebiet"),
    "area_footer": ("{readings} readings · {days} days · {riders} bikes",
                    "{readings} Messwerte · {days} Tage · {riders} Räder"),
    "area_tooltip": ("📡 {area} — click for values", "📡 {area} — klicken für Werte"),

    # Bike streets and bumpy roads on the map
    "own_lane_full": ("🚲 Own bike lane", "🚲 Eigener Radweg"),
    "shared_lane_full": ("🚗🚲 Shared lane (bikes and cars)", "🚗🚲 Geteilte Spur (Räder und Autos)"),
    "street_segments": ("{n} street segments", "{n} Straßenabschnitte"),
    "bike_tooltip": ("🚲 {name} — {n} segments", "🚲 {name} — {n} Abschnitte"),
    "avg_roughness": ("Average roughness: {v:.1f}", "Durchschnittliche Rauheit: {v:.1f}"),
    "peak_roughness": ("Peak roughness: {v:.0f}", "Höchste Rauheit: {v:.0f}"),
    "segments_with_data": ("{n} segments with data", "{n} Abschnitte mit Daten"),
    "bumpy_tooltip": ("🛣️ {name} — roughness {v:.0f}", "🛣️ {name} — Rauheit {v:.0f}"),

    # Smooth route between bike streets
    "route_tooltip": ("♿ Smooth route to {target} — {km:.1f} km", "♿ Glatter Weg nach {target} — {km:.1f} km"),
    "route_direct": ("♿🚲 **{start}** connects directly with **{target}**.",
                     "♿🚲 **{start}** ist direkt mit **{target}** verbunden."),
    "route_found": ("♿🚲 **Smooth route** (green) from **{start}** to the nearest bike lane street, "
                    "**{target}**: {km:.1f} km via {via}. {note}",
                    "♿🚲 **Glatter Weg** (grün) von **{start}** zur nächsten Straße mit Radweg, "
                    "**{target}**: {km:.1f} km über {via}. {note}"),
    "small_paths": ("small connecting paths", "kleine Verbindungswege"),
    "route_bumpy_note": ("⚠️ There is no way around a bumpy road on this route.",
                         "⚠️ Auf diesem Weg lässt sich eine holprige Straße nicht umgehen."),
    "route_smooth_note": ("No bumpy roads on the way.", "Keine holprigen Straßen auf dem Weg."),
    "clear_route": ("✖ Clear route", "✖ Weg ausblenden"),
    "click_hint": ("💡 Click a violet bike street to see the smoothest route to the next bike lane.",
                   "💡 Klicke auf eine violette Radstraße, um den glattesten Weg zum nächsten Radweg zu sehen."),

    # Accessible routes
    "access_header": ("♿ Accessible Routes", "♿ Barrierearme Wege"),
    "access_caption": ("Parts of the bike streets that the sensor bikes rode at least {n} times "
                       "and that are not on a bumpy road",
                       "Abschnitte der Radstraßen, die die Sensor-Räder mindestens {n}-mal befahren haben "
                       "und die nicht auf einer holprigen Straße liegen"),
    "access_checked": ("{km:.1f} of {total:.1f} km checked", "{km:.1f} von {total:.1f} km geprüft"),
    "access_no_data": ("⚠️ No sensor data on this street", "⚠️ Keine Sensordaten auf dieser Straße"),
    "access_tooltip": ("♿ {name} — {kind}, {km:.1f} km checked", "♿ {name} — {kind}, {km:.1f} km geprüft"),
    "access_popup": ("<b>♿ {name}</b><br>{area}<br><br>{kind}<br>{km:.1f} of {total:.1f} km checked with the sensor bikes",
                     "<b>♿ {name}</b><br>{area}<br><br>{kind}<br>{km:.1f} von {total:.1f} km mit den Sensor-Rädern geprüft"),

    # Community tab
    "community_header": ("👥 Community Hub", "👥 Community-Treffpunkt"),
    "create_meetup": ("Create a Meetup", "Treffen erstellen"),
    "title": ("Title", "Titel"),
    "title_placeholder": ("Morning Jog along Neckar", "Morgenlauf am Neckar"),
    "activity": ("Activity", "Aktivität"),
    "date": ("Date", "Datum"),
    "time": ("Time", "Uhrzeit"),
    "meeting_point": ("Meeting Point", "Treffpunkt"),
    "max_participants": ("Max Participants", "Max. Teilnehmende"),
    "description": ("Description", "Beschreibung"),
    "create_meetup_btn": ("Create Meetup", "Treffen erstellen"),
    "title_missing": ("Please enter a title.", "Bitte gib einen Titel ein."),
    "meetup_created": ("✅ '{title}' created!", "✅ „{title}“ erstellt!"),
    "upcoming_meetups": ("Upcoming Meetups", "Kommende Treffen"),
    "date_at_time": ("{date} at {time}", "{date} um {time}"),
    "joined_count": ("joined ({n} spots left)", "dabei ({n} Plätze frei)"),
    "organized_by": ("Organized by {name}", "Organisiert von {name}"),
    "joined": ("✅ Joined", "✅ Dabei"),
    "join_event": ("Join this event", "Mitmachen"),

    # Rate & Report tab
    "rate_header": ("⭐ Rate, Report & Ideas", "⭐ Bewerten, Melden & Ideen"),
    "subtab_rate": ("📝 Rate & Report", "📝 Bewerten & Melden"),
    "subtab_ideas": ("💡 Community Ideas Board", "💡 Ideenbörse der Community"),
    "rate_spot": ("Rate a Spot", "Ort bewerten"),
    "select_spot": ("Select spot", "Ort auswählen"),
    "rating": ("Rating", "Bewertung"),
    "your_experience": ("Your experience", "Deine Erfahrung"),
    "report_issue": ("Report an issue", "Problem melden"),
    "issue": ("Issue", "Problem"),
    "submit": ("Submit", "Absenden"),
    "thanks_demo": ("✅ Thanks! (Demo)", "✅ Danke! (Demo)"),
    "suggest_improvement": ("Suggest Improvement", "Verbesserung vorschlagen"),
    "whats_needed": ("What's needed?", "Was wird gebraucht?"),
    "where": ("Where?", "Wo?"),
    "urgency": ("Urgency", "Dringlichkeit"),
    "submit_suggestion": ("Submit Suggestion", "Vorschlag absenden"),
    "recorded_demo": ("✅ Recorded! (Demo)", "✅ Gespeichert! (Demo)"),
    "community_ratings": ("Community Ratings", "Bewertungen der Community"),
    "reviews": ("reviews", "Bewertungen"),
    "label_great": ("🟢 Great", "🟢 Super"),
    "label_ok": ("🟡 OK", "🟡 OK"),
    "label_avoid": ("🔴 Avoid", "🔴 Meiden"),
    "most_requested": ("Most Requested", "Am häufigsten gewünscht"),
    "need": ("Need", "Bedarf"),
    "votes": ("Votes", "Stimmen"),

    # Community Ideas Board
    "ideas_intro": ("Citizens share ideas to make Heilbronn more liveable. Vote on ideas you support!",
                    "Bürgerinnen und Bürger teilen Ideen, um Heilbronn lebenswerter zu machen. Stimme für die Ideen, die du unterstützt!"),
    "post_idea": ("📮 Post Your Idea", "📮 Eigene Idee posten"),
    "idea_title": ("Idea Title", "Titel der Idee"),
    "idea_title_placeholder": ("e.g. Install mist cooling walls at Marktplatz",
                               "z. B. Sprühnebel-Kühlwände am Marktplatz aufstellen"),
    "category": ("Category", "Kategorie"),
    "suggested_location": ("Suggested Location", "Vorgeschlagener Ort"),
    "describe_idea": ("Describe your idea", "Beschreibe deine Idee"),
    "describe_idea_placeholder": ("Explain what you'd like to see and why it would help...",
                                  "Erkläre, was du dir wünschst und warum es helfen würde ..."),
    "upload_photo": ("Upload a photo or sketch (optional)", "Foto oder Skizze hochladen (optional)"),
    "post_idea_btn": ("Post Idea", "Idee posten"),
    "idea_posted": ("✅ Idea posted! (Demo)", "✅ Idee gepostet! (Demo)"),
    "n_votes": ("👍 {n} Votes", "👍 {n} Stimmen"),
    "n_comments": ("💬 {n} Comments", "💬 {n} Kommentare"),
    "show_on_map": ("📍 Show on Map", "📍 Auf Karte zeigen"),
    "image_missing": ("📷 Image: {file} not found — place it in the ecocity-hn folder",
                      "📷 Bild: {file} nicht gefunden — lege es in den Ordner ecocity-hn"),

    # Idea 1: Cooling Wall
    "idea1_title": ("Cooling Water Walls at Hot Spots", "Kühlende Wasserwände an Hitze-Hotspots"),
    "idea1_meta": ("Posted by <b>Maria S.</b> · 📍 Marktplatz · 3 days ago",
                   "Gepostet von <b>Maria S.</b> · 📍 Marktplatz · vor 3 Tagen"),
    "idea1_card_title": ("Cooling Water Wall", "Wasser-Kühlwand"),
    "idea1_card_desc": ("Vertical water features with<br>wooden frame & green facade",
                        "Vertikale Wasserelemente mit<br>Holzrahmen & begrünter Fassade"),
    "idea1_card_effect": ("Cools surrounding area by 3-5°C", "Kühlt die Umgebung um 3–5 °C"),
    "idea1_body": ("""
**Install water cooling walls** at Heilbronn's hottest spots like Marktplatz and Kaiserstrasse.
These vertical water features with wooden frames and green facades can cool the surrounding
area by 3-5°C through evaporative cooling. They also add greenery and improve air quality.

**Why it works:** Water evaporation absorbs heat from the air. Combined with plants on the
facade, it creates a natural micro-climate cooling effect. Benches nearby let people sit
and enjoy the cooler zone.

**Suggested locations:** Marktplatz (35.2°C avg), Hauptbahnhof (34.0°C avg)
""", """
**Wasser-Kühlwände installieren** an Heilbronns heißesten Orten wie Marktplatz und Kaiserstraße.
Diese vertikalen Wasserelemente mit Holzrahmen und begrünter Fassade können die Umgebung
durch Verdunstungskühlung um 3–5 °C abkühlen. Außerdem bringen sie mehr Grün und verbessern die Luftqualität.

**Warum es funktioniert:** Verdunstendes Wasser entzieht der Luft Wärme. Zusammen mit den Pflanzen
an der Fassade entsteht ein natürliches, kühlendes Mikroklima. Bänke in der Nähe laden zum Verweilen
in der kühleren Zone ein.

**Vorgeschlagene Orte:** Marktplatz (Ø 35,2 °C), Hauptbahnhof (Ø 34,0 °C)
"""),

    # Idea 2: Lamp Post Sensors
    "idea2_title": ("Smart Lamp Post Sensor Network", "Sensornetz an smarten Straßenlaternen"),
    "idea2_meta": ("Posted by <b>Jonas K.</b> · 📍 City-wide · 5 days ago",
                   "Gepostet von <b>Jonas K.</b> · 📍 Stadtweit · vor 5 Tagen"),
    "idea2_card_title": ("Smart Lamp Post", "Smarte Straßenlaterne"),
    "idea2_card_list": ("""📡 senseBox mounted at top<br>
                    🌡️ Temperature + Humidity<br>
                    🌬️ PM1, PM2.5, PM4, PM10<br>
                    ⚗️ <b>NO₂ + O₃ gas sensors</b><br>
                    📍 GPS location built-in""",
                        """📡 senseBox oben montiert<br>
                    🌡️ Temperatur + Luftfeuchtigkeit<br>
                    🌬️ PM1, PM2.5, PM4, PM10<br>
                    ⚗️ <b>NO₂- + O₃-Gassensoren</b><br>
                    📍 Integriertes GPS"""),
    "idea2_card_power": ("Powered by lamp post electricity", "Strom direkt aus der Straßenlaterne"),
    "idea2_card_birdbox": ("Bird box housing option<br>blends with environment",
                           "Optionales Vogelhaus-Gehäuse<br>fügt sich ins Stadtbild ein"),
    "idea2_body": ("""
**Mount sensor boxes on existing lamp posts** across Heilbronn to dramatically expand our
environmental monitoring coverage — no new infrastructure needed!

**The setup:**
- senseBox sensor unit attached to the lamp post, powered by the existing electricity
- Measures temperature, humidity, PM1/PM2.5/PM4/PM10 particulate matter
- **NEW: NO₂ and O₃ gas sensors** to track traffic pollution and summer ozone
- Bird box-style housing that blends naturally into the streetscape

**Why NO₂ and O₃ matter:** NO₂ comes directly from vehicle exhaust. Ground-level ozone (O₃)
forms when sunlight cooks traffic fumes — it gets **worst on the hottest days**, exactly when
EcoCity users need the cleanest routes.

**Coverage goal:** Every 200m along main roads = complete city monitoring
""", """
**Sensorboxen an bestehenden Straßenlaternen montieren** – so erweitern wir die Umweltmessung
in ganz Heilbronn enorm, ganz ohne neue Infrastruktur!

**Der Aufbau:**
- senseBox-Sensoreinheit am Laternenmast, versorgt über den vorhandenen Stromanschluss
- Misst Temperatur, Luftfeuchtigkeit und Feinstaub (PM1/PM2.5/PM4/PM10)
- **NEU: NO₂- und O₃-Gassensoren**, um Verkehrsabgase und Sommerozon zu erfassen
- Gehäuse im Vogelhaus-Stil, das sich natürlich ins Stadtbild einfügt

**Warum NO₂ und O₃ wichtig sind:** NO₂ stammt direkt aus Autoabgasen. Bodennahes Ozon (O₃)
entsteht, wenn Sonnenlicht auf Verkehrsabgase trifft – es ist **an den heißesten Tagen am
schlimmsten**, genau dann, wenn EcoCity-Nutzer die saubersten Routen brauchen.

**Ziel der Abdeckung:** Alle 200 m entlang der Hauptstraßen = flächendeckende Messung in der ganzen Stadt
"""),

    # Idea 3: Pet-Friendly Water Stations
    "idea3_title": ("Pet-Friendly Drinking Water Stations", "Haustierfreundliche Trinkwasserstationen"),
    "idea3_meta": ("Posted by <b>Sophie L.</b> · 📍 Wertwiesenpark, Neckarufer · 1 week ago",
                   "Gepostet von <b>Sophie L.</b> · 📍 Wertwiesenpark, Neckarufer · vor 1 Woche"),
    "idea3_card_title": ("Pet-Friendly Fountain", "Haustierfreundlicher Brunnen"),
    "idea3_card_human": ("""<b>Human level:</b><br>
                    Standard drinking fountain<br>
                    with bottle refill tap""",
                         """<b>Obere Ebene:</b><br>
                    Normaler Trinkbrunnen<br>
                    mit Flaschen-Nachfüllhahn"""),
    "idea3_card_pet": ("""<b>Ground level:</b><br>
                    Sliding panel opens to<br>
                    reveal water bowl for pets<br>
                    Auto-drain & self-cleaning""",
                       """<b>Bodenebene:</b><br>
                    Schiebeklappe gibt einen<br>
                    Wassernapf für Tiere frei<br>
                    Automatischer Ablauf & Selbstreinigung"""),
    "idea3_card_rain": ("♻️ Rainwater collection option", "♻️ Optional mit Regenwassernutzung"),
    "idea3_body": ("""
**Dual-level drinking fountains** that serve both people and their pets! Perfect for
Heilbronn's parks and walking paths along the Neckar.

**Design features:**
- **Upper level:** Standard drinking fountain + bottle refill spout for humans
- **Lower level:** Sliding panel at the base that opens to reveal a stainless steel water bowl for dogs and cats
- **Hygienic:** Auto-drain after each use, self-cleaning cycle, fresh water each time
- **Sustainable:** Optional rainwater collection system for the pet bowl

**Why this matters:** On hot summer days, dogs suffer from heat too. Dog owners currently
carry extra water or look for puddles. These stations make walks safer for pets and encourage
people to walk longer cool routes instead of cutting through hot zones.

**Suggested locations:** Wertwiesenpark (popular dog walking), Neckarufer paths, Pfuehlpark
""", """
**Trinkbrunnen auf zwei Ebenen**, die Menschen und ihren Haustieren dienen! Perfekt für
Heilbronns Parks und Spazierwege entlang des Neckars.

**Design-Merkmale:**
- **Obere Ebene:** Normaler Trinkbrunnen + Nachfüllhahn für Flaschen
- **Untere Ebene:** Eine Schiebeklappe am Sockel gibt einen Edelstahl-Wassernapf für Hunde und Katzen frei
- **Hygienisch:** Automatischer Ablauf nach jeder Nutzung, Selbstreinigung, jedes Mal frisches Wasser
- **Nachhaltig:** Optionale Regenwassernutzung für den Tiernapf

**Warum das wichtig ist:** An heißen Sommertagen leiden auch Hunde unter der Hitze. Hundehalter
tragen heute extra Wasser mit oder suchen nach Pfützen. Diese Stationen machen Spaziergänge für
Tiere sicherer und motivieren dazu, längere kühle Routen zu gehen, statt durch heiße Zonen abzukürzen.

**Vorgeschlagene Orte:** Wertwiesenpark (beliebt bei Hundehaltern), Wege am Neckarufer, Pfühlpark
"""),

    # Idea 4: Kids Tree Planting Initiative
    "idea4_title": ("Cool Our School Road! — Sapling Squad 🌳", "Kühle Schulstraße! — Die Setzling-Truppe 🌳"),
    "idea4_meta": ("Posted by <b>Class 4a, Grundschule Dammstrasse</b> 👧👦 · Ages 9-10 · 📍 Kaiserstrasse & Dammstrasse · 5 days ago",
                   "Gepostet von <b>Klasse 4a, Grundschule Dammstraße</b> 👧👦 · 9–10 Jahre · 📍 Kaiserstraße & Dammstraße · vor 5 Tagen"),
    "idea4_card_title": ("🌱 The Sapling Squad Plan 🌱", "🌱 Der Plan der Setzling-Truppe 🌱"),
    "idea4_card_hot": ("☀️ HOT ROAD (34°C) ☀️", "☀️ HEISSE STRASSE (34 °C) ☀️"),
    "idea4_card_where": ("Kaiserstrasse near school", "Kaiserstraße bei der Schule"),
    "idea4_card_plant": ("⬇️ We plant! ⬇️", "⬇️ Wir pflanzen! ⬇️"),
    "idea4_card_water": ("⬇️ We water daily! ⬇️", "⬇️ Wir gießen jeden Tag! ⬇️"),
    "idea4_card_cool": ("🌡️ COOL ROAD! 🌡️", "🌡️ KÜHLE STRASSE! 🌡️"),
    "idea4_card_rota": ("""📅 Mon: Team A 💧 Tue: Team B 💧<br>
                    📅 Wed: Team C 💧 Thu: Team D 💧<br>
                    📅 Fri: Team E 💧<br>
                    📅 Sat: Neighborhood kids 🏡💧<br>
                    📅 Sun: Neighborhood kids 🏡💧<br>
                    ✅ Every day covered!""",
                        """📅 Mo: Team A 💧 Di: Team B 💧<br>
                    📅 Mi: Team C 💧 Do: Team D 💧<br>
                    📅 Fr: Team E 💧<br>
                    📅 Sa: Nachbarskinder 🏡💧<br>
                    📅 So: Nachbarskinder 🏡💧<br>
                    ✅ Jeder Tag ist abgedeckt!"""),
    "idea4_body": ("""
*"Hello! We are Class 4a and on Environment Day our teacher showed us the EcoCity app.
We checked — the road from our school to the bus stop is 34°C in summer! There are
NO trees at all. So we have a plan!"* 🌱

**Our "Sapling Squad" Plan:**
- **Plant tree saplings** along Kaiserstrasse and Dammstrasse near our school
- **We take care of them!** Every class gets a watering schedule — Team A on Monday,
  Team B on Tuesday, Team C on Wednesday... every day is covered
- Each student "adopts" a sapling and gives it a name
- We measure the temperature next to our trees every week using a thermometer
  and track it on the EcoCity app
- **Next year's Class 4 takes over** — so the trees always have caretakers!

**What we need from the city:**
- Saplings (we researched: linden trees and maples grow well in Heilbronn!)
- Permission to plant along the school road
- A few watering cans for the school

*"Our teacher Herr Weber says if each class plants 10 trees, in 5 years the
whole road will be shaded. We did the math — that's 50 trees from just our
school! And if other schools join..."* 🌳🌳🌳

**Herr Weber's note:** *"This project teaches the children responsibility, teamwork,
and climate science. They've already used EcoCity data to identify the hottest
streets near school. The daily watering rota is their own idea — I'm very proud."*
""", """
*„Hallo! Wir sind die Klasse 4a, und am Umwelttag hat uns unser Lehrer die EcoCity-App gezeigt.
Wir haben nachgeschaut – der Weg von unserer Schule zur Bushaltestelle hat im Sommer 34 °C!
Dort gibt es KEINEN einzigen Baum. Also haben wir einen Plan!“* 🌱

**Unser „Setzling-Truppe“-Plan:**
- **Baumsetzlinge pflanzen** entlang der Kaiserstraße und Dammstraße bei unserer Schule
- **Wir kümmern uns um sie!** Jede Klasse bekommt einen Gießplan – Team A am Montag,
  Team B am Dienstag, Team C am Mittwoch … jeder Tag ist abgedeckt
- Jedes Kind „adoptiert“ einen Setzling und gibt ihm einen Namen
- Wir messen jede Woche mit einem Thermometer die Temperatur neben unseren Bäumen
  und tragen sie in die EcoCity-App ein
- **Die nächste 4. Klasse übernimmt** – so haben die Bäume immer jemanden, der sich kümmert!

**Was wir von der Stadt brauchen:**
- Setzlinge (wir haben recherchiert: Linden und Ahorn wachsen gut in Heilbronn!)
- Die Erlaubnis, entlang des Schulwegs zu pflanzen
- Ein paar Gießkannen für die Schule

*„Unser Lehrer Herr Weber sagt, wenn jede Klasse 10 Bäume pflanzt, ist in 5 Jahren die
ganze Straße beschattet. Wir haben nachgerechnet – das sind 50 Bäume allein von unserer
Schule! Und wenn andere Schulen mitmachen …“* 🌳🌳🌳

**Anmerkung von Herrn Weber:** *„Dieses Projekt lehrt die Kinder Verantwortung, Teamarbeit
und Klimawissenschaft. Sie haben bereits EcoCity-Daten genutzt, um die heißesten Straßen
rund um die Schule zu finden. Der tägliche Gießplan war ihre eigene Idee – ich bin sehr stolz.“*
"""),
    "idea4_top_comment": ('💬 Top comment: *"This is what education should look like. Our school wants to join — can we make this city-wide?"* — Frau Müller, Elly-Heuss-Knapp Gymnasium',
                          '💬 Top-Kommentar: *„So sollte Bildung aussehen. Unsere Schule möchte mitmachen – können wir das stadtweit machen?“* — Frau Müller, Elly-Heuss-Knapp-Gymnasium'),

    # Idea 5: Elderly Crochet Shade Canopy
    "idea5_title": ("Crochet Shade Canopy — Let Us Knit Heilbronn Cool!",
                    "Gehäkeltes Schattendach — Lasst uns Heilbronn kühl stricken!"),
    "idea5_meta": ('Posted by <b>Ingrid H., 67</b> 👵 · Heilbronn Strickgruppe "Goldene Nadeln" · 📍 Marktplatz, Kaiserstrasse · 2 days ago',
                   'Gepostet von <b>Ingrid H., 67</b> 👵 · Heilbronner Strickgruppe „Goldene Nadeln“ · 📍 Marktplatz, Kaiserstraße · vor 2 Tagen'),
    "idea5_caption": ("📸 Reference: Tejiendo la Calle, Valverde de la Vera & Alhaurín de la Torre, Spain",
                      "📸 Vorbild: Tejiendo la Calle, Valverde de la Vera & Alhaurín de la Torre, Spanien"),
    "idea5_body": ("""
*"Liebe Heilbronner! Our knitting circle has 25 members, ages 58 to 82. We've been meeting
every Wednesday for years. When we saw what the women in Spain did — crocheting beautiful
shade canopies over their streets — we said: WE CAN DO THIS TOO!"* 👵🧶

**Our proposal:**
- Our group "Goldene Nadeln" will crochet colorful shade panels from recycled yarn
- We string them between buildings over Kaiserstrasse and Marktplatz in summer
- Each panel is a unique artwork — we'll weave in Heilbronn landmarks and patterns
- **We just need the city to provide yarn and the hanging infrastructure!**

**Why it works — proven in Spain:**
In Valverde de la Vera, elderly women created "Tejiendo la Calle" (Knitting the Street) —
XXL crochet sunshades that cool streets by up to 5°C. In Alhaurín de la Torre near Malaga,
40 women crocheted a 13,000 sq ft canopy over the shopping street. Both projects won
European awards.

**What we bring:** Community spirit, skilled hands, and time. What we need: yarn,
metal cables between buildings, and the city's blessing.

**If this project gets accepted, we'll need more hands!** We will post a meetup in the
Community Hub to recruit new members — all ages welcome, beginners too. We'll teach you! 🧶

Let's knit Heilbronn cool! 🧶❤️
""", """
*„Liebe Heilbronner! Unser Strickkreis hat 25 Mitglieder zwischen 58 und 82 Jahren. Wir treffen
uns seit Jahren jeden Mittwoch. Als wir gesehen haben, was die Frauen in Spanien gemacht haben –
wunderschöne Schattendächer über ihre Straßen zu häkeln –, haben wir gesagt: DAS KÖNNEN WIR AUCH!“* 👵🧶

**Unser Vorschlag:**
- Unsere Gruppe „Goldene Nadeln“ häkelt bunte Schattenbahnen aus recyceltem Garn
- Im Sommer spannen wir sie zwischen den Gebäuden über Kaiserstraße und Marktplatz
- Jede Bahn ist ein Unikat – wir häkeln Heilbronner Wahrzeichen und Muster hinein
- **Wir brauchen von der Stadt nur Garn und die Aufhängung!**

**Warum es funktioniert – in Spanien erprobt:**
In Valverde de la Vera haben ältere Frauen „Tejiendo la Calle“ (Die Straße stricken) ins Leben
gerufen – riesige gehäkelte Sonnensegel, die Straßen um bis zu 5 °C abkühlen. In Alhaurín de la
Torre bei Málaga häkelten 40 Frauen ein rund 1.200 m² großes Dach über die Einkaufsstraße. Beide
Projekte wurden mit europäischen Preisen ausgezeichnet.

**Was wir mitbringen:** Gemeinschaftssinn, geschickte Hände und Zeit. Was wir brauchen: Garn,
Stahlseile zwischen den Gebäuden und den Segen der Stadt.

**Wenn das Projekt angenommen wird, brauchen wir mehr Hände!** Wir posten dann ein Treffen im
Community-Treffpunkt, um neue Mitglieder zu gewinnen – alle Altersgruppen willkommen, auch
Anfänger. Wir bringen es euch bei! 🧶

Lasst uns Heilbronn kühl stricken! 🧶❤️
"""),
    "idea5_top_comment": ('💬 Top comment: *"This is the most beautiful idea! My Oma wants to join!"* — Lena, 29',
                          '💬 Top-Kommentar: *„Das ist die schönste Idee überhaupt! Meine Oma will mitmachen!“* — Lena, 29'),

    # Dashboard tab
    "dashboard_header": ("📊 Heilbronn Bike Sensor Analysis", "📊 Auswertung der Heilbronner Sensor-Räder"),
    "dashboard_caption": ("openSenseMap bike sensors · {sensors} bikes · {points} readings · {first} to {last}",
                          "openSenseMap-Fahrradsensoren · {sensors} Räder · {points} Messwerte · {first} bis {last}"),
    "areas_ranked": ("Areas Ranked", "Bewertete Gebiete"),
    "coolest_area": ("Coolest Area", "Kühlstes Gebiet"),
    "most_dust": ("Most Fine Dust", "Am meisten Feinstaub"),
    "temp_vs_city": ("{v:+.2f}°C vs. city", "{v:+.2f} °C ggü. Stadt"),
    "pm_vs_city": ("{v:+.2f} µg/m³ vs. city", "{v:+.2f} µg/m³ ggü. Stadt"),
    "chart_temp_vs_city": ("Temperature vs. City (same hour)", "Temperatur ggü. Stadt (selbe Uhrzeit)"),
    "chart_pm_vs_city": ("Fine Dust (PM2.5) vs. City (same hour)", "Feinstaub (PM2.5) ggü. Stadt (selbe Uhrzeit)"),
    "area": ("Area", "Gebiet"),
    "gaps_tendency": ("The gaps between areas are small (a few tenths of a degree), so read them as tendencies.",
                      "Die Unterschiede zwischen den Gebieten sind klein (wenige Zehntelgrad), lies sie also als Tendenz."),
    "ranking_header": ("📡 Area Ranking", "📡 Rangliste der Gebiete"),
    "ranking_caption": ("Rank 1 = coolest and cleanest. Differences are compared with all sensors at the same hour.",
                        "Rang 1 = am kühlsten und saubersten. Die Unterschiede sind mit allen Sensoren zur selben Uhrzeit verglichen."),
    "livability_formula": ("🏙️ Livability (0–100) = {parts}. Above 60 green, 50–60 white, below 50 red (45 = strongest red).",
                           "🏙️ Lebensqualität (0–100) = {parts}. Über 60 grün, 50–60 weiß, unter 50 rot (45 = kräftigstes Rot)."),
    "part_air": ("air", "Luft"),
    "part_heat": ("heat", "Hitze"),
    "part_bike": ("bike", "Rad"),
    "col_rank": ("Rank", "Rang"),
    "col_temp_diff": ("Temp diff (°C)", "Temp.-Differenz (°C)"),
    "col_temp_avg": ("Avg temp (°C)", "Ø Temp. (°C)"),
    "col_pm_diff": ("PM2.5 diff (µg/m³)", "PM2.5-Differenz (µg/m³)"),
    "col_pm_avg": ("Avg PM2.5 (µg/m³)", "Ø PM2.5 (µg/m³)"),
    "col_days": ("Days", "Tage"),
    "needs_help": ("🎯 Where Heilbronn Needs Help", "🎯 Wo Heilbronn Hilfe braucht"),
    "help_warmest": ("**🔥 Warmest areas** (more shade and trees)", "**🔥 Wärmste Gebiete** (mehr Schatten und Bäume)"),
    "help_dust": ("**🌫️ Most fine dust** (less traffic, more green)", "**🌫️ Am meisten Feinstaub** (weniger Verkehr, mehr Grün)"),
    "help_bumpy": ("**🛣️ Bumpiest bike roads** (repair first)", "**🛣️ Holprigste Radstraßen** (zuerst reparieren)"),
    "roughness": ("roughness {v:.0f}", "Rauheit {v:.0f}"),
    "where_measured": ("🗺️ Where the Sensor Bikes Measured", "🗺️ Wo die Sensor-Räder gemessen haben"),
    "where_measured_intro": ("Purple = streets the sensor bikes rode (darker = more readings). Circles = the ranked areas.",
                             "Lila = Straßen, die die Sensor-Räder befahren haben (dunkler = mehr Messwerte). Kreise = die bewerteten Gebiete."),
    "coverage_tooltip": ("📡 {area} — {readings} readings on {days} days", "📡 {area} — {readings} Messwerte an {days} Tagen"),

    # Footer
    "footer": ("🌿 EcoCity HN — Green City Heilbronn Hackathon | Data: openSenseMap · OpenStreetMap",
               "🌿 EcoCity HN — Green City Heilbronn Hackathon | Daten: openSenseMap · OpenStreetMap"),
}

# ─── German names for option values and data categories (English value -> German) ───
OPTIONS_DE = {
    # Activities
    "Jogging": "Joggen", "Walking": "Spazieren", "Cycling": "Radfahren",
    "Yoga": "Yoga", "Workout": "Workout", "Other": "Sonstiges",
    # Issues
    "Broken fountain": "Defekter Brunnen", "No shade": "Kein Schatten", "Trash": "Müll",
    "Unsafe": "Unsicher", "Needs seating": "Sitzplätze fehlen", "Needs water": "Wasser fehlt",
    # Suggestions
    "More trees": "Mehr Bäume", "Water fountain": "Trinkbrunnen", "Cooling station": "Kühlstation",
    "Benches": "Sitzbänke", "Better lighting": "Bessere Beleuchtung",
    "Pet water station": "Wasserstelle für Haustiere", "Sensor box": "Sensorbox",
    "Mist cooling zone": "Sprühnebel-Kühlzone",
    # Urgency
    "Nice to have": "Wäre schön", "Would help": "Würde helfen", "Needed": "Notwendig", "Urgent": "Dringend",
    # Idea categories / badges
    "Cooling Infrastructure": "Kühl-Infrastruktur", "Water & Drinking Fountains": "Wasser & Trinkbrunnen",
    "Sensor Network": "Sensornetz", "Green Spaces": "Grünflächen", "Pet Friendly": "Haustierfreundlich",
    "Accessibility": "Barrierefreiheit", "Kids Initiative": "Kinder-Initiative",
    "Community Project": "Gemeinschaftsprojekt",
    # Most requested
    "Trees": "Bäume", "Fountains": "Brunnen", "Cooling": "Kühlung",
    "Pet Water": "Wasser für Tiere", "Sensors": "Sensoren",
}

# ─── German versions of the demo data texts ───
MEETUPS_DE = {
    1: ("Morgenlauf am Neckar", "Früher Morgenlauf am Fluss entlang, bevor die Hitze kommt. ca. 5 km."),
    2: ("Yoga im Park", "Yoga im Freien im Schatten. Bring deine eigene Matte mit!"),
    3: ("Rundgang zu kühlen Orten", "Geführter Spaziergang zu Heilbronns kühlsten Orten."),
    4: ("Radtour im Wald", "Schattige Waldstrecke. ca. 10 km, mittelschwer."),
}

RATING_COMMENTS_DE = {
    "Waldgebiet Jaegerhaus": "Kühlster Ort der Stadt",
    "Wertwiesenpark": "Viel Schatten, immer ein laues Lüftchen",
    "Neckarufer Sued": "Angenehme Brise vom Fluss",
    "Pfuehlpark": "Gut, aber Brunnen defekt",
    "Bildungscampus": "Etwas Schatten, überwiegend Beton",
    "Hauptbahnhof": "Hitzefalle aus Beton",
    "Marktplatz": "Zu heiß, nachmittags meiden",
}


def translate(key, lang, **kwargs):
    text = T[key][1 if lang == "de" else 0]
    return text.format(**kwargs) if kwargs else text


def translate_option(value, lang):
    return OPTIONS_DE.get(value, value) if lang == "de" else value


# ─── Shortcuts for the current page language (set by the ENG / DE switch, key "lang_de") ───
def get_lang():
    return "de" if st.session_state.get("lang_de") else "en"


def t(key, **kwargs):
    return translate(key, get_lang(), **kwargs)


def opt(value):
    return translate_option(value, get_lang())
