// Simple test script for API endpoints
const API_BASE = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:3000';

async function testAPI() {
  console.log('🧪 Testing API endpoints...');
  
  try {
    // Test health endpoint
    console.log('\n1. Testing health endpoint...');
    const healthResponse = await fetch(`${API_BASE}/api/health`);
    const healthData = await healthResponse.json();
    console.log('✅ Health:', healthData);
    
    // Test patient registration
    console.log('\n2. Testing patient registration...');
    const registerResponse = await fetch(`${API_BASE}/api/auth/register/patient`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Test User',
        age: 25,
        gender: 'male',
        village: 'Test Village',
        phone: '1234567890'
      })
    });
    const registerData = await registerResponse.json();
    console.log('✅ Registration:', registerData);
    
    if (registerData.token) {
      // Test profile endpoint
      console.log('\n3. Testing profile endpoint...');
      const profileResponse = await fetch(`${API_BASE}/api/me`, {
        headers: { 'Authorization': `Bearer ${registerData.token}` }
      });
      const profileData = await profileResponse.json();
      console.log('✅ Profile:', profileData);
    }
    
  } catch (error) {
    console.error('❌ API Test failed:', error);
  }
}

// Only run if this is the main module
if (typeof window === 'undefined') {
  testAPI();
}