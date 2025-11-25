const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting TeleMedicine Backend Server...');
console.log('📂 Working directory:', process.cwd());

// Start the backend server
const serverProcess = spawn('node', ['-r', 'tsx/cjs', 'src/server.ts'], {
  stdio: 'inherit',
  shell: true,
  cwd: process.cwd()
});

serverProcess.on('error', (error) => {
  console.error('❌ Failed to start backend server:', error.message);
});

serverProcess.on('close', (code) => {
  console.log(`🛑 Backend server exited with code ${code}`);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down backend server...');
  serverProcess.kill('SIGINT');
  process.exit(0);
});