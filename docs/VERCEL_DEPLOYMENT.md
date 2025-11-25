# Vercel Deployment Guide

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/telemed-app)

## 📋 Prerequisites

1. **Database**: You need a MySQL database (PlanetScale, Railway, or any cloud MySQL provider)
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)

## 🔧 Environment Variables

Add these environment variables in your Vercel dashboard:

```bash
DB_HOST=your-mysql-host
DB_PORT=3306
DB_USER=your-mysql-username
DB_PASSWORD=your-mysql-password
DB_NAME=telemedicine
JWT_SECRET=your-super-secret-jwt-key-change-in-production
NODE_ENV=production
```

## 🛠 Deployment Steps

### 1. Connect Repository
- Go to [vercel.com/dashboard](https://vercel.com/dashboard)
- Click "New Project"
- Import your GitHub repository

### 2. Configure Build Settings
- Framework Preset: **Vite**
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

### 3. Add Environment Variables
- Go to Project Settings → Environment Variables
- Add all the variables listed above

### 4. Deploy
- Click "Deploy"
- Wait for deployment to complete

## 📁 Project Structure

```
├── api/                    # Vercel serverless functions
│   ├── _lib/              # Shared utilities
│   │   ├── database.ts    # Database connection
│   │   └── utils.ts       # Auth utilities
│   ├── auth/              # Authentication endpoints
│   │   ├── login/
│   │   │   └── patient.ts # Patient login
│   │   └── register/
│   │       └── patient.ts # Patient registration
│   ├── health.ts          # Health check
│   └── me.ts             # User profile
├── src/                   # Frontend React app
├── dist/                  # Build output
├── vercel.json           # Vercel configuration
└── package.json          # Dependencies
```

## 🔑 API Endpoints

- `GET /api/health` - Health check
- `POST /api/auth/register/patient` - Patient registration
- `POST /api/auth/login/patient` - Patient login
- `GET /api/me` - User profile (requires auth)

## 🐛 Common Issues

### 1. Database Connection Errors
- Verify your database credentials
- Ensure your database allows external connections
- Check if the database name exists

### 2. Build Failures
```bash
# Run locally to debug
npm run build
```

### 3. API Not Working
- Check environment variables are set correctly
- Verify API endpoints in browser dev tools

## 🔄 Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run backend server (optional)
npm run dev:server

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📊 Database Setup

The database tables will be created automatically when the API is first called. The schema includes:

- `users` - User accounts
- `patients` - Patient profiles
- `doctors` - Doctor profiles (future)
- `healthworkers` - Health worker profiles (future)

## 🔐 Security Features

- JWT token authentication
- Password hashing (for non-patient users)
- CORS protection
- Input validation
- SQL injection protection

## 🆘 Support

If you encounter issues:
1. Check the Vercel function logs
2. Verify environment variables
3. Test API endpoints manually
4. Check database connectivity

## 🎯 Production Checklist

- [ ] Database is accessible from Vercel
- [ ] All environment variables are set
- [ ] JWT secret is secure and random
- [ ] API endpoints return expected data
- [ ] Frontend can communicate with API
- [ ] Registration and login work
- [ ] Patient dashboard loads correctly