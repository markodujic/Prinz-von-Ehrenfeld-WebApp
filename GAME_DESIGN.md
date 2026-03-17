# Game Design Document – Prinz von Ehrenfeld

## Elevator Pitch

> Ein überdrehtes 2D-Plattformspiel im modernen Kölner Stadtteil Ehrenfeld. Du spielst einen sympathischen Typen aus dem Veedel, der sich durch Straßen voller Graffiti kämpft, Kölsch-Kronen sammelt, dem Ordnungsamt entkommt und am Ende den echten "Prinz vum Veedel"-Titel ergattert.

---

## Story

**Protagonist:** Kevin „Kev" Mülheimer – ein normaler Typ aus der Ehrenfelder Subkultur. Skater, Club-Gänger, Graffiti-Liebhaber.

**Ausgangssituation:** Der alljährliche "Prinz-Veedel-Wettbewerb" steht an. Wer alle Kölsch-Kronen einsammelt, alle Klischee-Touristen überleben und den gefürchteten Ordnungsamts-Chef "Hauptkommissar Brömmelkamp" besiegt, trägt den Titel für ein Jahr.

**Ziel:** 5 Level durchlaufen, all Collectibles einsammeln, Bosskampf gewinnen → Titel "Prinz von Ehrenfeld" erhalten.

---

## Spielbare Charaktere

### Kev (Standard)
- **Stärken:** Ausgewogen, guter Sprung
- **Schwächen:** Durchschnittliche Geschwindigkeit
- **Look:** Hoodie, Sneaker, Cap
- **Special:** Doppelsprung

### Silla (Schnell)
- **Stärken:** Sehr schnell, langer Dash
- **Schwächen:** Weniger Leben, kleinerer Sprung
- **Look:** Rennrad-Jacke, Fixie-Fahrer-Vibe
- **Special:** Dreifach-Dash

### Jojo (Tank)
- **Stärken:** Viele Leben, Stampf-Angriff
- **Schwächen:** Langsam, kürzerer Sprung
- **Look:** Karneval-Kostüm, auch im Sommer
- **Special:** Bodystomp (schadet Gegnern im Fallradius)

---

## Level-Übersicht

### Level 1 – Die Venloer Straße
**Setting:** Belebte Hauptstraße mit Dönerläden, Graffiti-Wänden, Straßenbahn-Schienen  
**Gegner:** Touristen mit Selfie-Sticks, Bürohengste die spät dran sind  
**Collectibles:** 20 Kölsch-Kronen, 3 Veedel-Sticker  
**Boss:** Keiner (Tutorial-Level)  
**Neues Mechanic:** Laufen, Springen, Collectibles sammeln

### Level 2 – Heliosgelände (Industriebrache)
**Setting:** Verlassenes Fabrikgelände, Graffiti überall, Rohre und Plattformen  
**Gegner:** Ordnungsamt-Streifen, Wachhunde (Mops-Variante)  
**Collectibles:** 30 Kölsch-Kronen, 5 Veedel-Sticker, 1 Power-Up-Kiste  
**Boss:** Keiner  
**Neues Mechanic:** Dash, Wand-Sliding (geplant), Gefahr durch Abgrund

### Level 3 – Club Bahnhof Ehrenfeld
**Setting:** Club-Viertel bei Nacht, Neon-Lichter, Türsteher-Gegner  
**Gegner:** Türsteher (stark), Partygäste (schwarm-artig), DJ-Bouncers  
**Collectibles:** 40 Kölsch-Kronen, 7 Veedel-Sticker, 2 Power-Up-Kisten  
**Boss:** "DJ Brumm" – wirf ihm die richtigen Schallplatten zurück  
**Neues Mechanic:** Objekte zurückwerfen (Schallplatten)

### Level 4 – Ehrenfelder Brücke & Canal
**Setting:** Brücke über den Innenstadtring, darunter Kanalwasser  
**Gegner:** Skater-Gang (schnell, springend), Graffiti-Jäger  
**Collectibles:** 50 Kölsch-Kronen, 10 Veedel-Sticker  
**Boss:** Keiner (Speed-Run-Level, zeitbasiert)  
**Neues Mechanic:** Movable Platforms, Wind-Zonen

### Level 5 – Das Ordnungsamt (Finale)
**Setting:** Das Ordnungsamt-Höhlenhauptquartier (übertrieben bürokratisch)  
**Gegner:** Elite-Ordnungsamt (Schilde, Formular-Werfer), Bürokraten  
**Collectibles:** 60 Kölsch-Kronen  
**Boss:** Hauptkommissar Brömmelkamp (3 Phasen)  
**Neues Mechanic:** Keines – alle Mechaniken kombiniert

---

## Gegner-Typen

### Tourist mit Selfie-Stick
- **Verhalten:** Läuft langsam, hält plötzlich an für Fotos (unberechenbar)
- **Angriff:** Selfie-Stick-Stoß (kurze Reichweite)
- **Schwäche:** Leicht auszuweichen durch Ducken
- **KI-States:** Wander → Foto-Stop → Angriff
- **Drops:** 1–3 Kölsch-Kronen

### Ordnungsamt-Beamter
- **Verhalten:** Patrouilliert in festem Radius, verfolgt bei Sichtkontakt
- **Angriff:** Knöllchen-Wurf (Projektil), Nahkampf
- **Schwäche:** Wird durch Ablenkung (Collectible-Geräusch) abgelenkt
- **KI-States:** Patrol → Chase → Attack → Return
- **Drops:** 2–5 Kölsch-Kronen, selten Power-Up

### Türsteher
- **Verhalten:** Steht still, reagiert auf Lärm / Sichtkontakt
- **Angriff:** Schwerer Nahkampf (ein Treffer reicht), kann nicht übersprungen werden
- **Schwäche:** Kann von der Seite angeschlichen werden
- **KI-States:** Guard → Alert → Attack
- **Drops:** 5–10 Kölsch-Kronen, Checkpoint-Skip-Item

---

## Boss-Phasen: Hauptkommissar Brömmelkamp

### Phase 1 – "Der Formular-Terror"
- Wirft Formularpakete (Projektile) im Bogen
- Bewegt sich langsam, vorhersehbar
- Schwachstelle: Kopf (Stomp von oben)

### Phase 2 (< 60% HP) – "Die Verstärkung"
- Ruft 2 Ordnungsamt-Beamte als Adds
- Geschwindigkeit und Wurffrequenz erhöht
- Schildwall-Fähigkeit (kurz unverwundbar)

### Phase 3 (< 30% HP) – "Der Ausnahmezustand"
- Kompletter Bodenbereich wird gefährlich (Aktenstapel)
- Nur bestimmte Plattformen sicher
- Projektile verfolgen den Spieler (Homing)
- Enrage-Timer (2 Minuten)

---

## Power-Ups

| Name | Kölsch | Dauer | Effekt |
|------|--------|-------|--------|
| Schnell-Kölsch | „Schnäll Kölsch" | 10s | +80% Bewegungsgeschwindigkeit |
| Schild | „Et Schilldche" | 15s | Absorbiert 3 Treffer |
| Unverwundbar | „Unkaputtbar" | 8s | Keine Schadensnahme, blinkt |
| Extra-Leben | „Noch ens Levve" | dauerhaft | +1 Leben |
| Megasprung | „Superjummp" | 12s | 2× Sprunghöhe, kein Fallschaden |

---

## Collectibles

| Item | Wert | Kölsch-Name | Beschreibung |
|------|------|-------------|--------------|
| Kölsch-Krone | 10 Punkte | „Kölsch-Kron" | Überall zu finden |
| Veedel-Sticker | 50 Punkte | „Veedel-Stickche" | Versteckt in Levels |
| Karneval-Konfetti | 25 Punkte | „Kamelle" | Spawnt nach Gegnertod |
| Goldene Kölsch-Krone | 200 Punkte | „Goldkron" | 1× pro Level, sehr versteckt |

---

## Audio-Vision

- **Hauptmenü:** Ruhiger Kölner HipHop-Beat (Lo-Fi / Cologne vibes)
- **Level 1–2:** Uptempo HipHop, Straßen-Feeling
- **Level 3 (Club):** Techno/Electronic, 130 BPM
- **Level 4 (Brücke):** Drum & Bass, Outdoor-Feeling
- **Level 5 (Boss):** Industrial/Punk, intensiv
- **SFX:** Kölsche Ausrufe ("Joot so!", "Alaaf!", "Dat war nix!")

---

## Spieler-Progression

```
Kriesche (Score) = Collectibles × Wert + Zeit-Bonus + Combo-Multiplikator
Zeit-Bonus: max. 500 Punkte (fällt pro Sekunde ab)
Combo: jeder Kill ohne Treffer erhöht Multiplikator × 1.1 (max × 3.0)
```

**Freischaltungen:**
- Charakter Silla: Level 2 abschließen
- Charakter Jojo: Level 4 abschließen
- Geheimer Level: Alle Goldkronen in Level 1–5 finden
