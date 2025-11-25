#!/usr/bin/env node
// start-fullstack-server.cjs - Start the TeleMedicine servers

const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting TeleMedicine Fullstack Server...\n');

// Start Mock API server (more reliable for development)
function startMockAPI() {
  console.log('🔧 Starting Mock API server on port 3001...');
  
  const mockProcess = spawn('node', ['mock-api-server.cjs'], {
    stdio: 'inherit',
    shell: true
  });

  mockProcess.on('error', (error) => {
    console.error('❌ Failed to start mock API server:', error.message);
    console.log('📝 Make sure mock-api-server.cjs exists');
  });

  return mockProcess;
}

// Start Vite frontend server
function startFrontend() {
  console.log('⚡ Starting Vite frontend server...');
  
  const frontendProcess = spawn('npm', ['run', 'dev'], {
    stdio: 'inherit',
    shell: true
  });

  frontendProcess.on('error', (error) => {
    console.error('❌ Failed to start frontend server:', error.message);
    console.log('📝 Make sure dependencies are installed: npm install');
  });

  return frontendProcess;
}

// Start both servers
function startServers() {
  const mockProcess = startMockAPI();
  
  // Wait a bit for mock API to start
  setTimeout(() => {
    const frontendProcess = startFrontend();
    
    // Handle graceful shutdown
    process.on('SIGINT', () => {
      console.log('\n🛑 Shutting down servers...');
      mockProcess.kill('SIGINT');
      frontendProcess.kill('SIGINT');
      process.exit(0);
    });
    
    console.log('\n✅ Both servers are starting...');
    console.log('📋 Access points:');
    console.log('   🌐 Frontend: http://localhost:5173 (or next available port)');
    console.log('   🔧 Mock API: http://localhost:3001');
    console.log('   🔐 Auth Endpoints: http://localhost:3001/api/auth/*');
    console.log('   🏥 Health Check: http://localhost:3001/api/health');
    console.log('\n💡 Using Mock API for development (no database required)');
    
  }, 2000);
}

startServers();