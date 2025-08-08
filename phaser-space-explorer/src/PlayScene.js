import SectorFactory from './SectorFactory.js';
import EncounterDirector from './EncounterDirector.js';

export default class PlayScene extends Phaser.Scene {
  constructor(){ super('Play'); }
  create(){
    // Camera post effects
    const pipes = this.game.registry.get('pipelines');
    if(window.GFX.bloom) this.cameras.main.setPostPipeline(pipes.bloom);
    if(window.GFX.vignette) this.cameras.main.setPostPipeline(pipes.vignette);

    // world
    this.player = this.physics.add.sprite(this.scale.width/2, this.scale.height*0.7, 'player');
    this.player.setDamping(true).setDrag(0.9).setMaxVelocity(200);
    this.player.setData({ hull:3, shield:false, discoveries:0 });

    // bullets / enemies
    this.bullets = this.physics.add.group();
    this.enemies = this.physics.add.group();

    // sector
    this.seed = Date.now() & 0xffff;
    this.loadSector(this.seed);

    // scanning
    this.scanRing = this.add.circle(0,0,10,0x20b2ae,0.3).setVisible(false);

    // encounter director
    this.director = new EncounterDirector(this);

    // input
    this.cursors = this.input.keyboard.createCursorKeys();
    this.keys = this.input.keyboard.addKeys('W,A,S,D,SPACE,E,SHIFT,ESC,O');
    // gamepad
    this.pad = null;
    this.input.gamepad.on('connected', pad => { this.pad = pad; });
    this.input.gamepad.on('disconnected', pad=>{ if(this.pad && pad.index===this.pad.index) this.pad=null; });

    // audio
    this.soundCtx = this.game.sound.context;
    this.master = this.soundCtx.createGain();
    this.master.connect(this.soundCtx.destination);
    this.sfx = this.soundCtx.createGain(); this.sfx.connect(this.master);

    // collisions
    this.physics.add.overlap(this.bullets, this.enemies, this.hitEnemy, null, this);
    this.physics.add.overlap(this.player, this.enemies, this.playerHit, null, this);

    this.events.emit('updateHud', { discoveries:0, hull:3, sector:this.sector.name });
  }

  loadSector(seed){
    if(this.starGroup){ this.starGroup.destroy(true); }
    const sector = SectorFactory(seed);
    this.sector = sector;
    // starfield layers using particle emitters
    this.starGroup = this.add.particles('star');
    for(let i=0;i<sector.stars.length;i++){
      this.starGroup.createEmitter({
        x: { min:0, max:this.scale.width },
        y: { min:0, max:this.scale.height },
        lifespan: 60000,
        quantity: Math.floor(80 * window.GFX.particles),
        frequency: -1,
        speedY: 20*(i+1),
        scale: 0.1 + i*0.2,
        blendMode: 'ADD'
      });
    }
    // planets
    this.planets = this.add.group();
    sector.planets.forEach(p=>{
      const planet = this.add.sprite(p.x, p.y, 'planet').setScale(p.scale).setTint(p.tint);
      const ring = this.add.sprite(p.x, p.y, 'ring').setScale(p.scale*1.2).setTint(0xffffff).setAlpha(0.4);
      ring.rotation = Math.random();
      this.planets.add(planet); this.planets.add(ring);
    });
    // nebulae
    this.nebulae = this.add.group();
    sector.nebulae.forEach(n=>{
      const nb = this.add.rectangle(n.x, n.y, 400, 300, n.color, n.alpha);
      nb.setBlendMode(Phaser.BlendModes.ADD);
      this.nebulae.add(nb);
    });
    // TODO: galaxies, belts, stations, anomalies, dark-matter fields etc.
  }

  fire(){
    const bullet = this.bullets.get(this.player.x, this.player.y-20, 'bullet');
    if(!bullet){ return; }
    bullet.setActive(true).setVisible(true);
    bullet.body.reset(this.player.x, this.player.y-20);
    bullet.setVelocity(0,-300);
    // audio ping
    const osc = this.soundCtx.createOscillator(); osc.frequency.value=440; osc.connect(this.sfx); osc.start(); osc.stop(this.soundCtx.currentTime+0.1);
  }

  scan(){
    this.scanRing.setVisible(true).setPosition(this.player.x, this.player.y).setRadius(10);
    this.tweens.add({ targets:this.scanRing, radius:200, alpha:0, duration:500, onComplete:()=>{ this.scanRing.setVisible(false).setAlpha(0.3); } });
    // simple proximity check
    let found=false;
    this.planets.children.iterate(p=>{ if(Phaser.Math.Distance.Between(this.player.x,this.player.y,p.x,p.y)<150){ found=true; }});
    if(found){
      this.player.data.values.discoveries++;
      this.events.emit('updateHud',{ discoveries:this.player.data.values.discoveries });
      // hyperspace jump every 5
      if(this.player.data.values.discoveries %5===0) this.jumpSector();
    }
    // TODO: log names/descriptions
  }

  shield(){
    if(this.player.data.values.shield) return;
    this.player.data.values.shield=true;
    const circle = this.add.circle(this.player.x,this.player.y,40,0x20b2ae,0.5);
    this.time.delayedCall(300, ()=>{ circle.destroy(); this.player.data.values.shield=false; });
  }

  playerHit(player, enemy){
    enemy.destroy();
    if(this.player.data.values.shield) return;
    this.player.data.values.hull--;
    this.events.emit('updateHud', { hull:this.player.data.values.hull });
    if(this.player.data.values.hull<=0){ this.gameOver(); }
  }

  hitEnemy(bullet, enemy){
    bullet.destroy();
    enemy.setData('hp', enemy.getData('hp')-1);
    if(enemy.getData('hp')<=0){ enemy.destroy(); this.player.data.values.discoveries++; this.events.emit('updateHud',{discoveries:this.player.data.values.discoveries}); }
  }

  jumpSector(){
    this.seed = (this.seed*16807)%2147483647;
    this.loadSector(this.seed);
    this.events.emit('updateHud',{ sector:this.sector.name });
  }

  gameOver(){
    this.scene.stop('HUD');
    this.scene.start('Title');
  }

  togglePhoto(){
    this.photo = !this.photo;
    const pipes = this.game.registry.get('pipelines');
    pipes.bloom.intensity = this.photo?1.2:0.6;
    this.events.emit('photo', this.photo);
  }

  update(time, delta){
    // input movement
    const speed = 200;
    let vx=0, vy=0;
    if(this.cursors.left.isDown || this.keys.A.isDown) vx=-speed;
    else if(this.cursors.right.isDown || this.keys.D.isDown) vx=speed;
    if(this.cursors.up.isDown || this.keys.W.isDown) vy=-speed;
    else if(this.cursors.down.isDown || this.keys.S.isDown) vy=speed;
    if(this.pad){
      vx = this.pad.axes[0].getValue()*speed;
      vy = this.pad.axes[1].getValue()*speed;
      if(this.pad.buttons[0].pressed) this.fire();
      if(Phaser.Input.Gamepad.Configs.XBOX_ONE.LB && this.pad.buttons[4].pressed) this.shield();
      if(this.pad.buttons[2].pressed) this.scan();
    }
    this.player.setVelocity(vx,vy);

    // keyboard actions
    if(Phaser.Input.Keyboard.JustDown(this.keys.SPACE)) this.fire();
    if(Phaser.Input.Keyboard.JustDown(this.keys.E)) this.scan();
    if(Phaser.Input.Keyboard.JustDown(this.keys.SHIFT)) this.shield();
    if(Phaser.Input.Keyboard.JustDown(this.keys.O)) this.togglePhoto();
    if(Phaser.Input.Keyboard.JustDown(this.keys.ESC)) this.scene.pause();

    // bullets cleanup
    this.bullets.children.iterate(b=>{ if(b.y<-50) b.destroy(); });

    // encounter director
    this.director.update(time, delta);
  }
}
