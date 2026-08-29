# Shopzy - Docker Compose Setup

This project uses Docker Compose for easy local development. All 8 services (7 microservices + frontend) run in Docker containers with a shared PostgreSQL database.

## Quick Start

### Prerequisites

- Docker & Docker Compose installed
- 8GB+ available RAM
- Ports 5173, 8000-8006, 5432 available

### Start All Services

```bash
docker-compose up --build
```

This will:
- Create and start PostgreSQL database
- Build and start all 7 microservices
- Build and start React frontend
- Initialize databases

### First Time Setup

The first run will take longer as Docker images are built. Subsequent runs will be faster.

```bash
# Build images first (optional)
docker-compose build

# Start all services
docker-compose up
```

## Access Services

After all containers start:

**Frontend:**
- http://localhost:5173

**API Documentation:**
- API Gateway: http://localhost:8000/docs
- Product Service: http://localhost:8001/docs
- Customer Service: http://localhost:8002/docs
- Inventory Service: http://localhost:8003/docs
- Order Service: http://localhost:8004/docs
- Payment Service: http://localhost:8005/docs
- Notification Service: http://localhost:8006/docs

**Database:**
- Host: localhost:5432
- User: shopzy
- Password: shopzy123

## Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f product-service

# Last 100 lines
docker-compose logs --tail=100
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart product-service
```

### Rebuild and Start

```bash
# Rebuild images and start
docker-compose up --build

# Force rebuild (ignore cache)
docker-compose up --build --no-cache
```

## Service Details

| Service | Port | Container | Status |
|---------|------|-----------|--------|
| API Gateway | 8000 | shopzy-api-gateway | Main entry point |
| Product | 8001 | shopzy-product-service | Product catalog |
| Customer | 8002 | shopzy-customer-service | Customer management |
| Inventory | 8003 | shopzy-inventory-service | Stock management |
| Order | 8004 | shopzy-order-service | Order processing |
| Payment | 8005 | shopzy-payment-service | Payment handling |
| Notification | 8006 | shopzy-notification-service | Notifications |
| Frontend | 5173 | shopzy-frontend | React app |
| Database | 5432 | shopzy-postgres | PostgreSQL 15 |

## Development Workflow

### Making Changes

Changes to source code are automatically reflected in running containers:
- Backend: Services use `--reload` flag
- Frontend: Vite hot reload enabled

No need to restart containers for code changes.

### Running Tests

```bash
# Access service container
docker exec shopzy-product-service pytest tests/ -v

# Run tests for all services
docker exec shopzy-product-service pytest tests/ -v
docker exec shopzy-customer-service pytest tests/ -v
# ... etc
```

### Database Access

```bash
# Connect to PostgreSQL
psql -h localhost -U shopzy -d product_db

# Or using docker
docker exec -it shopzy-postgres psql -U shopzy -d product_db
```

## Troubleshooting

### Ports Already in Use

```bash
# Check what's using a port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

### Database Connection Issues

```bash
# Check if postgres is healthy
docker exec shopzy-postgres pg_isready -U shopzy

# View postgres logs
docker-compose logs postgres
```

### Service Won't Start

```bash
# Check service logs
docker-compose logs <service-name>

# Rebuild that service
docker-compose build <service-name>
docker-compose up <service-name>
```

### OutOfMemory Errors

```bash
# Increase Docker memory limit in Docker Desktop settings
# Or on Linux, check available memory
free -h

# Stop and remove all containers
docker-compose down -v

# Start again
docker-compose up
```

## Clean Up

```bash
# Remove all containers but keep images
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Remove all Shopzy images
docker image rm shopzy-*
```

## Production Considerations

This docker-compose setup is optimized for local development:
- Uses development Python base images
- Services run with `--reload` enabled
- Frontend runs in dev mode with hot reload
- No health checks configured (local only)
- Volumes are not persisted

For production:
- Use lightweight base images
- Disable reload/hot reload
- Add health checks
- Configure volume persistence
- Use secrets management
- Set resource limits

## Docker Compose Version

Requires: Docker Compose v2.0+ or `docker compose` CLI

Verify:
```bash
docker-compose --version
# or
docker compose version
```

## Environment Variables

Configuration in docker-compose.yml:
- `POSTGRES_USER`: shopzy
- `POSTGRES_PASSWORD`: shopzy123
- `DATABASE_URL`: postgresql://shopzy:shopzy123@postgres:5432/{service}_db
- `SERVICE_PORT`: Individual service ports (8000-8006)
- `PYTHONUNBUFFERED`: 1 (for real-time logging)
- `VITE_API_URL`: http://localhost:8000 (frontend API endpoint)

Modify docker-compose.yml to change any values.

## Next Steps

1. Start containers: `docker-compose up --build`
2. Open browser: http://localhost:5173
3. Browse products, add to cart, checkout
4. Check API docs: http://localhost:8000/docs
5. Run tests: `docker exec shopzy-product-service pytest tests/ -v`

---

**Happy developing! 🚀**
