import BloomPipeline from './pipelines/BloomPipeline.js';
import VignettePipeline from './pipelines/VignettePipeline.js';

export default class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }
  preload(){
    // Generate tiny textures procedurally to keep repo asset-free
    const g = this.add.graphics();
    // star
    g.fillStyle(0xffffff,1).fillCircle(4,4,4);
    g.generateTexture('star',8,8); g.clear();
    // player
    g.fillStyle(0x20b2ae,1).fillPolygon([0,0, 32,16, 0,32]);
    g.generateTexture('player',32,32); g.clear();
    // bullet
    g.fillStyle(0xa4b1ff,1).fillRect(0,0,4,12);
    g.generateTexture('bullet',4,12); g.clear();
    // enemy
    g.fillStyle(0xf87171,1).fillTriangle(0,0, 28,14, 0,28);
    g.generateTexture('enemy',28,28); g.clear();
    // planet
    g.fillStyle(0x7788ff,1).fillCircle(64,64,64);
    g.lineStyle(4,0xffffff,0.4).strokeCircle(64,64,68);
    g.generateTexture('planet',128,128); g.clear();
    // ring
    g.lineStyle(3,0xffffff,0.6).strokeCircle(64,64,64);
    g.generateTexture('ring',128,128); g.clear();
  }
  create(){
    // Register pipelines
    const bloom = this.renderer.pipelines.addPostPipeline('BloomPipeline', new BloomPipeline(this.game));
    const vignette = this.renderer.pipelines.addPostPipeline('VignettePipeline', new VignettePipeline(this.game));
    this.game.registry.set('pipelines', { bloom, vignette });
    this.scene.start('Title');
  }
}
