# Asset-Quellen – Prinz von Ehrenfeld

Alle verwendeten Assets sind open-source lizenziert. Keine kommerziell eingeschränkten Assets ohne explizite Genehmigung.

**Lizenz-Kurzreferenz:**

| Kürzel | Bedeutung | Kommerziell erlaubt | Attribution nötig |
|--------|-----------|---------------------|-------------------|
| CC0 | Public Domain | ✅ | ❌ |
| CC-BY 3.0/4.0 | Creative Commons Attribution | ✅ | ✅ |
| CC-BY-SA 4.0 | Attribution + ShareAlike | ✅ | ✅ |
| OGA-BY 3.0 | OpenGameArt Attribution | ✅ | ✅ |
| MIT | MIT License | ✅ | ✅ |

---

## Sprites & Grafiken

### Tilesets (Level)

| Asset | Quelle | Lizenz | Verwendung |
|-------|--------|--------|------------|
| City Kit (Commercial) | [kenney.nl/assets/city-kit-commercial](https://kenney.nl/assets/city-kit-commercial) | CC0 | Haupttileset Level 1, 5 |
| Pixel Platformer | [kenney.nl/assets/pixel-platformer](https://kenney.nl/assets/pixel-platformer) | CC0 | Platformer-Tiles, Level 2 |
| Urban Tileset | [opengameart.org/content/urban-tileset-city-pack](https://opengameart.org) | CC-BY 3.0 | Detailtiles, Hintergründe |
| Industrial Zone Tileset | [opengameart.org](https://opengameart.org) | CC0 | Level 2 (Heliosgelände) |
| _Ggf. eigene Tiles_ | Eigene Erstellung | — | Custom Ehrenfeld-Details |

### Character & Enemy Sprites (SpriteCook – KI-generiert)

Alle Charakter- und Gegner-Sprites wurden mit **SpriteCook** im 16-Bit-SNES-Stil generiert.  
Stil-Referenz: *"16-bit SNES-style 2D platformer sprite, Cologne urban Ehrenfeld theme, pixel art"*

Dateipfad: `Assets/Art/Sprites/Placeholder/`

| Datei | Charakter | SpriteCook Asset-ID | Beschreibung |
|-------|-----------|---------------------|--------------|
| `Player.png` | Kev (Protagonist) | `5adebfa3-ea58-471e-8475-57f4bfe3fe29` | Hoodie, Cap, Sneaker – Ehrenfelder Typ |
| `Hooliganito.png` | Hooliganito | *(letzter Job)* | Kleiner Schläger, Trainingsanzug |
| `KioskRaeuber.png` | KioskRäuber | *(letzter Job)* | Kioskbetreiber-Gegner |
| `TalentscoutKurt.png` | TalentscoutKurt | *(letzter Job)* | Talentscout im Anzug |
| `Broemmelkamp.png` | Brömmelkamp (Boss) | *(letzter Job)* | Hauptkommissar-Kostüm, 3 Phasen |
| `Collectible_Koelsch.png` | Kölsch-Krone | *(letzter Job)* | Collectible-Item |
| `PowerUp.png` | Power-Up | *(letzter Job)* | Generisches Power-Up-Icon |
| `Checkpoint.png` | Checkpoint | *(letzter Job)* | Fahne / Checkpoint-Marker |

**Für Regeneration** denselben Stil-Prompt verwenden:
```
16-bit SNES-style 2D platformer sprite, Cologne urban Ehrenfeld theme,
pixel art, transparent background, single character/item, front-facing
```

Als Stil-Referenz immer Player-Asset-ID `5adebfa3-ea58-471e-8475-57f4bfe3fe29` angeben.

**Lizenz:** SpriteCook – kommerzielle Nutzung gemäß SpriteCook-AGB erlaubt.



### UI / Icons

| Asset | Quelle | Lizenz | Verwendung |
|-------|--------|--------|------------|
| Kenney UI Pack | [kenney.nl/assets/ui-pack](https://kenney.nl/assets/ui-pack) | CC0 | Buttons, Panels, Rahmen |
| Game Icons | [kenney.nl/assets/game-icons](https://kenney.nl) | CC0 | HUD-Icons |
| RPG GUI | [opengameart.org](https://opengameart.org) | CC-BY 3.0 | Menü-Elemente |

---

## Audio

### Musik (BGM)

| Track | Quelle | Lizenz | Verwendung |
|-------|--------|--------|------------|
| _TBD: Kölner HipHop Beat_ | [ccMixter](https://ccmixter.org) | CC-BY | Hauptmenü |
| _TBD: Uptempo Urban_ | [Free Music Archive](https://freemusicarchive.org) | CC-BY | Level 1–2 |
| _TBD: Techno/Electronic_ | [ccMixter](https://ccmixter.org) | CC-BY | Level 3 (Club) |
| _TBD: Drum & Bass_ | [Free Music Archive](https://freemusicarchive.org) | CC-BY | Level 4 |
| _TBD: Industrial/Punk_ | [Incompetech](https://incompetech.com) | CC-BY | Level 5 / Boss |

### Soundeffekte (SFX)

| Asset | Quelle | Lizenz | Verwendung |
|-------|--------|--------|------------|
| Kenney Impact Sounds | [kenney.nl/assets/impact-sounds](https://kenney.nl) | CC0 | Gegner-Hits, Landung |
| Kenney UI Audio | [kenney.nl/assets/ui-audio](https://kenney.nl) | CC0 | Menü-Sounds |
| Kenney Sci-Fi Sounds | [kenney.nl/assets/sci-fi-sounds](https://kenney.nl) | CC0 | Power-Up-Effekte |
| Jump Sounds Pack | [opengameart.org](https://opengameart.org) | CC0 | Sprung-SFX |
| Collectible SFX Pack | [opengameart.org](https://opengameart.org) | CC0 | Kölsch-Krone aufsammeln |
| _Kölsche Sprach-SFX_ | Eigene Aufnahmen | — | "Joot so!", "Alaaf!" etc. |

---

## Fonts

| Font | Quelle | Lizenz | Verwendung |
|------|--------|--------|------------|
| Press Start 2P | [Google Fonts](https://fonts.google.com/specimen/Press+Start+2P) | OFL (Open Font License) | Hauptschrift UI/HUD |
| Pixelify Sans | [Google Fonts](https://fonts.google.com/specimen/Pixelify+Sans) | OFL | Dialoge, Untertitel |

---

## Attribution-Vorlage (für Credits-Screen)

```
Grafiken:
  Kenney (kenney.nl) – CC0 Public Domain
  OpenGameArt-Autoren (credits je Asset, siehe ASSET_SOURCES.md)

Musik:
  [Titel] von [Künstler] – CC-BY [Version]
  Bezugsquelle: [URL]

Soundeffekte:
  Kenney (kenney.nl) – CC0 Public Domain
  OpenGameArt-Autoren – CC0 / CC-BY

Fonts:
  Press Start 2P – Google Fonts / OFL
  Pixelify Sans – Google Fonts / OFL
```

---

> **Hinweis:** Vor jedem Release diese Datei aktualisieren und alle tatsächlich verwendeten Assets mit exakten URLs und Autoren eintragen. CC-BY-Lizenzen erfordern Attribution im Credits-Screen des Spiels.
