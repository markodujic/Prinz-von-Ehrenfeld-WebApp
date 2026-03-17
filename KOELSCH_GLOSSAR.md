# Kölsch-Glossar – Prinz von Ehrenfeld

Alle UI-Texte, Dialoge und In-Game-Nachrichten sind auf **Kölsch**.  
Strings niemals hardcoden – immer über `UIText`-Konstanten oder `LocalizationKey`-Enum referenzieren.

---

## UI-Texte (Hauptnavigation)

| Kölsch | Deutsch | Code-Schlüssel | Anmerkung |
|--------|---------|----------------|-----------|
| Fang an! | Start / Spielen | `UIText.StartButton` | Haupt-CTA im Menü |
| Widder vun vorne | Neu starten / Retry | `UIText.Retry` | Nach Game Over |
| Päus | Pause | `UIText.Pause` | Pause-Button im HUD |
| Weider | Weiter / Continue | `UIText.Continue` | Pause → Weiterspielen |
| Optione | Einstellungen | `UIText.Options` | Settings-Menü |
| Noh naus | Beenden / Quit | `UIText.Quit` | Spiel beenden |
| Zerick | Zurück | `UIText.Back` | Navigation zurück |

---

## Spielzustand

| Kölsch | Deutsch | Code-Schlüssel | Anmerkung |
|--------|---------|----------------|-----------|
| Tschüss Jott! | Game Over | `UIText.GameOver` | Game-Over-Screen |
| Joot jemaat! | Level geschafft | `UIText.LevelComplete` | Level-Complete-Screen |
| Dat nächste Ding | Nächstes Level | `UIText.NextLevel` | Button nach Level-Complete |
| Checkpoint! | Checkpoint erreicht | `UIText.Checkpoint` | Kurzes Popup |
| Widder vun vorne | Neustart | `UIText.Retry` | Game-Over-Button |

---

## HUD

| Kölsch | Deutsch | Code-Schlüssel | Anmerkung |
|--------|---------|----------------|-----------|
| Kriesche | Punkte / Score | `UIText.Score` | HUD oben links |
| Et Levve | Leben / Lives | `UIText.Lives` | HUD: Lebens-Anzeige |
| Zick | Zeit / Timer | `UIText.Timer` | Countdown im HUD |
| Kölsch-Krone | Collectible-Zähler | `UIText.Collectibles` | Sammelgegenstand |

---

## Highscore

| Kölsch | Deutsch | Code-Schlüssel | Anmerkung |
|--------|---------|----------------|-----------|
| Noh hück! | Highscore | `UIText.Highscore` | Highscore-Screen-Titel |
| Dä Beste | Platz 1 | `UIText.Rank1` | Erste Zeile |
| Dinge Name | Dein Name | `UIText.EnterName` | Namenseingabe |
| Eintrage | Eintragen | `UIText.SaveScore` | Score speichern |

---

## Charakter-Auswahl

| Kölsch | Deutsch | Code-Schlüssel | Anmerkung |
|--------|---------|----------------|-----------|
| Wä willste sin? | Wer willst du sein? | `UIText.CharSelect` | Screen-Titel |
| Klaar! | Auswählen / Confirm | `UIText.SelectChar` | Charakter bestätigen |
| Noch nit frei | Noch gesperrt | `UIText.Locked` | Gesperrter Charakter |
| Schnäll | Schnell | `UIText.StatSpeed` | Charakter-Stat |
| Stark | Stark | `UIText.StatStrength` | Charakter-Stat |
| Hält lang | Ausdauer | `UIText.StatStamina` | Charakter-Stat |

---

## Level-Editor

| Kölsch | Deutsch | Code-Schlüssel | Anmerkung |
|--------|---------|----------------|-----------|
| Bau dinge Veedel! | Baue deinen Level! | `UIText.EditorTitle` | Editor-Screen-Titel |
| Legge Steng | Tile platzieren | `UIText.PlaceTile` | Tooltip |
| Wegmache | Löschen | `UIText.DeleteTile` | Tooltip |
| Speichere | Speichern | `UIText.Save` | Toolbar-Button |
| Lore | Laden | `UIText.Load` | Toolbar-Button |
| Loslegge! | Testen / Spielen | `UIText.TestLevel` | Level ausprobieren |
| Jespeichert! | Gespeichert! | `UIText.Saved` | Bestätigungs-Toast |
| Fehler beim Speichere | Fehler beim Speichern | `UIText.SaveError` | Fehlermeldung |

---

## Power-Ups (In-Game Benachrichtigungen)

| Kölsch | Deutsch | Code-Schlüssel | Anmerkung |
|--------|---------|----------------|-----------|
| Schnäll Kölsch! | Speed-Boost! | `UIText.PowerUpSpeed` | Power-Up-Toast |
| Et Schilldche! | Schild aktiviert! | `UIText.PowerUpShield` | Power-Up-Toast |
| Unkaputtbar! | Unverwundbar! | `UIText.PowerUpInvincible` | Power-Up-Toast |
| Noch ens Levve! | Extra Leben! | `UIText.PowerUpLife` | Power-Up-Toast |
| Superjummp! | Mega-Sprung! | `UIText.PowerUpJump` | Power-Up-Toast |

---

## Dialog / Spieler-Reaktionen (SFX-Texte)

| Kölsch | Deutsch | Kontext |
|--------|---------|---------|
| Joot so! | So ist es gut! | Treffer auf Gegner gelandet |
| Alaaf! | Köln-Ausruf | Level geschafft |
| Dat war nix! | Das war nichts! | Treffer bekommen |
| Hä?! | Hä?! | Überraschungs-Reaktion |
| Nä, nä, nä! | Nein, nein, nein! | Fast game over |
| Schön Kölsch! | Schönes Kölsch! | Goldkrone gefunden |
| Ich bin dä Prinz! | Ich bin der Prinz! | Finale / Sieg |
| Mer loofe! | Wir laufen! | Dash aktiviert |
| Ow! | Au! | Schaden bekommen |
| Hüpp! | Hüpf! | Jump-SFX-Text |

---

## Fehlermeldungen & System-Texte

| Kölsch | Deutsch | Code-Schlüssel |
|--------|---------|----------------|
| Dat hätt nit jeklappt | Das hat nicht funktioniert | `UIText.ErrorGeneric` |
| Kein Spaicher donn | Kein Speicherplatz | `UIText.ErrorNoSpace` |
| Lore fehlgeschlare | Laden fehlgeschlagen | `UIText.ErrorLoad` |
| Neue Spielstand? | Neues Spiel starten? | `UIText.NewGameConfirm` |
| Alles losche? | Alles löschen? | `UIText.DeleteConfirm` |
| Jo, maach! | Ja, mach! | `UIText.Confirm` |
| Nä, lass dat! | Nein, lass das! | `UIText.Cancel` |

---

## Kölsch-Zahlen & Ordnungszahlen (für Level-Benennung)

| Kölsch | Deutsch |
|--------|---------|
| Eß | Eins |
| Zwei | Zwei |
| Dreij | Drei |
| Veier | Vier |
| Fönnef | Fünf |
| Sächs | Sechs |
| Sävve | Sieben |
| Ach | Acht |
| Nüün | Neun |
| Zähn | Zehn |

---

## Quellen & Referenzen

- [Kölsches Wörterbuch – koesch.de](https://www.koesch.de)
- [Kölsch-Deutsch Wörterbuch – koeln.de](https://www.koeln.de)
- Muttersprachler-Reviews empfohlen vor finalem Release 🙏
