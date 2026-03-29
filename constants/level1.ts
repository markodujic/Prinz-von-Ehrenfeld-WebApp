// Level 1 – Die Venloer Straße
// Alle statischen Daten für das erste Level

export type Platform = {
  x: number;
  y: number;
  width: number;
  height: number;
  solid?: boolean;
};

export type CollectibleDef = {
  id: string;
  x: number;
  y: number;
  type: 'koelsch' | 'sticker';
};

export type EnemyDef = {
  id: string;
  x: number;
  patrolMin: number;
  patrolMax: number;
};

// Spielfeld: 960 × 600, Boden bei y=500
// Venloer Straße: breiter Bürgersteig, Döner-Mauer, Müllcontainer, Straßenbahn-Erhöhung

export const LEVEL1_PLATFORMS: Platform[] = [
  // --- Hauptbürgersteig ---
  // Linkes Abschnitt
  { x: 0,   y: 460, width: 260,  height: 20 },
  // Lücke (Bordstein-Übergang bei 260–310)
  { x: 310, y: 460, width: 400,  height: 20 },
  // Lücke (Straßenbahn-Schiene bei 710–760)
  { x: 760, y: 460, width: 200,  height: 20 },

  // --- Erhöhungen (Döner-Theke-Mauer, Müllcontainer, etc.) ---
  // Müllcontainer-Plattform (linke Seite)
  { x: 80,  y: 380, width: 80,   height: 16 },
  // Marktstand-Tisch
  { x: 220, y: 340, width: 100,  height: 16 },
  // Straßenbahn-Gleisbett (erhöht, solide)
  { x: 340, y: 400, width: 80,   height: 20, solid: true },
  // Döner-Ladenvorsprung
  { x: 460, y: 350, width: 120,  height: 16 },
  // Graffiti-Mauer oben
  { x: 500, y: 270, width: 90,   height: 16 },
  // Fensterbank großes Haus
  { x: 640, y: 310, width: 80,   height: 14 },
  // Briefkastenreihe (solide)
  { x: 700, y: 390, width: 55,   height: 16, solid: true },
  // Gerüst-Brett rechts
  { x: 810, y: 360, width: 100,  height: 16 },
  { x: 840, y: 290, width: 80,   height: 16 },
];

// 20 Kölsch-Kronen + 3 Veedel-Sticker
export const LEVEL1_COLLECTIBLES: CollectibleDef[] = [
  // Kronen auf dem Boden (leicht erreichbar, Tutorial)
  { id: 'k01', x: 60,  y: 432, type: 'koelsch' },
  { id: 'k02', x: 110, y: 432, type: 'koelsch' },
  { id: 'k03', x: 160, y: 432, type: 'koelsch' },

  // Kronen auf dem Müllcontainer
  { id: 'k04', x: 93,  y: 352, type: 'koelsch' },
  { id: 'k05', x: 120, y: 352, type: 'koelsch' },

  // Kronen auf dem Marktstand
  { id: 'k06', x: 235, y: 312, type: 'koelsch' },
  { id: 'k07', x: 275, y: 312, type: 'koelsch' },
  { id: 'k08', x: 295, y: 432, type: 'koelsch' },

  // Kronen um das Gleisbett
  { id: 'k09', x: 345, y: 372, type: 'koelsch' },
  { id: 'k10', x: 380, y: 372, type: 'koelsch' },
  { id: 'k11', x: 415, y: 432, type: 'koelsch' },

  // Kronen am Döner-Vorsprung
  { id: 'k12', x: 470, y: 322, type: 'koelsch' },
  { id: 'k13', x: 510, y: 322, type: 'koelsch' },
  { id: 'k14', x: 550, y: 322, type: 'koelsch' },

  // Kronen auf Graffiti-Mauer
  { id: 'k15', x: 510, y: 242, type: 'koelsch' },
  { id: 'k16', x: 550, y: 242, type: 'koelsch' },

  // Kronen auf Fensterbank
  { id: 'k17', x: 650, y: 282, type: 'koelsch' },
  { id: 'k18', x: 690, y: 282, type: 'koelsch' },

  // Kronen auf Gerüst
  { id: 'k19', x: 820, y: 332, type: 'koelsch' },
  { id: 'k20', x: 875, y: 432, type: 'koelsch' },

  // 3 Veedel-Sticker (versteckt)
  { id: 's01', x: 140, y: 352, type: 'sticker' },  // auf Müllcontainer
  { id: 's02', x: 505, y: 242, type: 'sticker' },  // auf Graffiti-Mauer (nah an Krone k15)
  { id: 's03', x: 845, y: 262, type: 'sticker' },  // auf oberem Gerüst-Brett
];

// 3 Touristen patrouillieren
export const LEVEL1_ENEMIES: EnemyDef[] = [
  { id: 'e01', x: 320,  patrolMin: 310,  patrolMax: 450 },
  { id: 'e02', x: 600,  patrolMin: 530,  patrolMax: 700 },
  { id: 'e03', x: 780,  patrolMin: 760,  patrolMax: 920 },
];

export const LEVEL1_START_X = 40;
export const LEVEL1_GROUND_Y = 500;
export const LEVEL1_WIDTH = 960;

export const LEVEL1_SCORE_KOELSCH  = 10;
export const LEVEL1_SCORE_STICKER  = 50;
