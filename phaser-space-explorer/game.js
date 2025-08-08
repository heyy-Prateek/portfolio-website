// Deep Space Explorer in Phaser 3
// Exploration-first vertical space game with rare combat encounters.
// Performance knobs:
//   window.GFX = { bloom: true, vignette: true, particles: 1.0, encounterPeriod: 15000 };
// Tuning these at runtime adjusts visual quality and encounter density.
// TODO: power-ups, boss sectors, codex/galactopedia UI, save to localStorage

window.GFX = { bloom: true, vignette: true, particles: 1.0, encounterPeriod: 15000 };

import BootScene from './src/BootScene.js';
import TitleScene from './src/TitleScene.js';
import PlayScene from './src/PlayScene.js';
import HUDScene from './src/HUDScene.js';

const config = {
  type: Phaser.WEBGL,
  width: window.innerWidth,
  height: window.innerHeight,
  parent: document.body,
  scene: [BootScene, TitleScene, PlayScene, HUDScene],
  physics: { default: 'arcade', arcade: { gravity: { y: 0 }, debug: false } },
  audio: { disableWebAudio: false }
};

const game = new Phaser.Game(config);

window.addEventListener('resize', () => {
  game.scale.resize(window.innerWidth, window.innerHeight);
});

// Expose for console tweaking
window.__game = game;
