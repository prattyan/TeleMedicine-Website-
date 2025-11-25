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
  
  const { name, age, gender, village, phone } = req.body;
  
  // Validate required fields
  if (!name || !age || !gender || !village || !phone) {
    return res.status(400).json({ error: "All fields are required" });
  }
  
  // Validate data formats
  if (age < 1 || age > 150) {
    return res.status(400).json({ error: "Age must be between 1 and 150" });
  }
  
  if (!/^[0-9]{10,15}$/.test(phone.replace(/[^\d]/g, ''))) {
    return res.status(400).json({ error: "Invalid phone number format" });
  }
  
  try {
    // Ensure database tables exist
    await ensureTablesExist();
    
    const conn = await getDbConnection();
    
    try {
      // Check if patient already exists
      const [existingUsers] = await conn.execute("SELECT id FROM users WHERE phone=? AND role='patient'", [phone]);
      
      if ((existingUsers as any[]).length > 0) {
        return res.status(400).json({ error: "Patient with this phone number already exists" });
      }
      
      // Create user account
      const [userResult] = await conn.execute(
        "INSERT INTO users (role, phone, is_verified, is_active) VALUES ('patient', ?, TRUE, TRUE)",
        [phone]
      );
      
      const userId = (userResult as any).insertId;
      
      // Generate medical record number
      const medicalRecordNumber = `MRN${userId.toString().padStart(6, '0')}`;
      
      // Create patient profile
      await conn.execute(
        "INSERT INTO patients (user_id, name, age, gender, village, medical_record_number) VALUES (?, ?, ?, ?, ?, ?)",
        [userId, name, age, gender, village, medicalRecordNumber]
      );
      
      // Generate JWT token
      const jwt = require('jsonwebtoken');
      const secret = process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-in-production';
      const token = jwt.sign(
        { id: userId, role: 'patient', phone }, 
        secret, 
        { expiresIn: '7d' }
      );
      
      res.status(201).json({
        ok: true,
        token,
        user: {
          id: userId,
          role: 'patient',
          phone,
          medical_record_number: medicalRecordNumber
        },
        message: "Patient registered successfully"
      });
      
    } finally {
      await conn.end();
    }
    
  } catch (error) {
    console.error("Registration error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
}