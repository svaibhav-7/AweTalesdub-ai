# Render Deployment Guide

## Prerequisites
- GitHub repository with your code
- Render account (free tier available)

## Deployment Steps

### 1. Push to GitHub
Make sure all changes are committed and pushed to your GitHub repository:
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Deploy to Render

#### Option A: Using Blueprint (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Blueprint**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and create both services:
   - `dubsmart-api` (Backend Web Service)
   - `dubsmart-frontend` (Static Site)

#### Option B: Manual Service Creation

**Backend Service:**
1. Click **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `dubsmart-api`
   - **Runtime**: Python 3
   - **Build Command**: 
     ```bash
     apt-get update && apt-get install -y ffmpeg
     pip install --upgrade pip
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     cd src && uvicorn dubsmart.api.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Starter (recommended due to large AI models)
   - **Advanced** → Add Disk: 
     - Name: `dubsmart-models`
     - Mount Path: `/root/.cache`
     - Size: 10 GB

**Frontend Service:**
1. Click **New** → **Static Site**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `dubsmart-frontend`
   - **Build Command**: 
     ```bash
     cd webapp
     npm install
     npm run build
     ```
   - **Publish Directory**: `webapp/dist`
   - **Environment Variable**:
     - Key: `VITE_API_URL`
     - Value: `https://dubsmart-api.onrender.com` (use your actual backend URL)

### 3. Configuration After Deployment

**Important:** After the backend deploys, update the frontend environment variable:
1. Go to your frontend service in Render
2. Navigate to **Environment** tab
3. Update `VITE_API_URL` to your backend URL (e.g., `https://dubsmart-api.onrender.com`)
4. Click **Save Changes** and redeploy

### 4. Testing
- Backend API: `https://dubsmart-api.onrender.com/docs`
- Frontend: `https://dubsmart-frontend.onrender.com`
- Health Check: `https://dubsmart-api.onrender.com/health`

## Important Notes

### Performance Considerations
- **Model Loading**: First request will be slow (2-5 minutes) as AI models download
- **Disk Space**: The persistent disk stores downloaded models between deployments
- **Memory**: Upgrade to Starter or higher plan for reliable performance
- **Cold Starts**: Free tier services spin down after inactivity

### Cost Optimization
- **Free Tier**: Limited to 750 hours/month, spins down after 15 minutes of inactivity
- **Starter Plan** ($7/month): Recommended for production use
- **Persistent Disk**: Additional cost (~$0.25/GB/month)

### Troubleshooting
- **Build Fails**: Check Render logs for FFmpeg installation or Python dependency errors
- **Models Not Persisting**: Ensure persistent disk is mounted at `/root/.cache`
- **CORS Errors**: Verify `VITE_API_URL` is set correctly in frontend environment
- **Slow Performance**: Upgrade from free tier to Starter plan

## Environment Variables Reference

**Backend** (optional):
- `PYTHON_VERSION`: 3.11.9
- `PYTHONUNBUFFERED`: 1

**Frontend** (required):
- `VITE_API_URL`: Your backend URL (e.g., `https://dubsmart-api.onrender.com`)

## Monitoring
- Check deployment logs in Render dashboard
- Use `/health` endpoint for uptime monitoring
- Monitor disk usage for model cache
