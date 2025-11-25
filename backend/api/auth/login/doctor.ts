import { getDbConnection } from '../../_lib/database';
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
    const { identifier, password, employeeId, role } = req.body;

    if (!identifier || !password) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const db = await getDbConnection();
    
    // Find user by email or employee_id
    const userQuery = `
      SELECT u.*, p.* FROM users u 
      LEFT JOIN doctor_profiles p ON u.id = p.user_id 
      WHERE (u.email = ? OR u.employee_id = ?) AND u.role IN ('doctor', 'healthworker')
    `;
    
    const [users] = await db.execute(userQuery, [identifier, employeeId || identifier]);
    
    if (!Array.isArray(users) || users.length === 0) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const user = users[0] as any;

    // Verify password
    const passwordMatch = await bcrypt.compare(password, user.password_hash);
    if (!passwordMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Check role if specified
    if (role && user.role !== role) {
      return res.status(401).json({ error: 'Invalid role' });
    }

    // Generate JWT token
    const token = jwt.sign(
      { 
        userId: user.id, 
        role: user.role,
        email: user.email 
      },
      process.env.JWT_SECRET || 'fallback-secret-key',
      { expiresIn: '7d' }
    );

    await db.end();

    return res.status(200).json({
      success: true,
      message: 'Login successful',
      token,
      user: {
        id: user.id,
        role: user.role,
        phone: user.phone,
        email: user.email,
        name: user.name || `${user.role} User`
      }
    });

  } catch (error) {
    console.error('Doctor login error:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}