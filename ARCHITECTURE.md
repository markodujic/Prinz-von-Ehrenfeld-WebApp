# Architektur – Prinz von Ehrenfeld

## Überblick

Das Spiel ist als **Unity 6 (6000.x) 2D-Platformer** aufgebaut. Die Architektur folgt klaren Trennlinien zwischen Gameplay-Systemen, Konfigurationsdaten und UI – verbunden über einen zentralen EventBus.

```
┌─────────────────────────────────────────────────────────┐
│                      GameManager                        │
│         (Spielzustand, Level-Flow, Game Over)           │
└───────────────┬─────────────────────┬───────────────────┘
                │                     │
        ┌───────▼──────┐     ┌────────▼────────┐
        │  EventBus    │     │   SaveManager   │
        │  (Pub/Sub)   │     │   (JSON)        │
        └──────┬───────┘     └─────────────────┘
               │
   ┌───────────┼────────────────────────────────┐
   │           │                │               │
┌──▼──┐  ┌────▼────┐  ┌────────▼──────┐  ┌────▼────┐
│Player│  │ Enemy   │  │  LevelManager │  │  UI     │
│State │  │ State   │  │  + Tilemap    │  │ Manager │
│Machine│ │Machine  │  │  + Editor     │  └─────────┘
└─────┘  └─────────┘  └───────────────┘
```

---

## Design Patterns

### 1. State Machine (Player & Enemy)

Jede Spielfigur hat eine eigene `StateMachine`. Jeder Zustand ist eine eigene C#-Klasse.

```
PlayerStateMachine
├── IdleState
├── RunState
├── JumpState
├── FallState
├── DashState
├── HurtState
└── DeadState
```

**Transitions werden von außen ausgelöst** (z.B. Collision → `TransitionTo<HurtState>()`).

```csharp
public abstract class State
{
    public virtual void Enter() { }
    public abstract void Update();
    public virtual void FixedUpdate() { }
    public virtual void Exit() { }
}
```

### 2. ScriptableObject-Konfiguration

Alle Gameplay-Werte leben in ScriptableObjects, nicht im Code:

| ScriptableObject | Felder |
|-----------------|--------|
| `CharacterData` | Speed, JumpForce, DashForce, MaxHealth, CharacterName, Sprites |
| `EnemyConfig` | PatrolSpeed, ChaseSpeed, AggroRadius, Damage, Health, DropTable |
| `PowerUpConfig` | Duration, EffectType, Magnitude, Icon, SFXClip |
| `LevelConfig` | LevelName, BGMTrack, TileRegistry, SpawnPoints |

### 3. EventBus (Publisher-Subscriber)

Systeme kommunizieren **ausschließlich** über Events. Kein direktes `GetComponent` zwischen unabhängigen Systemen.

```csharp
// GameEvents.cs – alle Events zentral definiert
public static class GameEvents
{
    public static event Action<int>         OnPlayerDamaged;
    public static event Action              OnPlayerDied;
    public static event Action<int>         OnScoreChanged;
    public static event Action<PowerUpConfig> OnPowerUpCollected;
    public static event Action              OnCheckpointReached;
    public static event Action<int>         OnLevelCompleted;
    public static event Action              OnGameOver;
}
```

### 4. Singleton (nur Manager)

```csharp
public class Singleton<T> : MonoBehaviour where T : MonoBehaviour
{
    public static T Instance { get; private set; }

    protected virtual void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = (T)(object)this;
        DontDestroyOnLoad(gameObject);
    }
}
```

Singletons: `GameManager`, `AudioManager`, `SaveManager`  
**Kein Singleton** für: Player, Enemies, UI-Elemente

### 5. Object Pooling

`ObjectPool<T>` aus `Assets/Scripts/Utilities/ObjectPool.cs`.  
Verpflichtend für: `Projectile`, `Collectible`, `Enemy`, `ParticleEffect`-Instanzen.

---

## System-Überblick

### Player-System

```
PlayerController
├── PlayerStateMachine              ← Zustandsverwaltung
├── PlayerMovement                  ← Rigidbody2D-Physik
│   ├── PlayerInputHandler.cs       ← Input-Auswertung (New Input System)  [Movement/]
│   ├── Coyote Time (0.15s)
│   └── Jump Buffer (0.1s)
├── PowerUpHandler                  ← Aktive Effekte
├── Animator                        ← 7 States (Idle/Run/Jump/Fall/Dash/Hurt/Dead)
└── CharacterData (SO)              ← Alle Werte (auto-assigned von PrefabFactory)
```

> `PlayerInputHandler.cs` liegt in `Assets/Scripts/Player/Movement/` – **nicht** im `Player/`-Root.

### Enemy-System

```
EnemyBase
├── EnemyStateMachine
│   ├── PatrolState             ← Waypoint-Patrol
│   ├── ChaseState              ← Raycast-Detection
│   ├── AttackState             ← Melee / Ranged
│   └── DeadState               ← Death + Pooling
└── EnemyConfig (SO)
```

### Level-Editor (Runtime)

```
RuntimeTilemapEditor
├── Edit-Mode Toggle            ← Gameplay pausiert
├── TilePaletteUI               ← Scroll-Liste verfügbarer Tiles
├── GridGizmo                   ← Visuelles Raster
└── TilemapSerialization        ← JSON-Export/Import
    └── CustomLevels/*.json
```

### Save-System

```
SaveManager
├── savegame.json
│   ├── unlockedCharacters: int[]
│   ├── completedLevels: int[]
│   └── lastCheckpoint: { levelId, checkpointId }
├── highscores.json
│   └── entries: { name, score, levelId, time }[]
└── CustomLevels/
    └── *.json (TilemapData)
```

---

## Szenen-Flow

```
MainMenu
  └── CharacterSelect
        └── Level_01 → Level_02 → ... → Level_05
              └── Boss
  └── LevelEditor
        └── (Beliebiges CustomLevel spielbar)
```

---

---

## Editor-Automatisierung (`Assets/Editor/`)

Alle Szenen, Prefabs, Animationen und Assets werden **vollautomatisch** per Editor-Script erzeugt – kein manuelles Aufsetzen in Unity nötig.

### Einstiegspunkt

`Tools → Prinz von Ehrenfeld → Setup Wizard` öffnet den `SetupWizard.cs`-Dialog mit drei Schritten:

| Schritt | Script | Funktion |
|---------|--------|----------|
| Step 1 | `SceneFactory` + `InputActionsCreator` | Ordnerstruktur, Szenen, InputActions.asset erstellen |
| Step 2 | `PrefabFactory` | Player-Prefab + AnimatorController + alle Animations-Clips generieren |
| Step 3 | `ScenePopulator` | Alle Level-Szenen mit Player, Kamera, Ground und Platforms befüllen |
| Step 4 | `SpriteGeneratorWindow` | KI-Sprites direkt aus Unity via SpriteCook generieren & importieren |

### `SpriteGeneratorWindow.cs`

Eigenes `EditorWindow` für die direkte SpriteCook-Integration:

- Öffnen: `Tools → Prinz von Ehrenfeld → 4 - Sprites generieren (SpriteCook)`
- API Key (`sc_live_...`) wird per `EditorPrefs` gespeichert (kein Re-Enter nötig)
- Felder: Prompt, Dateiname, Speicherordner, Breite/Höhe, Pixel Art, Variationen
- Erweiterte Einstellungen: Stil, Thema, Referenz-Asset-ID (Stil-Konsistenz)
- **Quick-Presets** für alle 8 Projektcharaktere (Kev, Hooliganito, Brömmelkamp, …) – ein Klick generiert + speichert
- Kommuniziert mit `https://api.spritecook.ai/mcp/` via MCP JSON-RPC (kein separates Plugin nötig)
- Unterstützt sowohl JSON- als auch SSE-Antworten
- Speichert direkt in `Assets/Art/Sprites/Generated/` + ruft `AssetDatabase.Refresh()` auf

### `PrefabFactory.cs`

- Erstellt `Assets/Art/Animations/Player_Controller.controller` + 7 AnimationClips
- **Wichtige Reihenfolge:** `PreCreateAnimationClips()` → `AssetDatabase.SaveAssets()` → Refresh → dann Controller erstellen → Clips per `LoadAssetAtPath` verdrahten
- Erstellt Player-Prefab (immer gelöscht und neu gebaut – kein Early-Return bei bestehendem Prefab)
- `GetOrCreateSprite()` setzt immer `spriteImportMode = SpriteImportMode.Single` + Point-Filter + 32px/unit

**Animation-Clips:**

| Clip | Datei | Animiert |
|------|-------|----------|
| Idle | `Player_Idle.anim` | Scale-Bob (sanftes Atmen) |
| Run | `Player_Run.anim` | Scale-Squish/Stretch + Rotation ±5° (keine Position-Kurve!) |
| Jump | `Player_Jump.anim` | Scale-Stretch beim Absprung |
| Fall | `Player_Fall.anim` | Scale-Squish im freien Fall |
| Dash | `Player_Dash.anim` | Horizontales Stretch |
| Hurt | `Player_Hurt.anim` | Roter Farb-Flash |
| Dead | `Player_Dead.anim` | Scale → 0 |

> **Achtung:** Keine `m_LocalPosition.y`-Kurve in Run-Clip – das kämpft gegen `Rigidbody2D`-Physik und lässt den Player im Boden versinken.

### `ScenePopulator.cs`

- Prüft am Anfang `Application.isPlaying` (zeigt Dialog und bricht ab, wenn Play-Mode aktiv)
- Erstellt `Ground_Floor` (40 Units breit, Y = −0.5, `BoxCollider2D`, Layer „Ground") + drei Plattformen
- Tauscht vorhandenen Player in der Szene immer aus (löscht alten, instantiiert neues Prefab)

---

## Kamera

**Cinemachine Virtual Camera** mit:
- `CinemachineConfiner` → Level-Bounds begrenzen die Kamera
- `SmoothFollow` auf Spieler-Transform
- `CinemachineImpulseSource` für Screenshake bei Treffern

---

## Input-Architektur

Alle Inputs laufen über `InputActions.asset` (New Input System):

| Action Map | Actions |
|------------|---------|
| `Player` | Move, Jump, Dash, Interact, Pause |
| `UI` | Navigate, Submit, Cancel |
| `LevelEditor` | PlaceTile, DeleteTile, OpenPalette, Save, TestLevel |

`InputManager.cs` subscribed auf die Actions und triggert `GameEvents`.
