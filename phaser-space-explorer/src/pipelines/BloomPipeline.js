// Very lightweight bloom post-process. Not physical; just softens and adds glow.
export default class BloomPipeline extends Phaser.Renderer.WebGL.Pipelines.PostFXPipeline {
  constructor(game) {
    super({
      game,
      name: 'BloomPipeline',
      fragShader: `
      precision mediump float;
      uniform sampler2D uMainSampler;
      varying vec2 outTexCoord;
      uniform float intensity;
      uniform vec2 resolution;
      void main(){
        vec4 col = texture2D(uMainSampler, outTexCoord);
        vec2 off = 1.0 / resolution;
        vec4 sum = vec4(0.0);
        for(int x=-1; x<=1; x++){
          for(int y=-1; y<=1; y++){
            sum += texture2D(uMainSampler, outTexCoord + vec2(float(x),float(y))*off);
          }
        }
        gl_FragColor = col + (sum/9.0)*intensity;
      }
      `
    });
    this.intensity = 0.6;
  }
  onPreRender(){
    this.set1f('intensity', this.intensity);
    this.set2f('resolution', this.renderer.width, this.renderer.height);
  }
}
