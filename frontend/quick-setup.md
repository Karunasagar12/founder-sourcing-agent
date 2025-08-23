# Quick Setup Guide

## Prerequisites Installation

### 1. Install Node.js
1. Go to [https://nodejs.org/](https://nodejs.org/)
2. Download the **LTS version** (recommended)
3. Run the installer
4. Restart your terminal/PowerShell

### 2. Verify Installation
```powershell
node --version
npm --version
```

## Frontend Setup

### 1. Install Dependencies
```powershell
cd frontend
npm install
```

### 2. Start Development Server
```powershell
npm run dev
```

### 3. Open Browser
Navigate to: `http://localhost:3000`

## Backend Setup

### 1. Install Python Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

### 2. Start Backend Server
```powershell
python main.py
```

The backend will be available at: `http://localhost:8000`

## Troubleshooting

### Node.js not found
- Make sure Node.js is installed and added to PATH
- Restart your terminal after installation
- Try running `node --version` to verify

### Port already in use
- Change the port in `vite.config.js` for frontend
- Change the port in `main.py` for backend

### API Connection Issues
- Make sure backend is running on port 8000
- Check CORS settings in backend
- Verify API endpoints are working
