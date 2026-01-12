# 🚀 GitHub Setup & Deployment Guide

## Quick Setup Commands

### 1. Initialize Git Repository
```bash
cd honda_vehicle_api
git init
git add .
git commit -m "🚀 Initial commit: Honda Vehicle Models API"
```

### 2. Push to GitHub
```bash
git branch -M main
git remote add origin https://github.com/vikram05/Honda_model_app.git
git push -u origin main
```

### 3. Setup & Run Locally
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Start the API server
uvicorn app.main:app --reload
```

## 🌐 Access Points
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 🧪 Test the API
```bash
python test_api.py
```

**Ready for GitHub!** 🎉