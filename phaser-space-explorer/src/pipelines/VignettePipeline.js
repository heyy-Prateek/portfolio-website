export default class VignettePipeline extends Phaser.Renderer.WebGL.Pipelines.PostFXPipeline {
  constructor(game){
    super({
      game,
      name: 'VignettePipeline',
      fragShader: `
      precision mediump float;
      uniform sampler2D uMainSampler;
      varying vec2 outTexCoord;
      uniform float strength;
      void main(){
        vec4 color = texture2D(uMainSampler, outTexCoord);
        float dist = distance(outTexCoord, vec2(0.5));
        float vig = smoothstep(0.8, 0.2, dist);
        color.rgb *= mix(1.0, vig, strength);
        gl_FragColor = color;
      }
      `
    });
    this.strength = 0.5;
  }
  onPreRender(){
    this.set1f('strength', this.strength);
  }
}
