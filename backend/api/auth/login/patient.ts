import { getDbConnection, ensureTablesExist } from '../../_lib/database';

export default async function handler(req: any, res: any) {
  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  const { phone } = req.body;
  
  if (!phone) {
    return res.status(400).json({ error: "Phone number is required" });
  }
  
  try {
    // Ensure database tables exist
    await ensureTablesExist();
    
    const conn = await getDbConnection();
    
    try {
      // Find user by phone number
      const [users] = await conn.execute(
        "SELECT * FROM users WHERE phone=? AND role='patient' AND is_active=TRUE",
        [phone]
      );
      
      const user = (users as any[])[0];
      
      if (!user) {
        return res.status(401).json({ error: "Invalid phone number or user not found" });
      }
      
      // Generate JWT token
      const jwt = require('jsonwebtoken');
      const secret = process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-in-production';
      const token = jwt.sign(
        { id: user.id, role: 'patient', phone: user.phone }, 
        secret, 
        { expiresIn: '7d' }
      );
      
      res.status(200).json({
        ok: true,
        token,
        user: {
          id: user.id,
          role: user.role,
          phone: user.phone
        },
        message: "Login successful"
      });
      
    } finally {
      await conn.end();
    }
    
  } catch (error) {
    console.error("Login error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
}