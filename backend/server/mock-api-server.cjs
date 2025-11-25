const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Mock database (in-memory storage for testing)
const mockUsers = [];
let userIdCounter = 1;

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ 
    ok: true, 
    message: "TeleMedicine API Server is running",
    timestamp: new Date().toISOString(),
    environment: 'development-mock'
  });
});

// Patient login endpoint
app.post('/api/auth/login/patient', (req, res) => {
  const { phone } = req.body;
  
  if (!phone) {
    return res.status(400).json({ error: 'Phone number is required' });
  }

  // Find or create mock patient
  let user = mockUsers.find(u => u.phone === phone && u.role === 'patient');
  
  if (!user) {
    // Auto-create patient for testing
    user = {
      id: userIdCounter++,
      role: 'patient',
      phone: phone,
      email: `patient${userIdCounter}@example.com`,
      name: `Patient ${userIdCounter}`
    };
    mockUsers.push(user);
  }

  // Generate mock JWT token
  const token = `mock-jwt-token-${user.id}-${Date.now()}`;

  res.status(200).json({
    success: true,
    message: 'Login successful',
    token,
    user: {
      id: user.id,
      role: user.role,
      phone: user.phone,
      email: user.email,
      name: user.name
    }
  });
});

// Doctor registration endpoint
app.post('/api/auth/register/doctor', (req, res) => {
  const { name, phone, email, password, employeeId } = req.body;
  
  if (!name || !phone || !email || !password || !employeeId) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  // Check if doctor already exists
  let user = mockUsers.find(u => 
    (u.email === email || u.phone === phone || u.employeeId === employeeId) && u.role === 'doctor'
  );
  
  if (user) {
    return res.status(400).json({ error: 'Doctor with this email, phone, or employee ID already exists' });
  }

  // Create new doctor
  user = {
    id: userIdCounter++,
    role: 'doctor',
    phone: phone,
    email: email,
    name: name,
    employeeId: employeeId,
    specialization: 'General Medicine'
  };
  mockUsers.push(user);

  // Generate mock JWT token
  const token = `mock-jwt-token-${user.id}-${Date.now()}`;

  res.status(201).json({
    ok: true,
    message: 'Registration successful',
    token,
    user: {
      id: user.id,
      role: user.role,
      phone: user.phone,
      email: user.email,
      name: user.name,
      employeeId: user.employeeId,
      specialization: user.specialization
    }
  });
});

// Health worker registration endpoint
app.post('/api/auth/register/healthworker', (req, res) => {
  const { name, village, phone, email, password, employeeId } = req.body;
  
  if (!name || !village || !phone || !email || !password || !employeeId) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  // Check if health worker already exists
  let user = mockUsers.find(u => 
    (u.email === email || u.phone === phone || u.employeeId === employeeId) && u.role === 'healthworker'
  );
  
  if (user) {
    return res.status(400).json({ error: 'Health worker with this email, phone, or employee ID already exists' });
  }

  // Create new health worker
  user = {
    id: userIdCounter++,
    role: 'healthworker',
    phone: phone,
    email: email,
    name: name,
    employeeId: employeeId,
    assignedVillage: village
  };
  mockUsers.push(user);

  // Generate mock JWT token
  const token = `mock-jwt-token-${user.id}-${Date.now()}`;

  res.status(201).json({
    ok: true,
    message: 'Registration successful',
    token,
    user: {
      id: user.id,
      role: user.role,
      phone: user.phone,
      email: user.email,
      name: user.name,
      employeeId: user.employeeId,
      assignedVillage: user.assignedVillage
    }
  });
});

// Profile endpoint
app.get('/api/me', (req, res) => {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  // Mock profile response
  res.status(200).json({
    success: true,
    profile: {
      user_id: 1,
      name: 'Test Patient',
      age: 30,
      gender: 'male',
      village: 'Test Village',
      district: 'Test District',
      medical_record_number: 'PAT001'
    },
    user: {
      id: 1,
      role: 'patient',
      phone: '+1234567890',
      email: 'test@example.com'
    }
  });
});

// Patient login endpoint
app.post('/api/auth/login/doctor', (req, res) => {
  const { identifier, password } = req.body;
  
  if (!identifier || !password) {
    return res.status(400).json({ error: 'Email/Employee ID and password are required' });
  }

  // Mock doctor login (accept any credentials for testing)
  const user = {
    id: userIdCounter++,
    role: 'doctor',
    phone: '+1234567890',
    email: identifier,
    name: 'Dr. Test Doctor'
  };

  const token = `mock-jwt-token-${user.id}-${Date.now()}`;

  res.status(200).json({
    success: true,
    message: 'Login successful',
    token,
    user
  });
});

// Health worker login endpoint
app.post('/api/auth/login/healthworker', (req, res) => {
  const { identifier, password } = req.body;
  
  if (!identifier || !password) {
    return res.status(400).json({ error: 'Email/Employee ID and password are required' });
  }

  // Mock health worker login (accept any credentials for testing)
  const user = {
    id: userIdCounter++,
    role: 'healthworker',
    phone: '+1234567890',
    email: identifier,
    name: 'Test Health Worker'
  };

  const token = `mock-jwt-token-${user.id}-${Date.now()}`;

  res.status(200).json({
    success: true,
    message: 'Login successful',
    token,
    user
  });
});

// Patient registration endpoint
app.post('/api/auth/register/patient', (req, res) => {
  const { name, phone, age, gender, village } = req.body;
  
  if (!name || !phone || !age || !gender || !village) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Check if patient already exists
  let user = mockUsers.find(u => u.phone === phone && u.role === 'patient');
  
  if (user) {
    return res.status(400).json({ error: 'Patient with this phone number already exists' });
  }

  // Create new patient
  user = {
    id: userIdCounter++,
    role: 'patient',
    phone: phone,
    email: `patient${userIdCounter}@example.com`,
    name: name,
    age: age,
    gender: gender,
    village: village,
    medicalRecordNumber: `MRN${String(userIdCounter).padStart(6, '0')}`
  };
  mockUsers.push(user);

  // Generate mock JWT token
  const token = `mock-jwt-token-${user.id}-${Date.now()}`;

  res.status(201).json({
    ok: true,
    message: 'Registration successful',
    token,
    user: {
      id: user.id,
      role: user.role,
      phone: user.phone,
      email: user.email,
      name: user.name,
      medicalRecordNumber: user.medicalRecordNumber,
      village: user.village
    }
  });
});

// Debug endpoint to view all registered users
app.get('/api/debug/users', (req, res) => {
  res.status(200).json({
    success: true,
    message: `Found ${mockUsers.length} registered users`,
    users: mockUsers,
    statistics: {
      patients: mockUsers.filter(u => u.role === 'patient').length,
      doctors: mockUsers.filter(u => u.role === 'doctor').length,
      healthworkers: mockUsers.filter(u => u.role === 'healthworker').length,
      total: mockUsers.length
    }
  });
});

// Debug endpoint to view users by role
app.get('/api/debug/users/:role', (req, res) => {
  const { role } = req.params;
  const roleUsers = mockUsers.filter(u => u.role === role);
  
  res.status(200).json({
    success: true,
    message: `Found ${roleUsers.length} ${role}s`,
    users: roleUsers
  });
});

// Debug endpoint to clear all users (for testing)
app.delete('/api/debug/users', (req, res) => {
  const count = mockUsers.length;
  mockUsers.length = 0; // Clear the array
  userIdCounter = 1; // Reset counter
  
  res.status(200).json({
    success: true,
    message: `Cleared ${count} users from mock database`
  });
});

// Default 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    error: 'Endpoint not found',
    path: req.originalUrl,
    method: req.method,
    available_endpoints: [
      'GET /api/health',
      'GET /api/me',
      'POST /api/auth/login/patient',
      'POST /api/auth/login/doctor',
      'POST /api/auth/login/healthworker',
      'POST /api/auth/register/patient',
      'POST /api/auth/register/doctor',
      'POST /api/auth/register/healthworker',
      'GET /api/debug/users',
      'GET /api/debug/users/:role',
      'DELETE /api/debug/users'
    ]
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Mock API server running on http://localhost:${PORT}`);
  console.log(`📋 Available endpoints:`);
  console.log(`   GET  http://localhost:${PORT}/api/health`);
  console.log(`   GET  http://localhost:${PORT}/api/me`);
  console.log(`   POST http://localhost:${PORT}/api/auth/login/patient`);
  console.log(`   POST http://localhost:${PORT}/api/auth/login/doctor`);
  console.log(`   POST http://localhost:${PORT}/api/auth/login/healthworker`);
  console.log(`   POST http://localhost:${PORT}/api/auth/register/patient`);
  console.log(`   POST http://localhost:${PORT}/api/auth/register/doctor`);
  console.log(`   POST http://localhost:${PORT}/api/auth/register/healthworker`);
  console.log(`\n🔍 Debug endpoints:`);
  console.log(`   GET  http://localhost:${PORT}/api/debug/users`);
  console.log(`   GET  http://localhost:${PORT}/api/debug/users/patient`);
  console.log(`   GET  http://localhost:${PORT}/api/debug/users/doctor`);
  console.log(`   GET  http://localhost:${PORT}/api/debug/users/healthworker`);
  console.log(`   DEL  http://localhost:${PORT}/api/debug/users`);
  console.log(`   POST http://localhost:${PORT}/api/auth/login/healthworker`);
  console.log(`   POST http://localhost:${PORT}/api/auth/register/patient`);
  console.log('\n✨ Ready for testing!');
});

module.exports = app;