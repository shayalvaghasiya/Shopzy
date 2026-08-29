# Shopzy Development Guide

This document provides comprehensive instructions for setting up, running, and developing the Shopzy microservices e-commerce platform.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start - Complete Application](#quick-start---complete-application)
3. [Running Individual Services](#running-individual-services)
4. [Frontend Development](#frontend-development)
5. [Testing](#testing)
6. [Development Workflow](#development-workflow)
7. [Debugging & Troubleshooting](#debugging--troubleshooting)

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.11+** - For backend services
- **Node.js 18+** - For frontend
- **PostgreSQL 15** (optional) - For production database (SQLite used for testing)
- **Git** - For version control
- **pip** - Python package manager
- **npm** - Node package manager

### Installation

```bash
# Check Python version
python --version  # Should be 3.11 or higher

# Check Node version
node --version    # Should be 18 or higher

# Check npm version
npm --version
```

---

## Quick Start - Complete Application

This section guides you through running the entire Shopzy platform locally.

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd /path/to/shopzy

# Create a virtual environment for each service (optional but recommended)
python -m venv venv_services
source venv_services/bin/activate  # On Windows: venv_services\Scripts\activate
```

### Step 2: Start Backend Services

Open 7 separate terminal windows/tabs for each service. In each terminal:

#### Terminal 1: Product Service (Port 8001)
```bash
cd services/product-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### Terminal 2: Customer Service (Port 8002)
```bash
cd services/customer-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

#### Terminal 3: Inventory Service (Port 8003)
```bash
cd services/inventory-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

#### Terminal 4: Order Service (Port 8004)
```bash
cd services/order-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

#### Terminal 5: Payment Service (Port 8005)
```bash
cd services/payment-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

#### Terminal 6: Notification Service (Port 8006)
```bash
cd services/notification-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --host 0.0.0.0 --port 8006 --reload
```

#### Terminal 7: API Gateway (Port 8000)
```bash
cd services/api-gateway

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3: Start Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev

# Frontend will be available at http://localhost:5173
```

### Step 4: Verify All Services Running

Check that all services are accessible:

```bash
# Product Service
curl http://localhost:8001/docs

# Customer Service
curl http://localhost:8002/docs

# Inventory Service
curl http://localhost:8003/docs

# Order Service
curl http://localhost:8004/docs

# Payment Service
curl http://localhost:8005/docs

# Notification Service
curl http://localhost:8006/docs

# API Gateway
curl http://localhost:8000/docs

# Frontend
open http://localhost:5173
```

### Step 5: Access the Application

- **Frontend**: http://localhost:5173
- **API Gateway**: http://localhost:8000
- **Individual Service Docs**: http://localhost:800X/docs (where X is the service port digit)

---

## Running Individual Services

This section explains how to set up and run each service independently for development/testing.

### Product Service

**Purpose**: Manages product catalog, search, and filtering

```bash
cd services/product-service

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# API Documentation: http://localhost:8001/docs
# Health Check: http://localhost:8001/health

# Test endpoint
curl http://localhost:8001/products?page=1&page_size=10
```

### Customer Service

**Purpose**: Manages customer profiles, addresses, and personal information

```bash
cd services/customer-service

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

# API Documentation: http://localhost:8002/docs
# Health Check: http://localhost:8002/health

# Test endpoint
curl http://localhost:8002/customers?page=1&page_size=10
```

### Inventory Service

**Purpose**: Manages stock levels and reservations

```bash
cd services/inventory-service

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

# API Documentation: http://localhost:8003/docs
# Health Check: http://localhost:8003/health

# Test endpoint
curl http://localhost:8003/inventory?page=1&page_size=10
```

### Order Service

**Purpose**: Handles order creation, tracking, and management

```bash
cd services/order-service

# Setup
python -m venv venv
source venv/activate
pip install -r requirements.txt

# Run
python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload

# API Documentation: http://localhost:8004/docs
# Health Check: http://localhost:8004/health

# Test endpoint
curl http://localhost:8004/orders?page=1&page_size=10
```

### Payment Service

**Purpose**: Processes payments and refunds

```bash
cd services/payment-service

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python -m uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload

# API Documentation: http://localhost:8005/docs
# Health Check: http://localhost:8005/health

# Test endpoint
curl http://localhost:8005/payments?page=1&page_size=10
```

### Notification Service

**Purpose**: Sends notifications and manages notification preferences

```bash
cd services/notification-service

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python -m uvicorn app.main:app --host 0.0.0.0 --port 8006 --reload

# API Documentation: http://localhost:8006/docs
# Health Check: http://localhost:8006/health

# Test endpoint
curl http://localhost:8006/notifications?page=1&page_size=10
```

### API Gateway

**Purpose**: Routes requests to appropriate services

```bash
cd services/api-gateway

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# API Documentation: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
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

# Edit .env.local to match your setup
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

### Frontend Features

- **Home Page**: Landing page with featured products
- **Products Page**: Browse all products with filtering and search
- **Product Detail**: View product details and add to cart
- **Cart**: Manage shopping cart items
- **Checkout**: Complete purchase with shipping and payment info
- **Order Confirmation**: Success confirmation after purchase
- **My Orders**: View order history and tracking
- **Order Detail**: View detailed order information with status timeline

---

## Testing

### Running Tests for Individual Services

Each service includes comprehensive test suites. Run tests using pytest:

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

### Running All Tests

Create a script to run all tests:

```bash
#!/bin/bash
# run_all_tests.sh

echo "Running all service tests..."

for service in services/*/; do
    if [ -d "$service/tests" ]; then
        echo "Testing $(basename $service)..."
        cd "$service"
        pytest tests/ -v
        cd - > /dev/null
    fi
done

echo "All tests completed!"
```

Run the script:
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

### Test Database

Tests use SQLite in-memory databases for isolation:

```python
# conftest.py automatically creates and destroys test databases
# No external database needed for testing
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
# Check if service can connect
curl http://localhost:8001/health

# Check environment variables
echo $DATABASE_URL

# Verify database exists (if using PostgreSQL)
psql -U shopzy -h localhost -c "SELECT 1"
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

#### 5. API Gateway Not Routing Correctly

```bash
# Test direct service access
curl http://localhost:8001/health

# Test through gateway
curl http://localhost:8000/health

# Check if service URLs are correct in API Gateway config
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
# Check service logs for errors
# Monitor database queries
# Use curl with timing
curl -w "@-" -o /dev/null -s \
  "http://localhost:8001/products" << 'EOF'
    time_namelookup:  %{time_namelookup}\n
    time_connect:     %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
    time_pretransfer: %{time_pretransfer}\n
    time_redirect:    %{time_redirect}\n
    time_starttransfer: %{time_starttransfer}\n
    ------\n
    time_total:       %{time_total}\n
EOF
```

#### Memory Usage

```bash
# Monitor Python service memory
watch -n 1 'ps aux | grep python'

# Use memory profiler
pip install memory-profiler
python -m memory_profiler services/product-service/app/main.py
```

---

## Environment Variables

### Backend Services

```bash
# Common for all services
DATABASE_URL=sqlite:///./test.db          # For testing
SERVICE_PORT=8001                         # Service port

# Optional
DEBUG=True                                # Enable debug mode
LOG_LEVEL=INFO                           # Logging level
```

### Frontend

```bash
# .env.local
VITE_API_URL=http://localhost:8000       # API Gateway URL
```

---

## Summary

### Quick Commands Reference

```bash
# Run complete application (in different terminals)
Terminal 1: cd services/product-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8001 --reload

Terminal 2: cd services/customer-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8002 --reload

Terminal 3: cd services/inventory-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8003 --reload

Terminal 4: cd services/order-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8004 --reload

Terminal 5: cd services/payment-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8005 --reload

Terminal 6: cd services/notification-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8006 --reload

Terminal 7: cd services/api-gateway && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8000 --reload

Terminal 8: cd frontend && npm install && npm run dev
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

---

**Last Updated**: August 29, 2026

For more information, see README.md for project overview and architecture details.
