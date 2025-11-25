import { IncomingMessage, ServerResponse } from 'http';
import jwt from 'jsonwebtoken';

export interface ApiRequest extends IncomingMessage {
  method?: string;
  url?: string;
  headers: any;
  body?: any;
  query?: any;
  user?: any;
}

export interface ApiResponse extends ServerResponse {
  status(code: number): ApiResponse;
  json(data: any): void;
  end(data?: any): void;
}

// CORS configuration for API routes
export function setCorsHeaders(res: any) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}

// Handle CORS preflight requests
export function handleCors(req: ApiRequest, res: ApiResponse) {
  setCorsHeaders(res);
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return true;
  }
  return false;
}

// JWT utilities
export function signToken(payload: any): string {
  const secret = process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-in-production';
  return jwt.sign(payload, secret, { expiresIn: '7d' });
}

export function verifyToken(token: string): any {
  const secret = process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-in-production';
  return jwt.verify(token, secret);
}

// Authentication middleware
export function requireAuth(req: ApiRequest, res: ApiResponse, next: () => void) {
  const auth = req.headers.authorization;
  if (!auth) {
    return res.status(401).json({ error: 'no_token' });
  }
  
  const token = auth.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'invalid_token_format' });
  }
  
  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'invalid_token' });
  }
}

// Password hashing utilities
import bcrypt from 'bcrypt';

export async function hashPassword(password: string): Promise<string> {
  const saltRounds = 10;
  return await bcrypt.hash(password, saltRounds);
}

export async function comparePassword(password: string, hash: string): Promise<boolean> {
  return await bcrypt.compare(password, hash);
}

// Generate medical record number
export function generateMedicalRecordNumber(userId: number): string {
  return `MRN${userId.toString().padStart(6, '0')}`;
}