export default class TitleScene extends Phaser.Scene {
  constructor(){ super('Title'); }
  create(){
    const { width, height } = this.scale;
    const t = this.add.text(width/2, height/2 - 60, 'Deep Space Explorer', { fontSize:32, color:'#e5e7eb' }).setOrigin(0.5);
    const s = this.add.text(width/2, height/2, 'Press Space / A to launch', { fontSize:18, color:'#a0aec0' }).setOrigin(0.5);

    this.input.keyboard.once('keydown-SPACE', ()=> this.start());
    this.input.on('pointerdown', ()=> this.start());

    this.input.gamepad.once('down', (pad, button, index)=>{ if(index===0) this.start(); });
  }
  start(){
    this.scene.start('Play');
    this.scene.launch('HUD');
  }
}
