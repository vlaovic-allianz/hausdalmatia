# Haus Dalmatia – Pflege der Website

Die Startseite ist eine einzelne, statische Datei (`index.html`) ohne externe Abhängigkeiten:
Schriften (Marcellus für Überschriften, Figtree für Text, Cormorant Garamond Kursiv für Akzente und Zitate – alle OFL) liegen in `fonts/`, Icons (Lucide, ISC-Lizenz) als SVG-Sprite in `index.html`, optimierte Bilder in `bilder/web/` (WebP). Es werden keine Cookies
gesetzt und keine Drittanbieter geladen.

## Sprachversionen (wichtig)

`index.html` ist die **deutsche Quelle**. Die Seiten `en/`, `pl/` und `hr/` werden daraus erzeugt:

```
python3 build.py
```

Nach **jeder** Änderung an `index.html` (Texte, Bilder, Übersetzungen) einmal ausführen und die erzeugten Dateien mit veröffentlichen.
Das Skript bricht ab, wenn das Übersetzungsobjekt einen Syntaxfehler hat, und meldet fehlende Übersetzungen.
Eine neue Sprache (z. B. Tschechisch) = neuer Block `cs:{…}` in `I18N` + Eintrag in `LOCALES` in `build.py` + Link im Sprachumschalter.

## Häufige Änderungen

| Was | Wo |
|---|---|
| „ab“-Preise pro Apartment | `index.html` → Block `EINSTELLUNGEN` → `prices: { More: 180, … }` (`null` = „Preis auf Anfrage“) |
| Webhook für Anfragen (Make, n8n, Brevo …) | `index.html` → `EINSTELLUNGEN` → `formEndpoint` |
| Deutsche Texte | direkt im HTML |
| Englisch / Polnisch / Kroatisch | `index.html` → Objekt `I18N` (`en`, `pl`, `hr`) – gleicher Schlüssel wie `data-i18n` im HTML, danach `python3 build.py` |
| Impressum / Datenschutz | `impressum.html`, `datenschutz.html` (Felder in `[ … ]` ergänzen) |

Neue Bilder: in `bilder/` ablegen, dann als WebP in 800 px und 1400 px Breite nach `bilder/web/` exportieren.

**Wichtig:** Nach jeder Änderung an den Übersetzungen die Seite einmal im Browser öffnen und die
Entwicklerkonsole prüfen. Ein einziger Syntaxfehler (z. B. ein doppeltes Komma) legt das gesamte
Skript lahm – genau das war der Fehler der Version vom 07.10.2026.

## Bilder

- `bilder/hd/` enthält die aufgewerteten Master-Fotos (Hochskalierung: Meerblick und Apartment More mit Topaz,
  alle übrigen kostenlos mit Real-ESRGAN, Open Source). Daraus werden die WebP-Dateien in `bilder/web/` erzeugt.
- Die Original-Fotos auf der alten WordPress-Seite sind nur etwa 370–600 px breit. Für wirklich scharfe Bilder
  bitte neue Fotos in voller Kameraauflösung aufnehmen (Handy reicht, querformatig, bei gutem Licht).
- Umgebungsfotos (Zadar, Krka, Kornaten): Wikimedia Commons, CC0 bzw. gemeinfrei – geprüft am 21.10.2026.
  Strand- und Wassersportfoto stammen von der eigenen Website; bitte bestätigen, dass sie selbst aufgenommen wurden.
- **Titelfilm** (`bilder/film/`): 21 Sekunden, nahtlose Schleife aus den aufgewerteten Fotos (Balkon, Pool, Strand, Pool mit Palme), ruhige Kamerafahrten.
  Querformat 1920 × 1080 für Computer, Hochformat 720 × 1280 für Handys, jeweils als MP4 (H.264) und WebM (VP9).
  Er wird erst nach dem Laden der Seite geholt und nicht im Datensparmodus, bei sehr langsamer Verbindung oder bei „Bewegung reduzieren“ –
  dann blenden die vier Fotos wie bisher über. Der Pause-Knopf hält auch den Film an.
  Neu erzeugen (z. B. mit neuen Fotos): Skript `werkzeuge/film.py` (Python + Pillow + ffmpeg); die Kamerafahrten stehen dort in `SHOTS`.
  Echte 4K-Qualität braucht 4K-Ausgangsmaterial (Video oder Fotos ab ca. 4.000 px Breite).

## Suchmaschinen & KI-Assistenten

- `build.py` erzeugt pro Sprache übersetzte Strukturdaten (Schema.org) und die FAQ-Daten (`ld-faq`) automatisch aus den sichtbaren Fragen.
  FAQ-Fragen also nur im HTML bzw. in `I18N` pflegen, danach `python3 build.py`.
- `llms.txt` fasst die wichtigsten Fakten für KI-Assistenten zusammen. Bei geänderten Fakten (z. B. Strandentfernung) mitpflegen.
- Bewertungssterne (aggregateRating) sind bewusst **nicht** eingebaut: Booking-Bewertungen dürfen laut Google-Richtlinien nicht als eigenes Markup erscheinen.
- **Beim Umzug von WordPress (wichtig):** Beim Hoster 301-Weiterleitungen einrichten, z. B. `/amenities/` → `/en/#pool`, `/contact/` → `/en/#anfrage`
  sowie alte deutsche und polnische Unterseiten → `/` bzw. `/pl/`. Das Meta-Tag `google-site-verification` aus der alten Seite übernehmen
  (oder die Domain per DNS in der Search Console bestätigen) und danach `sitemap.xml` einreichen.
- Beim Hosting Brotli/Gzip aktivieren und für `bilder/` und `fonts/` lange Cache-Zeiten setzen. Im CDN keine „KI-Bots blockieren“-Option aktivieren.

## Formular

- Die Einwilligungs-Checkbox wurde durch einen Datenschutzhinweis ersetzt (Verarbeitung zur Beantwortung der Anfrage, Art. 6 Abs. 1 lit. b DSGVO).
  **Bitte vor dem Livegang rechtlich bestätigen lassen.**
- Beim Versand per WhatsApp ist die E-Mail-Adresse freiwillig; beim Versand per E-Mail Pflicht.
- Nach dem Absenden erscheint eine Rückfallebene („Anfrage kopieren“, E-Mail-Adresse, WhatsApp-Link), falls sich keine App öffnet.

## Farb-Look und HD-Bilder

- `werkzeuge/look.py` gibt allen Fotos denselben „Haus-Dalmatia-Look“: warmes Adria-Licht, sanfte S-Kurve, Vibrance,
  kühle Schatten und warme Lichter, feine Detailschärfe. Quelle sind die Master in `bilder/hd/` (bzw. die Original-Fotos),
  Ergebnis sind die WebP-Dateien in `bilder/web/` (800/1400/1900 px, Meerblick bis 2200 px) und die Film-Master in `bilder/hd-look/`.
  Neue Fotos: Master in `bilder/hd/` ablegen, in `DIRECT` eintragen, `python3 werkzeuge/look.py` ausführen.
- Danach den Titelfilm neu erzeugen: `python3 werkzeuge/film.py quer` und `hoch` (MP4) sowie jeweils mit `webm`.
- Die Hausfotos stammen von der alten Website und haben real nur ca. 470–700 px Detail. Echte 4K-Schärfe gibt es nur mit
  Original-Aufnahmen in voller Auflösung – diese bitte in `bilder/original/` ablegen.

## Bewegung (GSAP)

`js/bewegung.js` (eigener Code) mit GSAP 3.13 + ScrollTrigger (`js/`, offizielles npm-Paket, „Standard no charge“-Lizenz):
Titeltext gleitet beim Scrollen weg, Fotos mit Tiefenwirkung, Lichtschein auf den Karten „Direkt buchen“.

## Effekte

**Luxus-Details** (Skriptblock `LUXUS`, CSS „LUXUS-DETAILS“):
- Begrüßungsvorhang mit Monogramm – nur beim ersten Seitenaufruf pro Sitzung, endet nach etwa 2,5 Sekunden auch ohne Skript.
- Sanftes Scrollen mit Lenis 1.1.20 (MIT-Lizenz, lokal eingebettet, nur mit Maus/Trackpad; Handys scrollen nativ).
- Eleganter Cursor mit „Ansehen“/„Ziehen“ über Fotos und Galerie (nur Maus), magnetische Gold-Knöpfe.
- Überschriften gleiten Wort für Wort aus einer Maske; Abschnittsnummern 01–11 erscheinen automatisch.
- „Ein Tag im Haus Dalmatia“ (`#tag`): auf dem Desktop bleibt der Abschnitt stehen und die fünf Momente fahren seitwärts;
  auf dem Handy wischt man. Bilder und Texte im HTML bzw. `I18N` (`day.*`).
- Ausflugskarte: Linien zeichnen sich nacheinander, das Haus pulsiert. Titelbild mit feinem Goldrahmen und „Entdecken“-Hinweis.
- Alles schaltet sich bei „Bewegung reduzieren“ ab.


Überschrift-Animation, Einblenden beim Scrollen, Vorhang-Effekt bei Fotos, Zähler, Parallaxe, goldene
Fortschrittslinie, Laufband und Lichtspiel auf dem Poolfoto stehen im Skriptblock `EFFEKTE` bzw. im CSS
unter „Effekte“. Sie schalten sich bei „Bewegung reduzieren“ automatisch ab; ohne Skript ist alles sichtbar.
Galerie „Einblicke“: Bilder im Abschnitt `GALERIE` (Reihenfolge = Reihenfolge im HTML).
Barrierefreiheit: Die Titel-Diashow hat einen Pause-Knopf, das Laufband hält beim Antippen an; Menü und Bildansicht halten den Tastaturfokus.

## Vor dem Livegang zu klären

1. **Strandentfernung:** alte Website „300 m“, Booking.com ca. 700 m – bitte messen. Bis dahin steht „wenige Gehminuten“.
2. **Gastgeber:** Website nennt Marijana, Booking-Gäste nennen „Atila und Ante“ – Geschichte vereinheitlichen.
3. **Pool-Heizung:** In welchen Monaten wird beheizt, welche Wassertemperatur? (stärkstes Argument für Mai/Juni/Sept./Okt.)
4. **Preise & Mindestaufenthalt** je Apartment und Saison.
5. **Sprachen der Gastgeberin:** „Deutsch, Kroatisch, Englisch“ bestätigen.
6. **Impressum:** OIB, Rješenje, Kategorie eintragen; Hosting-Anbieter in der Datenschutzerklärung.
7. **Porträt der Gastgeberin** (rund, gern mit Unterschrift) für die Willkommenskarte – stärkt das Vertrauen bei Direktbuchung.
8. **Booking.com-Listing:** „Lake view“ und „2 swimming pools“ korrigieren; Wert 9,9/10 (44 Bewertungen, Stand 21.10.2026) regelmäßig aktualisieren.
9. Alte Booking-Links der WordPress-Seite (fremde `aid`, Datum 2025) entfallen mit dieser Seite.
