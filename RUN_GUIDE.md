# Shopzy - Application Startup Guide

## Quick Start - One Command

### On Linux/macOS:

```bash
cd /path/to/shopzy
chmod +x run.sh
./run.sh
```

### On Windows:

```cmd
cd C:\path\to\shopzy
run.bat
```

## What the Script Does

The startup script automatically:

1. ✅ Checks for Python 3, Node.js, and npm
2. ✅ Creates virtual environments for each service (if needed)
3. ✅ Installs dependencies for all services (if needed)
4. ✅ Installs npm packages for frontend (if needed)
5. ✅ Starts all 7 backend services in parallel:
   - Product Service (Port 8001)
   - Customer Service (Port 8002)
   - Inventory Service (Port 8003)
   - Order Service (Port 8004)
   - Payment Service (Port 8005)
   - Notification Service (Port 8006)
   - API Gateway (Port 8000)
6. ✅ Starts the React frontend (Port 5173)
7. ✅ Displays all access URLs

## Access Points After Running

**Frontend:**
- http://localhost:5173

**API Documentation (Swagger):**
- http://localhost:8000/docs (API Gateway)
- http://localhost:8001/docs (Product Service)
- http://localhost:8002/docs (Customer Service)
- http://localhost:8003/docs (Inventory Service)
- http://localhost:8004/docs (Order Service)
- http://localhost:8005/docs (Payment Service)
- http://localhost:8006/docs (Notification Service)

## Stopping All Services

### Linux/macOS:
Press `Ctrl+C` in the terminal where you ran `./run.sh`

### Windows:
Close all the command windows that were opened by `run.bat`

Or manually close each service window.

## Troubleshooting

### Script won't run on macOS/Linux
```bash
# Make sure it's executable
chmod +x run.sh
```

### Port already in use
```bash
# Find what's using a port (e.g., 8001)
lsof -i :8001

# Kill the process
kill -9 <PID>
```

### Virtual environment issues
```bash
# Delete and recreate
rm -rf services/*/venv
./run.sh  # Will create new virtual environments
```

### NPM issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rm -rf frontend/node_modules

# Reinstall
cd frontend && npm install
```

## Manual Alternative

If the script doesn't work, you can still run services manually as described in `Development.md`

```bash
# Terminal 1 - Product Service
cd services/product-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8001 --reload

# Terminal 2 - Customer Service
cd services/customer-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8002 --reload

# ... repeat for other services

# Terminal 8 - Frontend
cd frontend
npm install
npm run dev
```

See `Development.md` for complete manual setup instructions.

## Tips

- The script creates `.marker` files to track installed dependencies
- Remove these files to force reinstallation: `rm services/**/installed.marker`
- Service logs are available in `/tmp/*.log` on Linux/macOS
- For more detailed setup options, see `Development.md`
