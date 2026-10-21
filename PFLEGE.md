# Haus Dalmatia – Pflege der Website

Die Startseite ist eine einzelne, statische Datei (`index.html`) ohne externe Abhängigkeiten:
Schriften (Marcellus für Überschriften, Figtree für Text) liegen in `fonts/`, Icons (Lucide, ISC-Lizenz) als SVG-Sprite in `index.html`, optimierte Bilder in `bilder/web/` (WebP). Es werden keine Cookies
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
- Titelbild: vier Fotos blenden nacheinander über (`TITELBILD` im Skript). Reihenfolge = Reihenfolge der `hero-bg`-Bilder im HTML.

## Effekte

Überschrift-Animation, Einblenden beim Scrollen, Vorhang-Effekt bei Fotos, Zähler, Parallaxe, goldene
Fortschrittslinie, Laufband und Lichtspiel auf dem Poolfoto stehen im Skriptblock `EFFEKTE` bzw. im CSS
unter „Effekte“. Sie schalten sich bei „Bewegung reduzieren“ automatisch ab; ohne Skript ist alles sichtbar.
Galerie „Einblicke“: Bilder im Abschnitt `GALERIE` (Reihenfolge = Reihenfolge im HTML).

## Vor dem Livegang zu klären

1. **Strandentfernung:** alte Website „300 m“, Booking.com ca. 700 m – bitte messen. Bis dahin steht „wenige Gehminuten“.
2. **Gastgeber:** Website nennt Marijana, Booking-Gäste nennen „Atila und Ante“ – Geschichte vereinheitlichen.
3. **Pool-Heizung:** In welchen Monaten wird beheizt, welche Wassertemperatur? (stärkstes Argument für Mai/Juni/Sept./Okt.)
4. **Preise & Mindestaufenthalt** je Apartment und Saison.
5. **Sprachen der Gastgeberin:** „Deutsch, Kroatisch, Englisch“ bestätigen.
6. **Impressum:** OIB, Rješenje, Kategorie eintragen; Hosting-Anbieter in der Datenschutzerklärung.
7. **Booking.com-Listing:** „Lake view“ und „2 swimming pools“ korrigieren; Wert 9,9/10 (44 Bewertungen, Stand 21.10.2026) regelmäßig aktualisieren.
8. Alte Booking-Links der WordPress-Seite (fremde `aid`, Datum 2025) entfallen mit dieser Seite.
