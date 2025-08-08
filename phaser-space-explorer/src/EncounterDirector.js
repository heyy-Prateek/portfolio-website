// Manages spawning small enemy formations on a timer
export default class EncounterDirector {
  constructor(scene){
    this.scene = scene;
    this.timer = 0;
  }
  update(time, delta){
    this.timer += delta;
    const period = window.GFX.encounterPeriod || 15000;
    if(this.timer > period){
      this.timer = 0;
      this.spawn();
    }
  }
  spawn(){
    const width = this.scene.scale.width;
    const type = Phaser.Math.RND.weightedPick(['scout','tank','pulsar']);
    const group = this.scene.add.group();
    for(let i=0;i<3;i++){
      const enemy = this.scene.physics.add.sprite(width/2 + (i-1)*40, -50, 'enemy');
      enemy.setData('type', type);
      enemy.setVelocity(0, 40 + i*10);
      enemy.setData('hp', type==='tank'?4:2);
      group.add(enemy);
    }
    this.scene.enemies.addMultiple(group.getChildren());
  }
}
