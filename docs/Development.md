# Shopzy Development Guide

This document provides comprehensive instructions for running the Shopzy microservices e-commerce platform both as a complete application and individual services.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start - Docker Compose (Complete Application)](#quick-start---docker-compose-complete-application)
3. [Running Individual Services](#running-individual-services)
4. [Frontend Development](#frontend-development)
5. [Testing](#testing)
6. [Development Workflow](#development-workflow)
7. [Debugging & Troubleshooting](#debugging--troubleshooting)

---

## Prerequisites

### For Docker Compose (Recommended for Complete Application)

- Docker 20.10+
- Docker Compose 2.0+
- 8GB+ RAM available
- Ports 5173, 8000-8006, 5432 available

Verify installation:
```bash
docker --version
docker-compose --version
```

### For Local Development (Individual Services)

- Python 3.11+
- Node.js 18+
- npm or yarn
- PostgreSQL 15 (optional, or use Docker)
- Git

Verify installation:
```bash
python --version
node --version
npm --version
```

---

## Quick Start - Docker Compose (Complete Application)

### Method 1: One Command (Recommended)

Start all 8 services with a single command:

```bash
docker-compose up --build
```

This will:
- ✅ Create PostgreSQL database with auto-initialization
- ✅ Build all service Docker images
- ✅ Start all 7 microservices
- ✅ Start React frontend
- ✅ Initialize all databases

### Access Services

After all containers start successfully:

**Frontend:**
```
http://localhost:5173
```

**API Documentation (Swagger):**
```
http://localhost:8000/docs           (API Gateway)
http://localhost:8001/docs           (Product Service)
http://localhost:8002/docs           (Customer Service)
http://localhost:8003/docs           (Inventory Service)
http://localhost:8004/docs           (Order Service)
http://localhost:8005/docs           (Payment Service)
http://localhost:8006/docs           (Notification Service)
```

**Database:**
```
Host: localhost:5432
User: shopzy
Password: shopzy123
```

### Common Docker Commands

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f product-service

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart product-service

# Check status
docker-compose ps
```

---

## Running Individual Services

### Prerequisites for Local Development

Before running individual services, install the base dependencies:

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or use individual venvs for each service
cd services/product-service
python -m venv venv
source venv/bin/activate
```

### Database Setup (One Time)

For local development without Docker:

```bash
# Install PostgreSQL (if not already installed)
# macOS:
brew install postgresql@15

# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# Create databases
createdb -U postgres product_db
createdb -U postgres customer_db
createdb -U postgres inventory_db
createdb -U postgres order_db
createdb -U postgres payment_db
createdb -U postgres notification_db
```

Or use Docker for just PostgreSQL:

```bash
docker run -d \
  --name shopzy-postgres \
  -e POSTGRES_USER=shopzy \
  -e POSTGRES_PASSWORD=shopzy123 \
  -p 5432:5432 \
  postgres:15-alpine
```

### Product Service

**Purpose:** Manages product catalog, search, and filtering

**Port:** 8001

**Setup & Run:**

```bash
cd services/product-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/product_db"
export SERVICE_PORT=8001

# Run service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Access:**
- API Documentation: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

---

### Customer Service

**Purpose:** Manages customer profiles, addresses, and personal information

**Port:** 8002

**Setup & Run:**

```bash
cd services/customer-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/customer_db"
export SERVICE_PORT=8002

python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

**Access:**
- API Documentation: http://localhost:8002/docs
- Health Check: http://localhost:8002/health

---

### Inventory Service

**Purpose:** Manages stock levels, availability checks, and reservations

**Port:** 8003

**Setup & Run:**

```bash
cd services/inventory-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/inventory_db"
export SERVICE_PORT=8003

python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

**Access:**
- API Documentation: http://localhost:8003/docs
- Health Check: http://localhost:8003/health

---

### Order Service

**Purpose:** Handles order creation, tracking, and management

**Port:** 8004

**Setup & Run:**

```bash
cd services/order-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/order_db"
export SERVICE_PORT=8004

python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

**Access:**
- API Documentation: http://localhost:8004/docs
- Health Check: http://localhost:8004/health

---

### Payment Service

**Purpose:** Processes payments, refunds, and payment transactions

**Port:** 8005

**Setup & Run:**

```bash
cd services/payment-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/payment_db"
export SERVICE_PORT=8005

python -m uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

**Access:**
- API Documentation: http://localhost:8005/docs
- Health Check: http://localhost:8005/health

---

### Notification Service

**Purpose:** Sends notifications and manages notification preferences

**Port:** 8006

**Setup & Run:**

```bash
cd services/notification-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/notification_db"
export SERVICE_PORT=8006

python -m uvicorn app.main:app --host 0.0.0.0 --port 8006 --reload
```

**Access:**
- API Documentation: http://localhost:8006/docs
- Health Check: http://localhost:8006/health

---

### API Gateway

**Purpose:** Routes requests to appropriate services and provides unified API endpoint

**Port:** 8000

**Setup & Run:**

```bash
cd services/api-gateway

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export SERVICE_PORT=8000

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access:**
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

### Running All Services Locally (Without Docker)

Open 8 separate terminal windows/tabs and run each service:

**Terminal 1 - Product Service:**
```bash
cd services/product-service
source venv/bin/activate
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/product_db"
python -m uvicorn app.main:app --port 8001 --reload
```

**Terminal 2 - Customer Service:**
```bash
cd services/customer-service
source venv/bin/activate
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/customer_db"
python -m uvicorn app.main:app --port 8002 --reload
```

**Terminal 3 - Inventory Service:**
```bash
cd services/inventory-service
source venv/bin/activate
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/inventory_db"
python -m uvicorn app.main:app --port 8003 --reload
```

**Terminal 4 - Order Service:**
```bash
cd services/order-service
source venv/bin/activate
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/order_db"
python -m uvicorn app.main:app --port 8004 --reload
```

**Terminal 5 - Payment Service:**
```bash
cd services/payment-service
source venv/bin/activate
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/payment_db"
python -m uvicorn app.main:app --port 8005 --reload
```

**Terminal 6 - Notification Service:**
```bash
cd services/notification-service
source venv/bin/activate
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/notification_db"
python -m uvicorn app.main:app --port 8006 --reload
```

**Terminal 7 - API Gateway:**
```bash
cd services/api-gateway
source venv/bin/activate
python -m uvicorn app.main:app --port 8000 --reload
```

**Terminal 8 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm run dev
```

---

## Frontend Development

### Initial Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template (if exists)
cp .env.example .env.local

# Edit .env.local
# VITE_API_URL=http://localhost:8000
```

### Development Server

```bash
# Start development server with hot reload
npm run dev

# Frontend will be available at http://localhost:5173
```

### Building for Production

```bash
# Build optimized production bundle
npm run build

# Output is in frontend/dist/

# Preview production build locally
npm run preview
```

### Frontend Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Products.tsx
│   │   ├── ProductDetail.tsx
│   │   ├── Cart.tsx
│   │   ├── Checkout.tsx
│   │   ├── OrderConfirmation.tsx
│   │   ├── MyOrders.tsx
│   │   └── OrderDetail.tsx
│   ├── components/
│   │   └── Layout.tsx
│   ├── App.tsx
│   ├── api.ts
│   ├── store.ts
│   └── main.tsx
├── package.json
└── vite.config.ts
```

---

## Testing

### Running Tests for Individual Services

Each service includes comprehensive test suites using pytest and SQLite in-memory databases.

#### Product Service Tests (33 tests)

```bash
cd services/product-service

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_api.py::TestProductAPI::test_create_product -v
```

#### Customer Service Tests (7 tests)

```bash
cd services/customer-service

pytest tests/ -v
pytest tests/test_api.py -v
```

#### Inventory Service Tests (7 tests)

```bash
cd services/inventory-service

pytest tests/ -v
pytest tests/test_api.py -v
```

#### Order Service Tests (9 tests)

```bash
cd services/order-service

pytest tests/ -v
pytest tests/test_api.py -v
```

#### Payment Service Tests (7 tests)

```bash
cd services/payment-service

pytest tests/ -v
pytest tests/test_api.py -v
```

#### Notification Service Tests (8 tests)

```bash
cd services/notification-service

pytest tests/ -v
pytest tests/test_api.py -v
```

#### API Gateway Tests (10 tests)

```bash
cd services/api-gateway

pytest tests/ -v
pytest tests/test_api.py -v
```

### Running Tests in Docker

```bash
# Run tests for a specific service
docker exec shopzy-product-service pytest tests/ -v

# Run all tests with coverage
docker exec shopzy-product-service pytest tests/ --cov=app

# Run specific test
docker exec shopzy-product-service pytest tests/test_api.py::TestProductAPI::test_create_product -v
```

### Test Database

Tests use SQLite in-memory databases for isolation and speed:

```python
# conftest.py automatically creates and destroys test databases
# No external database needed for testing
# Each test runs in isolation with a fresh database
```

---

## Development Workflow

### Adding a New Feature

#### Backend Feature

1. **Create/Update Model**
   ```python
   # services/[service]/app/models/[model].py
   class NewModel(Base):
       __tablename__ = "new_models"
       id = Column(UUID, primary_key=True, default=uuid4)
       # Add fields...
   ```

2. **Create Schema**
   ```python
   # services/[service]/app/schemas/[model].py
   class NewModelCreate(BaseModel):
       # Define input fields
       pass
   ```

3. **Implement Repository**
   ```python
   # services/[service]/app/repositories/[model]_repository.py
   class NewModelRepository:
       def create(self, db: Session, data: NewModelCreate):
           # Implement CRUD
           pass
   ```

4. **Add Service Logic**
   ```python
   # services/[service]/app/services/[model]_service.py
   class NewModelService:
       def __init__(self, repository: NewModelRepository):
           self.repository = repository
       
       def create(self, data: NewModelCreate):
           # Business logic
           pass
   ```

5. **Add API Routes**
   ```python
   # services/[service]/app/api/routes.py
   @router.post("/new-models")
   async def create_new_model(data: NewModelCreate, db: Session = Depends(get_db)):
       service = NewModelService(repository)
       return await service.create(data)
   ```

6. **Write Tests**
   ```python
   # services/[service]/tests/test_api.py
   def test_create_new_model(self, client, data):
       response = client.post("/new-models", json=data)
       assert response.status_code == 201
   ```

#### Frontend Feature

1. **Create Page Component**
   ```tsx
   // frontend/src/pages/NewPage.tsx
   export default function NewPage() {
       return <div>New Page</div>
   }
   ```

2. **Add Route**
   ```tsx
   // frontend/src/App.tsx
   <Route path="/new-page" element={<NewPage />} />
   ```

3. **Add Navigation Link**
   ```tsx
   // frontend/src/components/Layout.tsx
   <Link to="/new-page">New Page</Link>
   ```

4. **Integrate API**
   ```tsx
   // Use apiClient to fetch data
   const response = await apiClient.getNewData()
   ```

---

## Debugging & Troubleshooting

### Common Issues and Solutions

#### 1. Service Port Already in Use

```bash
# Check what's using the port
lsof -i :8001

# Kill the process
kill -9 <PID>

# Or use a different port
python -m uvicorn app.main:app --port 8010
```

#### 2. Database Connection Error

```bash
# Check if PostgreSQL is running
psql -U shopzy -h localhost -c "SELECT 1"

# Or check with Docker
docker ps | grep postgres

# Check PostgreSQL logs
docker logs shopzy-postgres
```

#### 3. Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Frontend Won't Start

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### 5. Docker Container Won't Start

```bash
# Check logs
docker-compose logs <service-name>

# Rebuild the image
docker-compose build <service-name>

# Restart
docker-compose up <service-name>
```

#### 6. Database Container Issues

```bash
# Check if container is running
docker ps | grep postgres

# Check logs
docker logs shopzy-postgres

# Restart PostgreSQL
docker-compose restart postgres

# Or remove and recreate
docker-compose down -v
docker-compose up postgres
```

### Debugging Tips

#### Python Services

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/debug")
async def debug():
    logger.debug("Debug message")
    return {"status": "ok"}

# Use debugger
import pdb; pdb.set_trace()
```

#### Frontend

```typescript
// Console logging
console.log("State:", state)
console.error("Error:", error)

// VS Code debugger configuration (.vscode/launch.json)
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/frontend"
    }
  ]
}
```

### Performance Issues

#### Slow API Responses

```bash
# Check service logs
docker-compose logs -f product-service

# Monitor database queries
# Or use timing tools
curl -w "@-" -o /dev/null -s \
  "http://localhost:8001/products" << 'EOF'
    time_total: %{time_total}\n
EOF
```

#### Memory Usage

```bash
# Monitor containers
docker stats

# Or on local Python
pip install memory-profiler
python -m memory_profiler services/product-service/app/main.py
```

---

## Environment Variables

### Backend Services

```bash
# Common for all services
DATABASE_URL=postgresql://shopzy:shopzy123@localhost:5432/service_db
SERVICE_PORT=8001

# Optional
DEBUG=True
LOG_LEVEL=INFO
```

### Frontend

```bash
# .env.local
VITE_API_URL=http://localhost:8000
NODE_ENV=development
```

---

## Summary

### Quick Commands Reference

**Docker Compose (Recommended):**
```bash
docker-compose up --build              # Start everything
docker-compose down                    # Stop everything
docker-compose logs -f                 # View logs
docker-compose restart <service>       # Restart service
```

**Individual Services:**
```bash
cd services/product-service
source venv/bin/activate
export DATABASE_URL="postgresql://shopzy:shopzy123@localhost:5432/product_db"
python -m uvicorn app.main:app --port 8001 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Testing:**
```bash
cd services/product-service
pytest tests/ -v
```

### Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| API Gateway | 8000 | Main entry point |
| Product Service | 8001 | Product management |
| Customer Service | 8002 | Customer management |
| Inventory Service | 8003 | Stock management |
| Order Service | 8004 | Order processing |
| Payment Service | 8005 | Payment handling |
| Notification Service | 8006 | Notifications |
| Frontend | 5173 | React application |
| PostgreSQL | 5432 | Database |

### Recommended Workflow

1. **For complete application:** Use `docker-compose up --build`
2. **For individual service development:** Run service locally with its own terminal
3. **For frontend development:** Run `npm run dev` in frontend directory
4. **For testing:** Run `pytest tests/ -v` in service directory

---

**Last Updated**: August 29, 2026

For more information, see README.md for project overview and DOCKER_SETUP.md for Docker details.
