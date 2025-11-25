# Vercel White Page Issue - Troubleshooting Guide

## Problem
After deploying to Vercel, the application shows a white/blank page instead of the expected content.

## Symptoms
- ✅ Build completes successfully 
- ✅ Deployment shows as successful
- ❌ Page loads but displays only white screen
- ❌ May or may not show console errors

## Root Causes & Solutions

### 1. **SPA Routing Configuration**

**Problem**: Vercel doesn't know how to handle client-side routes (like `/patient-landing`, `/signin`, etc.)

**Solution**: Update `vercel.json` with proper SPA routing:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*\\.(js|css|ico|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot))",
      "dest": "/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Key Points**:
- Static assets (JS/CSS) get served directly
- All other routes fallback to `index.html` for React Router
- API routes are handled separately

### 2. **Vite Configuration Issues**

**Problem**: Incorrect base path or build configuration

**Solution**: Update `vite.config.ts`:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/',  // Important: Use root path for Vercel
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom']
        }
      }
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      }
    },
  },
});
```

### 3. **Environment Detection Issues**

**Problem**: API configuration doesn't work correctly in production

**Solution**: Check `src/config/api.ts`:

```typescript
// Detect environment properly
const isDevelopment = 
  window.location.hostname === 'localhost' || 
  window.location.hostname === '127.0.0.1';

// Use relative API URLs in production
export const API_BASE_URL = isDevelopment 
  ? 'http://localhost:4000/api' 
  : '/api';
```

### 4. **React Error Boundary**

**Problem**: JavaScript errors cause white screen without visible error messages

**Solution**: Add error boundary (already implemented in `src/component/ErrorBoundary.tsx`)

### 5. **Asset Loading Issues**

**Problem**: CSS or JavaScript files fail to load

**Solution**: 
1. Check built `dist/index.html` has correct asset paths
2. Verify all assets are in `dist/assets/` folder
3. Ensure no hardcoded localhost URLs in production build

## Debugging Steps

### Step 1: Check Browser Console
1. Open deployed site in browser
2. Press F12 to open Developer Tools
3. Check **Console** tab for JavaScript errors
4. Check **Network** tab for failed requests
5. Look for red (failed) requests

### Step 2: Test API Endpoints
```bash
# Test health endpoint
curl https://your-app.vercel.app/api/health

# Expected response:
{
  "ok": true,
  "message": "TeleMedicine API Server is running"
}
```

### Step 3: Verify Build Output
```bash
npm run build
ls -la dist/  # Check files are generated
cat dist/index.html  # Check asset paths are correct
```

### Step 4: Test Locally with Production Build
```bash
npm run build
npm run preview  # Serves production build locally
```

### Step 5: Check Vercel Function Logs
1. Go to Vercel Dashboard → Your Project → Functions
2. Click on any API function
3. Check logs for errors

## Quick Fixes

### Fix 1: Redeploy with Correct Configuration
1. Update `vercel.json` as shown above
2. Commit and push changes
3. Vercel will automatically redeploy

### Fix 2: Manual Redeploy
1. Go to Vercel Dashboard → Your Project → Deployments
2. Click "Redeploy" on latest deployment
3. Select "Use existing Build Cache" = OFF

### Fix 3: Environment Variables
1. Verify all required environment variables are set
2. Special attention to `JWT_SECRET` and database variables
3. Restart deployment after adding variables

## Testing Checklist

After implementing fixes:

- [ ] Homepage (`/`) loads correctly
- [ ] API health check (`/api/health`) returns success
- [ ] Navigation between pages works
- [ ] Browser console shows no critical errors
- [ ] Registration/login forms are accessible
- [ ] Protected routes redirect to signin when not authenticated

## Common Error Messages

| Error | Cause | Solution |
|-------|--------|----------|
| `Cannot read property of undefined` | Missing environment variables | Check Vercel environment settings |
| `404 on /patient-landing` | Missing SPA routing | Update vercel.json routes |
| `Loading chunk failed` | Asset loading issues | Check base path in vite.config.ts |
| `Network Error` | API endpoint issues | Verify API functions are deployed |

## Still Having Issues?

1. **Check Vercel Status**: [status.vercel.com](https://status.vercel.com)
2. **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
3. **Compare Working Deployment**: Check if similar projects work
4. **Contact Support**: Vercel Pro/Team plans include support

---

**Last Updated**: Current deployment includes all these fixes. If you're still seeing a white page, follow the debugging steps above in order.