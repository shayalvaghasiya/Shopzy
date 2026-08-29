# Shopzy Development Guide

This document provides comprehensive development instructions for the Shopzy microservices platform.

## Development Setup

### Prerequisites

- Docker & Docker Compose (for infrastructure)
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend service development)
- Git

### Local Development Workflow

The recommended approach for development is to work in separate terminals:

#### Terminal 1: Infrastructure Services
```bash
# Start PostgreSQL
psql -U shopzy -h localhost -d product_db

# Or run with Docker Compose
docker-compose up -d
```

#### Terminal 2: Message Broker
```bash
# If using Docker Compose, start with infrastructure
# RabbitMQ will be started by docker-compose
```

#### Terminal 3: Product Service (Reference Implementation)
```bash
cd services/product-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://shopzy:shopzy@localhost/product_db
export SERVICE_PORT=8001
python -m app.main
```

#### Terminal 4: Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Individual Service Development

Each service should be developed in isolation using the Product Service as a template:

```bash
# Navigate to service directory
cd services/inventory-service

# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
export DATABASE_URL=postgresql://shopzy:shopzy@localhost/inventory_db
export SERVICE_PORT=8002

# Run service
python -m app.main
```

### Database Initialization

The development database needs to be initialized:

```bash
# Create databases if using local PostgreSQL
createdb product_db
createdb inventory_db
createdb customer_db
createdb order_db
createdb payment_db
createdb notification_db

# Run initialization script (if available)
psql -U shopzy -d product_db -f scripts/init-databases.sql
```

### Service-to-Service Communication

During development, services can communicate directly via HTTP:

```bash
# Test Product Service
curl http://localhost:8001/health
curl http://localhost:8001/products

# Test Order Service depends on other services
# Requires all services running locally
```

### Local Testing Workflow

1. **Start Infrastructure**
   ```bash
   docker-compose up -d postgres rabbitmq
   ```

2. **Initialize Databases**
   ```bash
   # Run initialization script
   docker-compose exec postgres psql -U shopzy -f scripts/init-databases.sql
   ```

3. **Start Services Sequentially**
   ```bash
   # Terminal 1: Product Service
   cd services/product-service
   source venv/bin/activate
   export DATABASE_URL=postgresql://shopzy:shopzy@postgres:5432/product_db
   python -m app.main

   # Terminal 2: Inventory Service
   cd services/inventory-service
   source venv/bin/activate
   export DATABASE_URL=postgresql://shopzy:shopzy@postgres:5432/inventory_db
   python -m app.main

   # Continue for other services...
   ```

4. **Test Services**
   ```bash
   # Health check
curl http://localhost:8001/health
curl http://localhost:8002/health

   # API endpoint tests
curl http://localhost:8000/api/products
   ```

5. **Frontend Development**
   ```bash
   cd frontend
   npm run dev
   ```

## Quick Start Commands

### Start All Services (Docker)
```bash
docker-compose up -d
```

### Access Services
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Product Service**: http://localhost:8001/docs
- **Inventory Service**: http://localhost:8002/docs
- **Customer Service**: http://localhost:8003/docs
- **Order Service**: http://localhost:8004/docs
- **Payment Service**: http://localhost:8005/docs
- **Notification Service**: http://localhost:8006/docs

### Test Development Setup
```bash
# Check if services are running
curl http://localhost:8001/health

# Test API Gateway
curl http://localhost:8000/api/products

# Test Product Service directly
curl http://localhost:8001/products
```

## Service Development Patterns

### 1. Copy Product Service Structure

For each new service, use Product Service as a template:

```bash
# Copy the structure
cp -r services/product-service services/[new-service]

# Navigate to new service
cd services/[new-service]

# Adapt the following files:
# - app/models/[model].py - Update models for your domain
# - app/schemas/[model].py - Add Pydantic schemas
# - app/repositories/[model]_repository.py - Implement data access
# - app/services/[model]_service.py - Add business logic
# - app/api/routes.py - Add API endpoints
# - app/core/config.py - Update database URL
# - app/main.py - Include your routes
```

### 2. Inventory Service Example

```bash
cd services/inventory-service

# Adapt models for inventory management
cat > app/models/inventory.py << 'EOF'
# Inventory and Reservation models
EOF

# Add schemas
cat > app/schemas/inventory.py << 'EOF'
# InventoryCreate, InventoryUpdate, InventoryResponse schemas
EOF

# Implement repository
cat > app/repositories/inventory_repository.py << 'EOF'
# Inventory CRUD with reservation logic
EOF

# Add business logic
cat > app/services/inventory_service.py << 'EOF'
# Reservation and release operations
EOF

# Add routes
cat > app/api/routes.py << 'EOF'
# All inventory endpoints
EOF
```

### 3. Order Service Special Considerations

The Order Service requires additional components:

```bash
# 1. Add order state machine
# Update app/models/order.py with OrderStatus enum

# 2. Add service clients
# Create app/clients/ directory for:
# - ProductClient
# - InventoryClient
# - CustomerClient
# - PaymentClient

# 3. Add event publisher
# Create app/events/ directory for RabbitMQ integration

# 4. Implement orchestration logic
# Add order creation, validation, and coordination logic
```

## Testing Services Locally

### Unit Tests
```bash
cd services/product-service
pytest tests/unit/
```

### Integration Tests
```bash
cd services/product-service
pytest tests/integration/
```

### With Coverage
```bash
cd services/product-service
pytest --cov=app tests/
```

### Test Development Workflow

1. **Write Unit Tests First**
   ```python
   # test_repository.py - Test data access
   # test_service.py - Test business logic
   ```

2. **Add Integration Tests**
   ```python
   # test_integration.py - Test service + database
   ```

3. **Test API Endpoints**
   ```python
   # test_routes.py - Test FastAPI endpoints
   ```

## Development Best Practices

### 1. Use Environment Variables

```python
# In app/core/config.py
DATABASE_URL: str = os.getenv("DATABASE_URL")
SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", 8001))
```

### 2. Follow Clean Architecture

```
service/
├── app/
│   ├── api/           # API routes (outermost layer)
│   ├── services/      # Business logic
│   ├── repositories/  # Data access
│   ├── models/        # Database models (innermost)
│   └── core/          # Configuration and dependencies
```

### 3. Error Handling

```python
# Standardized error responses
from shared.utils import ResponseFormat, ErrorCode

@app.get("/products")
async def get_products():
    try:
        products = await product_service.get_all_products()
        return ResponseFormat.success(products)
    except Exception as e:
        return ResponseFormat.error(ErrorCode.INTERNAL_ERROR, str(e))
```

### 4. Logging

```python
# Use structured logging
import logging
from shared.utils import StructuredLogger

logger = StructuredLogger(__name__)

@app.post("/products")
async def create_product(product_data: ProductCreate):
    logger.info("Creating product", sku=product_data.sku)
    try:
        product = await product_service.create_product(product_data)
        logger.info("Product created successfully", product_id=product.id)
        return ResponseFormat.success(product)
    except Exception as e:
        logger.error("Failed to create product", error=str(e))
        return ResponseFormat.error(ErrorCode.VALIDATION_ERROR, str(e))
```

### 5. Service Communication

```python
# Service clients for inter-service communication
class ProductClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def get_product(self, product_id: str):
        async with self.session.get(f"{self.base_url}/products/{product_id}") as response:
            return await response.json()
```

## Debugging Tips

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check PostgreSQL is running
   psql -U shopzy -h localhost -c "SELECT 1"

   # Verify database exists
   psql -U shopzy -lqt | cut -d \| -f 1 | grep product_db
   ```

2. **Service Startup Issues**
   ```bash
   # Check if port is available
   lsof -i :8001

   # Kill process using port
   kill -9 $(lsof -t -i :8001)
   ```

3. **Environment Variables**
   ```bash
   # Check all environment variables
   env | grep PRODUCT

   # Or in Python
   import os
   for key, value in os.environ.items():
       if 'PRODUCT' in key:
           print(f"{key}={value}")
   ```

### Development Scripts

Create a `scripts/dev.sh` file:

```bash
#!/bin/bash

# Start all services for development
.
cd services/product-service
source venv/bin/activate
python -m app.main &

# Wait for service to start
sleep 3

# Run tests
pytest --cov=app

# Stop all background processes
kill %1
```

## Performance Optimization

### 1. Database Connection Pooling
```python
# In app/core/dependencies.py
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600
)
```

### 2. Asynchronous Operations
```python
# Use async/await for I/O operations
async def process_order(order_data: OrderCreate):
    # Process asynchronously
    async with aiohttp.ClientSession() as session:
        # Make concurrent calls to multiple services
        tasks = [
            session.get(f"{PRODUCT_SERVICE_URL}/products/{item['product_id']}"),
            session.get(f"{INVENTORY_SERVICE_URL}/inventory/check"),
            # ... other service calls
        ]
        responses = await asyncio.gather(*tasks)
        # Process all responses
```

## Migration Guide

When upgrading from one version to another:

1. **Backup Databases**
   ```bash
   pg_dump -U shopzy product_db > product_db_backup.sql
   pg_dump -U shopzy inventory_db > inventory_db_backup.sql
   # ... backup all databases
   ```

2. **Update Services**
   ```bash
   # Update each service to new version
   cd services/product-service
   git checkout v2.0.0
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   # Alembic migrations
   alembic upgrade head
   ```

4. **Test Integration**
   ```bash
   # Test all services end-to-end
   curl http://localhost:8000/api/products
   ```

## Support

### Common Development Questions

**Q: How do I run all services locally?**
A: Use docker-compose or start them sequentially in separate terminals as shown above.

**Q: How do I debug service-to-service communication?**
A: Use structured logging and check that service URLs are correctly configured in environment variables.

**Q: How do I handle database migrations?**
A: Use Alembic for database migrations. Run `alembic upgrade head` to apply all migrations.

**Q: How do I test the complete flow?**
A: Start all services, then use tools like Postman or curl to test API endpoints.

### Getting Help

1. **Check Documentation**
   - README.md - Main project overview
   - IMPLEMENTATION_GUIDE.md - Detailed development guide
   - docs/architecture.md - Architecture details

2. **Study Reference Implementation**
   - Product Service in services/product-service/
   - Shared utilities in shared/

3. **Join Discussions**
   - GitHub issues for bug reports
   - Discord/Slack for real-time help (if available)

## Development Checklist

### Before Starting Development
- [ ] All databases created and initialized
- [ ] Docker Compose installed (optional)
- [ ] Virtual environments set up for all services
- [ ] Environment variables configured

### During Development
- [ ] Follow clean architecture principles
- [ ] Write unit tests for all business logic
- [ ] Use structured logging
- [ ] Follow API contract standards
- [ ] Test service-to-service communication
- [ ] Keep services independent and loosely coupled

### Before Deployment
- [ ] All tests passing
- [ ] Docker containers built
- [ ] Environment variables set for production
- [ ] Health checks implemented and working
- [ ] Monitoring and logging configured

## Project Structure for Development

```
shopzy/
├── services/
│   ├── api-gateway/         # Request routing and CORS
│   ├── product-service/     # Product catalog (complete)
│   ├── inventory-service/   # Stock management (in progress)
│   ├── customer-service/    # Customer profiles (in progress)
│   ├── order-service/       # Order orchestration (in progress)
│   ├── payment-service/     # Payment processing (in progress)
│   └── notification-service/# Event-driven notifications (in progress)
│
├── shared/                  # Shared utilities and contracts
│   ├── event_schemas.py     # Event definitions
│   ├── utils.py            # Response formatting and logging
│   └── database.py         # Database utilities
│
├── docs/                    # Architecture and development docs
│   └── architecture.md
│
└── README.md                # Quick start and overview
```

---

**Development Guide maintained as living document**

For the most current development information, refer to this guide and the implementation guide for detailed step-by-step instructions.