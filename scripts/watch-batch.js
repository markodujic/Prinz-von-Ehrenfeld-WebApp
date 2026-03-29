const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const manifest = path.resolve(__dirname, '..', 'docs', 'sprite-manifest.json');
let timeout = null;
let running = false;

function runBatch() {
  if (running) return;
  running = true;
  console.log(new Date().toISOString(), 'Starting batch generation...');

  const isWin = process.platform === 'win32';
  const cmd = isWin ? 'npm' : 'npm';
  const args = isWin ? ['run', 'sprite:generate:batch:ps'] : ['run', 'sprite:generate:batch'];

  const p = spawn(cmd, args, { stdio: 'inherit', shell: true });
  p.on('close', (code) => {
    console.log(new Date().toISOString(), `Batch finished, exit ${code}`);
    running = false;
  });
}

if (!fs.existsSync(manifest)) {
  console.error('Manifest file not found:', manifest);
  process.exit(1);
}

console.log('Watching manifest for changes:', manifest);
fs.watch(manifest, { persistent: true }, (eventType, filename) => {
  if (timeout) clearTimeout(timeout);
  // debounce multiple events
  timeout = setTimeout(() => {
    console.log(new Date().toISOString(), 'Change detected:', eventType, filename);
    runBatch();
  }, 300);
});
