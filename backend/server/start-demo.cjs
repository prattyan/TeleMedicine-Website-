#!/usr/bin/env node
// start-demo.js - Utility to start the Flask demo app

const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting Flask demo app...');

// Change to demo directory and run app.py
const demoPath = path.join(__dirname, 'demo');
const pythonProcess = spawn('python', ['app.py'], {
  cwd: demoPath,
  stdio: 'inherit',
  shell: true
});

pythonProcess.on('error', (error) => {
  console.error('❌ Failed to start Flask app:', error.message);
  console.log('📝 Make sure Python is installed and available in PATH');
  console.log('📝 You can manually run: cd demo && python app.py');
});

pythonProcess.on('exit', (code) => {
  if (code === 0) {
    console.log('✅ Flask app started successfully');
  } else {
    console.error(`❌ Flask app exited with code ${code}`);
  }
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down Flask app...');
  pythonProcess.kill('SIGINT');
  process.exit(0);
});