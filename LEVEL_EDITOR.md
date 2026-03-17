# Level-Editor – Dokumentation

## Überblick

Der Level-Editor von "Prinz von Ehrenfeld" läuft **vollständig im laufenden Spiel** – kein Unity-Editor nötig. Spieler können eigene Level bauen, speichern, laden und sofort testen.

---

## Bedienung

### Starten

Im Hauptmenü: **"Bau dinge Veedel!"** auswählen → Editor-Szene startet.

### Steuerung (PC – Maus/Tastatur)

| Aktion | Eingabe |
|--------|---------|
| Tile platzieren | Linksklick |
| Tile löschen | Rechtsklick |
| Palette öffnen / schließen | `Tab` |
| Nächste Tile-Kategorie | `Q` / `E` |
| Grid-Overlay ein/aus | `G` |
| Kamera bewegen | `Mittlere Maustaste` / `WASD` |
| Kamera zoomen | Mausrad |
| Level testen | `F5` |
| Testlauf beenden | `F5` (erneut) / `Escape` |
| Level speichern | `Strg+S` |
| Level laden | `Strg+O` |
| Rückgängig | `Strg+Z` |
| Wiederholen | `Strg+Y` |

### Steuerung (Controller)

| Aktion | Eingabe |
|--------|---------|
| Cursor bewegen | Linker Stick |
| Tile platzieren | `A` / `Cross` |
| Tile löschen | `B` / `Circle` |
| Palette öffnen | `Y` / `Triangle` |
| Kamera bewegen | Rechter Stick |
| Level testen | `Start` |

---

## Level-Layers

Der Editor arbeitet mit **4 Tilemap-Layern** (von hinten nach vorne):

| Layer | Name | Collider | Beschreibung |
|-------|------|----------|--------------|
| 0 | Background | ❌ | Hintergrunddekoration |
| 1 | Ground | ✅ | Begehbare Plattformen und Wände |
| 2 | Detail | ❌ | Vordergrunddekoration, Schilder |
| 3 | Hazards | ✅ (Trigger) | Gefährliche Tiles (Strom, Stacheln, Wasser) |

Im Editor aktiven Layer über die **Toolbar oben** wechseln.

---

## Tile-Kategorien (Palette)

- **Boden** – Straßenpflaster, Sims, Beton, Erde
- **Plattformen** – schwebende Platten, Metallroste, Holzbretter
- **Gebäude** – Hauswände, Fenster, Türen, Balkon-Kanten
- **Deko** – Graffiti, Mülltonnen, Laternen, Bänke, Pflanzen
- **Gefahr** – Glasscherben, Stromkästen, Wasser, Absturz-Markierung
- **Spezial** – Spawn-Punkt, Checkpoint, Level-Ausgang, Enemy-Spawn, Power-Up-Spawn

---

## Level speichern & laden

### Speicherort

```
Application.persistentDataPath/
└── CustomLevels/
    ├── MeinLevel.json
    └── EhrenfelderNacht.json
```

Unter Windows typisch:  
`C:\Users\NUTZERNAME\AppData\LocalLow\<Company>\<Product>\CustomLevels\`

### Level-Slots

Es gibt **10 benannte Speichelplätze**. Name wird beim Speichern abgefragt.

---

## JSON-Schema (Level-Dateiformat)

```json
{
  "levelName": "EhrenfelderNacht",
  "version": "1.0",
  "createdAt": "2026-03-11T20:00:00Z",
  "metadata": {
    "author": "Kevin M.",
    "playTime": 0,
    "difficulty": 2
  },
  "bounds": {
    "width": 80,
    "height": 20
  },
  "layers": [
    {
      "layerIndex": 0,
      "layerName": "Background",
      "tiles": [
        { "x": 0, "y": 0, "tileId": "bg_wall_brick_01" },
        { "x": 1, "y": 0, "tileId": "bg_wall_brick_01" }
      ]
    },
    {
      "layerIndex": 1,
      "layerName": "Ground",
      "tiles": [
        { "x": 0, "y": -1, "tileId": "ground_concrete_01" },
        { "x": 1, "y": -1, "tileId": "ground_concrete_01" }
      ]
    }
  ],
  "spawnPoints": {
    "playerSpawn": { "x": 2, "y": 0 },
    "levelExit": { "x": 78, "y": 0 },
    "checkpoints": [
      { "id": 0, "x": 20, "y": 0 },
      { "id": 1, "x": 50, "y": 0 }
    ],
    "enemySpawns": [
      { "enemyType": "Tourist", "x": 10, "y": 0 },
      { "enemyType": "Ordnungsamt", "x": 30, "y": 0 }
    ],
    "powerUpSpawns": [
      { "powerUpType": "SpeedBoost", "x": 15, "y": 5 }
    ]
  }
}
```

### Tile-IDs

Tile-IDs entsprechen den Keys im `TileRegistry.asset` (ScriptableObject).  
Format: `{kategorie}_{subkategorie}_{variante}` – z.B. `ground_concrete_01`, `deko_graffiti_02`.

---

## Architektur (Code)

### Klassen-Übersicht

| Klasse | Datei | Zuständigkeit |
|--------|-------|---------------|
| `RuntimeTilemapEditor` | `Level/TilemapEditor/RuntimeTilemapEditor.cs` | Edit/Play-Toggle, Eingabe-Handling, Tile-Platzierung |
| `TilePaletteUI` | `Level/TilemapEditor/TilePaletteUI.cs` | Palette-Anzeige, Tile-Auswahl, Scroll |
| `TilemapSerialization` | `Level/TilemapEditor/TilemapSerialization.cs` | JSON Read/Write, `LevelData`-Klassen |
| `GridGizmo` | `Level/TilemapEditor/GridGizmo.cs` | Visuelles Raster-Overlay |
| `LevelEditorUI` | `UI/LevelEditorUI.cs` | Toolbar, Layer-Selector, Save/Load-Dialog |

### Edit-Mode vs. Play-Mode

```
RuntimeTilemapEditor.IsEditMode (bool)
  true  → TilePaletteUI sichtbar, GridGizmo aktiv, Player-Input gesperrt
  false → Normales Gameplay, kein Grid/Palette sichtbar
```

Umschalten via `F5` oder Toolbar-Button → `GameEvents.OnEditorModeChanged` wird gefeuert.

---

## Einschränkungen

- Level-Größe: max. **120 × 30 Tiles** (Performance-Limit)
- Max. **50 Enemy-Spawns** pro Level
- Max. **10 Speicher-Slots** für Custom Levels
- Kein Undo über Session-Neustart hinaus (kein persistentes Undo-History)
- Getestete Level werden **nicht automatisch gespeichert** (manuell `Strg+S`)
