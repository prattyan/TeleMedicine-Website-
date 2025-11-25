#!/usr/bin/env node
// Quick test script to verify registration endpoints

const fetch = require('node-fetch').default || require('node-fetch');

async function testRegistration() {
  console.log('🧪 Testing registration endpoints...\n');
  
  const API_BASE = 'http://localhost:3001/api';
  
  // Test patient registration
  console.log('1. Testing Patient Registration...');
  try {
    const response = await fetch(`${API_BASE}/auth/register/patient`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Test Patient',
        age: 25,
        gender: 'male',
        village: 'Nabha',
        phone: '+919876543210'
      })
    });
    
    const data = await response.json();
    console.log('✅ Patient registration:', response.status, data);
  } catch (error) {
    console.log('❌ Patient registration failed:', error.message);
  }
  
  // Test doctor registration
  console.log('\n2. Testing Doctor Registration...');
  try {
    const response = await fetch(`${API_BASE}/auth/register/doctor`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Dr. Test',
        phone: '+919876543211',
        email: 'doctor@test.com',
        password: 'password123',
        employeeId: 'DOC001'
      })
    });
    
    const data = await response.json();
    console.log('✅ Doctor registration:', response.status, data);
  } catch (error) {
    console.log('❌ Doctor registration failed:', error.message);
  }
  
  // Test health worker registration
  console.log('\n3. Testing Health Worker Registration...');
  try {
    const response = await fetch(`${API_BASE}/auth/register/healthworker`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Test Health Worker',
        village: 'Nabha',
        phone: '+919876543212',
        email: 'healthworker@test.com',
        password: 'password123',
        employeeId: 'HW001'
      })
    });
    
    const data = await response.json();
    console.log('✅ Health worker registration:', response.status, data);
  } catch (error) {
    console.log('❌ Health worker registration failed:', error.message);
  }
}

// Only run if called directly
if (require.main === module) {
  testRegistration();
}

module.exports = { testRegistration };