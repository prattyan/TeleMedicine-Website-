import { getDbConnection, ensureTablesExist } from '../../_lib/database';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

export default async function handler(req: any, res: any) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, password, employeeId, phone, specialization, role } = req.body;

    // Validate required fields
    if (!name || !email || !password || !employeeId) {
      return res.status(400).json({ error: 'Missing required fields: name, email, password, employeeId' });
    }

    // Ensure database tables exist
    await ensureTablesExist();
    
    const db = await getDbConnection();
    
    // Check if user already exists
    const [existingUsers] = await db.execute(
      'SELECT id FROM users WHERE email = ? OR employee_id = ?',
      [email, employeeId]
    );
    
    if (Array.isArray(existingUsers) && existingUsers.length > 0) {
      await db.end();
      return res.status(409).json({ error: 'User with this email or employee ID already exists' });
    }

    // Hash password
    const saltRounds = 10;
    const password_hash = await bcrypt.hash(password, saltRounds);

    // Insert user
    const [userResult] = await db.execute(
      `INSERT INTO users (role, phone, email, password_hash, employee_id) 
       VALUES (?, ?, ?, ?, ?)`,
      [role || 'doctor', phone || null, email, password_hash, employeeId]
    ) as any;

    const userId = userResult.insertId;

    // Create doctor profile
    await db.execute(
      `INSERT INTO doctor_profiles (user_id, name, specialization, employee_id) 
       VALUES (?, ?, ?, ?) 
       ON DUPLICATE KEY UPDATE name = VALUES(name), specialization = VALUES(specialization)`,
      [userId, name, specialization || 'General Practice', employeeId]
    );

    // Generate JWT token
    const token = jwt.sign(
      { 
        userId: userId, 
        role: role || 'doctor',
        email: email 
      },
      process.env.JWT_SECRET || 'fallback-secret-key',
      { expiresIn: '7d' }
    );

    await db.end();

    return res.status(201).json({
      success: true,
      message: 'Doctor registered successfully',
      token,
      user: {
        id: userId,
        role: role || 'doctor',
        phone: phone || null,
        email: email,
        name: name
      }
    });

  } catch (error) {
    console.error('Doctor registration error:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}