const fs = require('fs');
const path = require('path');
const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

const { JSDOM } = require('jsdom');

describe('initParticlesBackground', () => {
  test('adds a particles canvas to the document body', () => {
    const html = '<!doctype html><html><body></body></html>';
    const dom = new JSDOM(html, { runScripts: 'dangerously' });
    dom.window.requestAnimationFrame = () => {};
    dom.window.HTMLCanvasElement.prototype.getContext = () => ({
      clearRect: jest.fn(),
      beginPath: jest.fn(),
      arc: jest.fn(),
      fill: jest.fn(),
      stroke: jest.fn(),
      moveTo: jest.fn(),
      lineTo: jest.fn()
    });
    const scriptContent = fs.readFileSync(path.resolve(__dirname, '../script.js'), 'utf8');

    // Execute the script inside the JSDOM window so functions are attached to it
    dom.window.eval(scriptContent);

    // Call the function to initialize the particles background
    dom.window.initParticlesBackground();

    const canvas = dom.window.document.getElementById('particles-canvas');
    expect(canvas).not.toBeNull();
  });
});
