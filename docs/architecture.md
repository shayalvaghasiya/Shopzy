# Shopzy Microservices Architecture Documentation

## Overview

Shopzy is a production-grade e-commerce platform built with true microservices architecture. Each service owns its business domain, data, and API contracts.

## Service Boundaries

### Product Service (Port 8001)
**Responsibility**: Manage product catalog and metadata.

**Owned Data**:
- Product information (name, description, SKU, price, category, etc.)
- Product status (active, inactive, discontinued)
- Product images and metadata

**Key Endpoints**:
```
GET    /products              # List all products
GET    /products/{id}         # Get product details
POST   /products              # Create product (admin)
PUT    /products/{id}         # Update product (admin)
DELETE /products/{id}         # Delete product (admin)
GET    /products/search       # Search products
```

**External Clients**:
- Order Service (to fetch product details)

**Database**: `product_db`

---

### Inventory Service (Port 8002)
**Responsibility**: Manage stock levels and reservations.

**Owned Data**:
- Product inventory (available quantity, reserved quantity)
- Reservation records
- Stock history

**Key Operations**:
- **Check Inventory**: Verify if product has sufficient stock
- **Reserve**: Allocate inventory for an order
- **Release**: Return inventory reservation when order cancelled

**Key Endpoints**:
```
GET    /inventory/{product_id}              # Get inventory
POST   /inventory                           # Add inventory
PUT    /inventory/{product_id}              # Update inventory
PATCH  /inventory/{product_id}/reserve      # Reserve stock
PATCH  /inventory/{product_id}/release      # Release reservation
```

**Business Logic**:
- Prevents overselling through transactional updates
- Tracks available vs. reserved quantities separately
- Supports concurrent reservation attempts safely

**Database**: `inventory_db`

---

### Customer Service (Port 8003)
**Responsibility**: Manage customer profiles and addresses.

**Owned Data**:
- Customer profiles (name, email, phone, etc.)
- Customer addresses (billing, shipping, etc.)
- Customer preferences (optional for future)

**Key Endpoints**:
```
POST   /customers                      # Register customer
GET    /customers/{id}                 # Get customer profile
PUT    /customers/{id}                 # Update customer
DELETE /customers/{id}                 # Delete customer (soft delete)
GET    /customers/{id}/addresses       # List addresses
POST   /customers/{id}/addresses       # Add address
GET    /customers/{id}/addresses/{aid}  # Get address
PUT    /customers/{id}/addresses/{aid}  # Update address
```

**Validations**:
- Email format validation
- Phone number format validation
- Required fields validation

**Database**: `customer_db`

---

### Order Service (Port 8004)
**Responsibility**: Orchestrate order creation and lifecycle management.

**Owned Data**:
- Order records (order ID, customer ID, total, status, etc.)
- Order items (product references, quantities, prices)
- Order state transitions
- Idempotency records (for safe retries)

**Order Status Lifecycle**:
```
PENDING
   ↓
PAYMENT_PENDING
   ↓
CONFIRMED
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED

Cancellation allowed from: PENDING, PAYMENT_PENDING, CONFIRMED
```

**Key Endpoints**:
```
POST   /orders                    # Create order
GET    /orders/{id}               # Get order details
GET    /orders                    # List orders (with pagination)
PUT    /orders/{id}               # Update order status
DELETE /orders/{id}               # Cancel order
```

**Order Creation Flow**:
1. Validate customer (Customer Service API)
2. Validate products (Product Service API)
3. Check inventory (Inventory Service API)
4. Reserve inventory (Inventory Service API)
5. Calculate order total
6. Create order in PENDING status
7. Initiate payment (Payment Service API)
8. On payment success: Update order to CONFIRMED, publish ORDER_CREATED event
9. On payment failure: Release inventory, cancel order, publish ORDER_CANCELLED event

**Service Clients**:
- Customer Service (validate customer)
- Product Service (get product details)
- Inventory Service (check and reserve stock)
- Payment Service (process payment)

**Event Publishing**:
- `ORDER_CREATED`: When order confirmed
- `ORDER_CANCELLED`: When order cancelled
- `ORDER_PAYMENT_PENDING`: When waiting for payment

**Database**: `order_db`

---

### Payment Service (Port 8005)
**Responsibility**: Process payments (simulated for development).

**Owned Data**:
- Payment records (payment ID, order ID, amount, status, transaction reference)
- Payment history

**Payment Status Lifecycle**:
```
PENDING → PROCESSING → SUCCESS
                    ↓
                  FAILED
                    
SUCCESS → REFUNDED
```

**Key Endpoints**:
```
POST   /payments             # Create payment
GET    /payments/{id}        # Get payment details
POST   /payments/{id}/refund # Refund payment
```

**Simulated Payment Logic**:
- Configurable success rate (PAYMENT_SUCCESS_RATE env var)
- Simulated processing delay (PAYMENT_PROCESSING_DELAY_MS)
- Returns consistent results for same payment (idempotent)

**External Clients**:
- Order Service (initiates payments)

**Event Publishing**:
- `PAYMENT_SUCCESS`: When payment succeeds
- `PAYMENT_FAILED`: When payment fails
- `PAYMENT_REFUNDED`: When refund processed

**Database**: `payment_db`

---

### Notification Service (Port 8006)
**Responsibility**: Handle notifications (email, in-app) triggered by events.

**Owned Data**:
- Notification records
- Notification status
- Notification templates (for future)

**Notification Types**:
- `ORDER_CREATED`: Order confirmation
- `ORDER_CONFIRMED`: Payment successful
- `ORDER_CANCELLED`: Order cancelled
- `PAYMENT_SUCCESS`: Payment confirmation
- `PAYMENT_FAILED`: Payment failure
- `ORDER_SHIPPED`: Shipment notification
- `ORDER_DELIVERED`: Delivery notification

**Notification Channels**:
- Email (mock for development)
- In-app (stored in database)

**Key Endpoints**:
```
GET    /notifications              # List notifications
GET    /notifications/{id}         # Get notification
PATCH  /notifications/{id}/read    # Mark as read
```

**Event Consumption**:
- Listens to RabbitMQ for all published events
- Processes events asynchronously
- Sends notifications based on event type
- Handles failures gracefully (retry logic ready)

**Database**: `notification_db`

---

### API Gateway (Port 8000)
**Responsibility**: Route requests to appropriate services and handle cross-cutting concerns.

**Responsibilities**:
1. **Request Routing**: Forward requests to appropriate services
2. **Request ID Generation**: Add X-Request-ID header
3. **Correlation ID Propagation**: Maintain correlation IDs across services
4. **Response Standardization**: Ensure consistent response format
5. **Error Handling**: Catch service errors and return appropriate HTTP status
6. **CORS**: Handle cross-origin requests

**Route Mapping**:
```
/api/products/*      → Product Service
/api/inventory/*     → Inventory Service
/api/customers/*     → Customer Service
/api/orders/*        → Order Service
/api/payments/*      → Payment Service
/api/notifications/* → Notification Service
/health              → Gateway health
/ready               → Gateway readiness
```

**Request Flow**:
```
Client
  ↓
API Gateway
  ├─ Generate Request ID
  ├─ Extract/Propagate Correlation ID
  ├─ Log Request
  ↓
Service Handler
  ├─ Process Request
  ├─ Propagate Correlation ID in outbound calls
  ↓
API Gateway
  ├─ Log Response
  ├─ Return Standardized Response
```

**No Business Logic**: The gateway does not contain business logic. It purely routes and coordinates.

---

## Communication Patterns

### Synchronous (HTTP/REST)

Used when immediate response is required:

```
Order Service
    ↓ (HTTP GET /customers/{id})
Customer Service
    ↓ (Response)
Order Service
```

Benefits:
- Immediate feedback
- Simple error handling
- Request-response pattern

Trade-offs:
- Tight coupling on availability
- Must implement timeouts and retries

### Asynchronous (Event Publishing)

Used when operation doesn't require immediate response:

```
Order Service
    ↓ (Publish ORDER_CREATED event)
RabbitMQ Message Broker
    ↓
Notification Service (subscribes to ORDER_CREATED)
    ↓ (Send email/notification)
```

Benefits:
- Loose coupling
- High availability (service can be offline)
- Scalable
- Can add subscribers without changing publisher

Trade-offs:
- Eventual consistency
- Requires idempotent consumers
- Requires event schema management

---

## API Response Format

All services follow standardized response format:

### Success Response (200, 201, 204)
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Product Name",
    ...
  },
  "error": null,
  "request_id": "req-uuid"
}
```

### Error Response (4xx, 5xx)
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Product with ID xyz not found",
    "details": {
      "product_id": "xyz"
    }
  },
  "request_id": "req-uuid"
}
```

---

## Event Schema

All events published to RabbitMQ follow this schema:

```json
{
  "event_id": "uuid",
  "event_type": "ORDER_CREATED",
  "timestamp": "2026-08-29T10:00:00Z",
  "source": "order-service",
  "version": "1.0",
  "correlation_id": "req-uuid",
  "data": {
    "order_id": "uuid",
    "customer_id": "uuid",
    "total_amount": 599.99,
    ...
  }
}
```

**Event Versioning**: Each event type has a version. Consumers can handle multiple versions.

**Idempotency**: Events include `event_id` and `correlation_id`. Consumers store processed event IDs to prevent duplicate processing.

---

## Data Consistency

The system uses **eventual consistency**:

1. **Order Created**: Order status = PENDING
2. **Inventory Reserved**: Inventory updated, event published
3. **Payment Processed**: Payment status = SUCCESS, event published
4. **Order Confirmed**: Order status = CONFIRMED
5. **ORDER_CREATED event received by Notification Service**: Email sent

If payment fails:
1. Release inventory reservation
2. Cancel order
3. Publish ORDER_CANCELLED event
4. Notification Service sends failure email

**No Distributed Transactions**: Services don't coordinate multi-service ACID transactions. Instead, they use:
- Idempotent operations
- Saga pattern (through event choreography)
- Compensating transactions (e.g., release inventory if payment fails)

---

## Observability

### Request Tracing

All requests have unique IDs that flow through the system:

```
Frontend Request
  │
  ├─ X-Request-ID: abc-123
  ├─ X-Correlation-ID: corr-456
  │
  v
API Gateway
  │ (logs)
  │ request_id: abc-123
  │ correlation_id: corr-456
  │
  v
Order Service
  │ (logs)
  │ request_id: abc-123
  │ correlation_id: corr-456
  │
  ├─ Calls Inventory Service
  │  │ (propagates correlation_id)
  │  │
  │  v
  │  Inventory Service
  │    (logs)
  │    request_id: xyz-789 (new for this call)
  │    correlation_id: corr-456 (same)
```

### Structured Logging

All services log in JSON format with required fields:

```json
{
  "timestamp": "2026-08-29T10:00:00Z",
  "level": "INFO",
  "service": "order-service",
  "request_id": "abc-123",
  "correlation_id": "corr-456",
  "method": "POST",
  "path": "/orders",
  "status_code": 201,
  "latency_ms": 245,
  "message": "Order created successfully"
}
```

### Health Endpoints

Every service exposes:

```
GET /health
```
Returns service health status (alive check).

```
GET /ready
```
Returns readiness status (all dependencies available).

Used by orchestration systems (Kubernetes) to manage service availability.

---

## Deployment

### Local Development
```bash
docker-compose up -d
# All services run in containers
# Can inspect logs: docker-compose logs -f
```

### Container Images

Each service builds independent Docker image:
```bash
docker build -t shopzy/product-service:latest services/product-service/
docker build -t shopzy/order-service:latest services/order-service/
# etc.
```

### Kubernetes Ready

Services are designed for Kubernetes deployment:
- Health endpoints for liveness/readiness probes
- Environment-based configuration
- Stateless services (state in database)
- Graceful shutdown handling
- Resource requests/limits specified

---

## Security Considerations

### Data Isolation
- Each service owns its database
- No cross-database access
- API-only communication between services

### Input Validation
- All inputs validated with Pydantic schemas
- Type checking with Python type hints
- Custom validators for business rules

### Error Handling
- No stack traces exposed to clients
- Standardized error codes
- Request IDs for tracking issues

### Future: Authentication
- JWT tokens ready to be added at API Gateway
- Propagated to services in headers
- Services can validate authorization independently

---

## Idempotency

Critical operations support idempotency:

### Order Creation
Request with `Idempotency-Key: abc-123`:
- First request: Creates order, stores idempotency record
- Retry with same key: Returns existing order (no duplicate created)

### Payment Creation
Same pattern: Multiple requests with same idempotency key return same payment.

### Event Processing
Notification Service tracks processed event IDs to prevent duplicate notifications.

---

## Failure Scenarios

### Service Unavailable
If Inventory Service is down:
- Order Service receives error
- Returns HTTP 503 to client
- Client can retry
- Eventually, Inventory Service recovers

### Payment Failure
1. Order Service initiates payment
2. Payment Service returns FAILED status
3. Order Service releases inventory reservation
4. Order Service cancels order
5. Publishes ORDER_CANCELLED event
6. Notification Service sends cancellation email

### Partial Failure (Order Created, Payment Failed)
1. Order created (status: PAYMENT_PENDING)
2. Payment fails
3. Inventory released
4. Order cancelled
5. Customer notified

---

## Future Extensions

The architecture supports these additions without modifying existing services:

### Authentication Service
- New service manages auth
- API Gateway validates JWTs
- Services receive user context in headers

### Cart Service
- Independent service
- Frontend communicates with Cart Service
- Cart Service calls Product Service for details
- Checkout flow moves cart items to Order Service

### Search Service (Elasticsearch)
- Independent service
- Consumes product events
- Maintains search index
- Provides full-text search API

### Shipping Service
- Tracks shipments
- Publishes ORDER_SHIPPED, ORDER_DELIVERED events
- Notification Service subscribes to send notifications

Each addition follows the same patterns:
- Independent database
- API contracts
- Event publishing/consuming
- Service discovery

---

## Testing Strategy

### Unit Tests
Test business logic in isolation:
```python
def test_inventory_reserve():
    """Test successful inventory reservation."""
    service = InventoryService(mock_repository)
    result = service.reserve(product_id, quantity)
    assert result.success
```

### Integration Tests
Test service + database:
```python
def test_order_creation_flow():
    """Test complete order creation with database."""
    # Spins up test database
    # Creates customer, product, inventory
    # Creates order
    # Verifies all state changes
```

### Contract Tests
Verify service communication contracts:
```python
def test_product_service_api():
    """Verify Product Service API contract."""
    response = http.get("http://product-service:8001/products/123")
    assert response.json() has required fields
```

### Load Tests
Verify performance:
- Concurrent order creation
- Concurrent inventory reservations
- Message throughput

---

## Configuration Management

Services use environment variables for configuration:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host/db

# Service URLs
PRODUCT_SERVICE_URL=http://product-service:8001

# Message Broker
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

# Application
SERVICE_PORT=8001
ENVIRONMENT=production
LOG_LEVEL=INFO
```

No hardcoded values in code. Configuration is environment-specific.

---

## Monitoring and Alerting

Services expose metrics for monitoring:
- Request count
- Request latency
- Error count
- Business metrics (orders created, payments successful, etc.)

Metrics exposed on `/metrics` endpoint (Prometheus format).

Can be scraped by monitoring systems like Prometheus/Grafana.

Alerts can be configured for:
- High error rate
- High latency
- Service unavailability
- Payment failures
