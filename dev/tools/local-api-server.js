const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Import and use API handlers
async function importHandler(filePath) {
  try {
    const module = require(filePath);
    return module.default || module;
  } catch (error) {
    console.error(`Error importing ${filePath}:`, error.message);
    return (req, res) => res.status(500).json({ error: `Handler not found: ${filePath}` });
  }
}

// Health check endpoint
app.get('/api/health', async (req, res) => {
  const handler = await importHandler('./api/health.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(200).json({ 
    ok: true, 
    message: "TeleMedicine API Server is running",
    timestamp: new Date().toISOString(),
    environment: 'development'
  });
});

// Profile endpoint
app.get('/api/me', async (req, res) => {
  const handler = await importHandler('./api/me.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(404).json({ error: 'Profile endpoint not implemented' });
});

// Patient authentication endpoints
app.post('/api/auth/register/patient', async (req, res) => {
  const handler = await importHandler('./api/auth/register/patient.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(404).json({ error: 'Patient registration endpoint not implemented' });
});

app.post('/api/auth/login/patient', async (req, res) => {
  const handler = await importHandler('./api/auth/login/patient.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(404).json({ error: 'Patient login endpoint not implemented' });
});

// Doctor authentication endpoints
app.post('/api/auth/register/doctor', async (req, res) => {
  const handler = await importHandler('./api/auth/register/doctor.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(404).json({ error: 'Doctor registration endpoint not implemented' });
});

app.post('/api/auth/login/doctor', async (req, res) => {
  const handler = await importHandler('./api/auth/login/doctor.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(404).json({ error: 'Doctor login endpoint not implemented' });
});

// Health worker authentication endpoints
app.post('/api/auth/register/healthworker', async (req, res) => {
  const handler = await importHandler('./api/auth/register/healthworker.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(404).json({ error: 'Health worker registration endpoint not implemented' });
});

app.post('/api/auth/login/healthworker', async (req, res) => {
  const handler = await importHandler('./api/auth/login/healthworker.ts');
  if (typeof handler === 'function') {
    return handler(req, res);
  }
  res.status(404).json({ error: 'Health worker login endpoint not implemented' });
});

// Serve static files in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, 'dist')));
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`🚀 Local API server running on http://localhost:${PORT}`);
  console.log(`📋 Available endpoints:`);
  console.log(`   GET  http://localhost:${PORT}/api/health`);
  console.log(`   GET  http://localhost:${PORT}/api/me`);
  console.log(`   POST http://localhost:${PORT}/api/auth/register/patient`);
  console.log(`   POST http://localhost:${PORT}/api/auth/login/patient`);
  console.log(`   POST http://localhost:${PORT}/api/auth/register/doctor`);
  console.log(`   POST http://localhost:${PORT}/api/auth/login/doctor`);
  console.log(`   POST http://localhost:${PORT}/api/auth/register/healthworker`);
  console.log(`   POST http://localhost:${PORT}/api/auth/login/healthworker`);
});

module.exports = app;