// Simple seeded RNG
function mulberry32(a){
  return function(){
    a |=0; a = a + 0x6D2B79F5 |0; let t = Math.imul(a ^ a>>>15, 1 | a);
    t = t + Math.imul(t ^ t>>>7, 61 | t) ^ t; return ((t ^ t>>>14)>>>0)/4294967296;
  }
}

export default function SectorFactory(seed){
  const rand = mulberry32(seed);
  const sector = {
    name: 'Sector ' + seed,
    stars: [],
    galaxies: [],
    nebulae: [],
    planets: [],
    belts: [],
    stations: [],
    anomalies: [],
    tint: Phaser.Display.Color.IntegerToColor(0xFFFFFF).color,
    ambient: 'deep',
    encounterWeights: { scout:0.7, tank:0.2, pulsar:0.1 }
  };
  // stars - 3 layers
  for(let l=0;l<3;l++){
    const layer = [];
    for(let i=0;i<200;i++){
      layer.push({ x: rand()*2000-1000, y: rand()*2000-1000, depth: 0.2 + l*0.3 });
    }
    sector.stars.push(layer);
  }
  // planets
  const planetCount = 1 + Math.floor(rand()*2);
  for(let i=0;i<planetCount;i++){
    sector.planets.push({ x: rand()*1600-800, y: rand()*1200-600, scale: 0.5+rand(), tint: Phaser.Display.Color.RandomRGB().color });
  }
  // galaxies
  const galaxyCount = Math.floor(rand()*2);
  for(let i=0;i<galaxyCount;i++){
    sector.galaxies.push({ x: rand()*1800-900, y: rand()*1400-700, scale:0.6+rand()*0.5, rot: rand()*360 });
  }
  // nebulae
  const nebulaCount = 1 + Math.floor(rand()*2);
  for(let i=0;i<nebulaCount;i++){
    sector.nebulae.push({ x: rand()*1600-800, y: rand()*1200-600, color: Phaser.Display.Color.RandomRGB().color, alpha:0.2+rand()*0.3 });
  }
  return sector;
}
