import { getDbConnection, ensureTablesExist } from '../_lib/database';

export default async function handler(req: any, res: any) {
  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  // Check authorization header
  const auth = req.headers.authorization;
  if (!auth) {
    return res.status(401).json({ error: 'no_token' });
  }
  
  const token = auth.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'invalid_token_format' });
  }
  
  try {
    // Verify JWT token
    const jwt = require('jsonwebtoken');
    const secret = process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-in-production';
    const decoded = jwt.verify(token, secret);
    
    // Ensure database tables exist
    await ensureTablesExist();
    
    const conn = await getDbConnection();
    
    try {
      // Get user data
      const [users] = await conn.execute("SELECT * FROM users WHERE id=?", [decoded.id]);
      const user = (users as any[])[0];
      
      if (!user) {
        return res.status(404).json({ error: "user_not_found" });
      }
      
      let profile = null;
      
      // Get role-specific profile data
      if (decoded.role === "patient") {
        const [patients] = await conn.execute("SELECT * FROM patients WHERE user_id=?", [decoded.id]);
        profile = (patients as any[])[0];
      } else if (decoded.role === "doctor") {
        const [doctors] = await conn.execute("SELECT * FROM doctors WHERE user_id=?", [decoded.id]);
        profile = (doctors as any[])[0];
      } else if (decoded.role === "healthworker") {
        const [healthworkers] = await conn.execute("SELECT * FROM healthworkers WHERE user_id=?", [decoded.id]);
        profile = (healthworkers as any[])[0];
      }
      
      res.status(200).json({ 
        ok: true, 
        user, 
        profile,
        timestamp: new Date().toISOString()
      });
      
    } finally {
      await conn.end();
    }
    
  } catch (error: any) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({ error: 'invalid_token' });
    }
    console.error("Profile fetch error:", error);
    res.status(500).json({ error: "database_error" });
  }
}