export default class HUDScene extends Phaser.Scene {
  constructor(){ super({ key:'HUD', active:false }); }
  create(){
    this.discEl = document.getElementById('disc');
    this.hullEl = document.getElementById('hull');
    this.secEl = document.getElementById('sector');
    this.help = document.getElementById('help');

    // Listen to events from Play scene
    const play = this.scene.get('Play');
    play.events.on('updateHud', data => {
      if(data.discoveries!==undefined) this.discEl.textContent = data.discoveries;
      if(data.hull!==undefined) this.hullEl.textContent = data.hull;
      if(data.sector!==undefined) this.secEl.textContent = data.sector;
    });
    play.events.on('photo', on => {
      document.getElementById('hud').classList.toggle('hidden', on);
      this.help.classList.toggle('hidden', on);
    });
  }
}
