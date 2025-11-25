#!/usr/bin/env node
// start-combined-server.js - Start both Vite and Flask servers

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('🚀 Starting HealthBridge Combined Server...\n');

// Check if Python is available
function checkPython() {
  return new Promise((resolve) => {
    const python = spawn('python', ['--version'], { stdio: 'pipe' });
    python.on('close', (code) => {
      if (code === 0) {
        resolve('python');
      } else {
        const python3 = spawn('python3', ['--version'], { stdio: 'pipe' });
        python3.on('close', (code) => {
          resolve(code === 0 ? 'python3' : null);
        });
      }
    });
  });
}

// Start Flask server
async function startFlask() {
  const pythonCmd = await checkPython();
  
  if (!pythonCmd) {
    console.error('❌ Python not found. Please install Python and try again.');
    process.exit(1);
  }

  console.log('🐍 Starting Flask server on port 5000...');
  
  const flaskProcess = spawn(pythonCmd, ['app.py'], {
    cwd: path.join(__dirname, 'demo'),
    stdio: 'inherit',
    shell: true
  });

  flaskProcess.on('error', (error) => {
    console.error('❌ Failed to start Flask server:', error.message);
    console.log('📝 Make sure Python dependencies are installed: pip install flask pandas reportlab');
  });

  return flaskProcess;
}

// Start Vite server
function startVite() {
  console.log('⚡ Starting Vite development server...');
  
  const viteProcess = spawn('npm', ['run', 'dev'], {
    stdio: 'inherit',
    shell: true
  });

  viteProcess.on('error', (error) => {
    console.error('❌ Failed to start Vite server:', error.message);
    console.log('📝 Make sure dependencies are installed: npm install');
  });

  return viteProcess;
}

// Start both servers
async function startServers() {
  const flaskProcess = await startFlask();
  
  // Wait a bit for Flask to start
  setTimeout(() => {
    const viteProcess = startVite();
    
    // Handle graceful shutdown
    process.on('SIGINT', () => {
      console.log('\n🛑 Shutting down servers...');
      flaskProcess.kill('SIGINT');
      viteProcess.kill('SIGINT');
      process.exit(0);
    });
    
    console.log('\n✅ Both servers are starting...');
    console.log('📋 Access points:');
    console.log('   🌐 Main App: http://localhost:5173 (or next available port)');
    console.log('   🏥 Patient Dashboard: http://localhost:5173/demo');
    console.log('   🔧 Flask API: http://localhost:5000');
    console.log('\n📝 Note: Patient login will now redirect to /demo instead of external Flask server');
    
  }, 2000);
}

startServers().catch(console.error);