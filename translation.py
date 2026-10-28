import streamlit as st

# ─── UI texts: key -> (English, German) ───
T = {
    # Sidebar
    "tagline": ("Making Heilbronn liveable", "Heilbronn lebenswert machen"),
    "winter_mode": ("Winter Mode ❄️", "Wintermodus ❄️"),
    "map_layers": ("Map Layers", "Kartenebenen"),
    "layer_temp": ("Temperature", "Temperatur"),
    "layer_water": ("Drinking Water", "Trinkwasser"),
    "layer_cool": ("Cool Spots", "Kühle Orte"),
    "layer_air": ("Air Quality", "Luftqualität"),

    # Tabs
    "tab_map": ("🗺️ City Map", "🗺️ Stadtkarte"),
    "tab_community": ("👥 Community", "👥 Community"),
    "tab_rate": ("⭐ Rate & Report", "⭐ Bewerten & Melden"),
    "tab_dashboard": ("📊 Dashboard", "📊 Dashboard"),

    # Map tab
    "map_header_summer": ("☀️ Heilbronn Climate Map", "☀️ Klimakarte Heilbronn"),
    "map_header_winter": ("❄️ Heilbronn Climate Map", "❄️ Klimakarte Heilbronn"),
    "avg_temp": ("Avg Temp", "Ø Temperatur"),
    "avg_humidity": ("Avg Humidity", "Ø Luftfeuchtigkeit"),
    "avg_pm25": ("Avg PM2.5", "Ø PM2.5"),
    "comfort": ("Comfort", "Komfort"),
    "humidity": ("Humidity", "Luftfeuchtigkeit"),
    "hottest": ("🔥 Hottest", "🔥 Am heißesten"),
    "coolest": ("❄️ Coolest", "❄️ Am kühlsten"),
    "reset_view": ("🔄 Reset View", "🔄 Ansicht zurücksetzen"),
    "selected": ("📍 Selected: {name}", "📍 Ausgewählt: {name}"),

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
    "you": ("You", "dir"),
    "joined": ("✅ Joined", "✅ Dabei"),
    "full": ("Full", "Ausgebucht"),
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
    "image_missing": ("📷 Image: {file} not found — place it in the images folder",
                      "📷 Bild: {file} nicht gefunden — lege es in den Ordner images"),

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
    "dashboard_header": ("📊 July 2026 Analysis", "📊 Analyse Juli 2026"),
    "sensors": ("Sensors", "Sensoren"),
    "hot_days": ("Hot Days (>35°C)", "Hitzetage (>35 °C)"),
    "coolest_spot": ("Coolest Spot", "Kühlster Ort"),
    "worst_air": ("Worst Air", "Schlechteste Luft"),
    "chart_daily_temp": ("Typical Daily Temperature by Area Type",
                         "Typischer Temperaturverlauf nach Gebietstyp"),
    "chart_pm": ("PM2.5 Throughout the Day", "PM2.5 im Tagesverlauf"),
    "chart_temp_location": ("Temperature by Location", "Temperatur nach Ort"),
    "hour": ("Hour", "Uhrzeit"),
    "area_type": ("Area type", "Gebietstyp"),
    "location": ("Location", "Ort"),
    "needs_help": ("🎯 Where Heilbronn Needs Help", "🎯 Wo Heilbronn Hilfe braucht"),
    "hottest_least_infra": ("**Hottest areas with least infrastructure:**",
                            "**Heißeste Gebiete mit der wenigsten Infrastruktur:**"),
    "recommendations": ("**Recommendations:**", "**Empfehlungen:**"),
    "rec_trees_industrie": ("🌳 Plant trees at **Neckargartach Industrie** — hottest, worst air",
                            "🌳 Bäume pflanzen in **Neckargartach Industrie** — am heißesten, schlechteste Luft"),
    "rec_fountain_kaiser": ("💧 Add fountain at **Kaiserstrasse** — high foot traffic, no water",
                            "💧 Brunnen an der **Kaiserstrasse** ergänzen — viele Fußgänger, kein Wasser"),
    "rec_shade_bahnhof": ("🏗️ Shade structure at **Hauptbahnhof** — transit hub, people wait in heat",
                          "🏗️ Schattenspender am **Hauptbahnhof** — Verkehrsknoten, Menschen warten in der Hitze"),
    "rec_fix_pfuehl": ("🔧 Fix fountain at **Pfuehlpark** — reported broken",
                       "🔧 Brunnen im **Pfuehlpark** reparieren — als defekt gemeldet"),
    "rec_canopy_markt": ("🌳 Expand canopy at **Marktplatz** — tourist area, consistently hot",
                         "🌳 Mehr Baumkronen am **Marktplatz** — Touristengebiet, durchgehend heiß"),
    "coverage_header": ("📡 Sensor Coverage & Green Zone Gaps", "📡 Sensorabdeckung & Lücken bei Grünzonen"),
    "coverage_intro": ("Green circles show sensor coverage (~300m). Gaps indicate areas needing additional sensors or green infrastructure.",
                       "Grüne Kreise zeigen die Sensorabdeckung (~300 m). Lücken markieren Gebiete, die zusätzliche Sensoren oder grüne Infrastruktur brauchen."),
    "gap": ("GAP", "LÜCKE"),
    "gap_residential": ("No sensors, residential area", "Keine Sensoren, Wohngebiet"),
    "gap_suburb": ("No sensors, growing suburb", "Keine Sensoren, wachsender Vorort"),
    "gap_highway": ("No sensors, near highway", "Keine Sensoren, nahe Autobahn"),
    "gap_dense": ("No sensors, dense housing", "Keine Sensoren, dichte Bebauung"),
    "coverage_legend": ("""
**Legend:**
🟢 Green circles = current sensor coverage (~300m radius)
🔴 Red zones = coverage gaps — priority areas for new sensors or green infrastructure
""", """
**Legende:**
🟢 Grüne Kreise = aktuelle Sensorabdeckung (~300 m Radius)
🔴 Rote Zonen = Abdeckungslücken — vorrangige Gebiete für neue Sensoren oder grüne Infrastruktur
"""),

    # Footer
    "footer": ("🌿 EcoCity HN — Green City Heilbronn Hackathon | Data: openSenseMap · Sensor.Community · Open-Meteo",
               "🌿 EcoCity HN — Green City Heilbronn Hackathon | Daten: openSenseMap · Sensor.Community · Open-Meteo"),
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
    # Chart area types
    "Park": "Park", "Urban Center": "Innenstadt", "Waterfront": "Flussufer", "Industrial": "Industrie",
    # Fountain status
    "working": "funktioniert", "broken": "defekt", "dry": "trocken",
}

# Sensor types are stored as ids in the data, so both languages need a label
SENSOR_TYPES = {
    "urban_center": ("City centre", "Innenstadt"),
    "park": ("Park", "Park"),
    "transit": ("Transit hub", "Verkehrsknoten"),
    "shopping": ("Shopping street", "Einkaufsstraße"),
    "waterfront": ("Waterfront", "Flussufer"),
    "industrial": ("Industrial", "Industrie"),
    "sports": ("Sports ground", "Sportstätte"),
    "old_town": ("Old town", "Altstadt"),
    "forest": ("Forest", "Wald"),
    "residential": ("Residential", "Wohngebiet"),
    "campus": ("Campus", "Campus"),
    "open_field": ("Open field", "Freifläche"),
}

# ─── German versions of the demo data texts ───
COOL_SPOTS_DE = {
    "Wertwiesenpark Schattenplatz": "Schattiger Platz mit Bänken unter alten Bäumen",
    "Stadtbibliothek": "Klimatisierte Stadtbibliothek, Eintritt frei",
    "Neckarufer Promenade": "Luftiger Spazierweg am Fluss, 2–3 Grad kühler",
    "Waldgebiet Trails": "Waldwege, bis zu 5 Grad kühler",
    "Pfuehlpark Schattenweg": "Baumgesäumte Wege mit gutem Schatten",
    "Harmonie Center": "Klimatisiertes Einkaufszentrum",
    "Experimenta Vorplatz": "Schattiger Bereich beim Science Center",
}

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


def translate_sensor_type(type_id, lang):
    labels = SENSOR_TYPES.get(type_id)
    if labels is None:
        return type_id
    return labels[1 if lang == "de" else 0]


# ─── Shortcuts for the current page language (set by the ENG / DE switch, key "lang_de") ───
def get_lang():
    return "de" if st.session_state.get("lang_de") else "en"


def t(key, **kwargs):
    return translate(key, get_lang(), **kwargs)


def opt(value):
    return translate_option(value, get_lang())
