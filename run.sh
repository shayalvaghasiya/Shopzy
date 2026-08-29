#!/bin/bash

# Shopzy - Complete Application Startup Script
# This script starts all 7 microservices + API Gateway + Frontend
# Usage: ./run.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

print_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        Shopzy - Microservices E-Commerce Platform             ║"
echo "║              Starting Complete Application                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check for required commands
print_info "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi
print_success "Python 3 found: $(python3 --version)"

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed"
    exit 1
fi
print_success "Node.js found: $(node --version)"

if ! command -v npm &> /dev/null; then
    print_error "npm is not installed"
    exit 1
fi
print_success "npm found: $(npm --version)"

echo ""

# Function to start a service
start_service() {
    local service_name=$1
    local service_path=$2
    local port=$3
    local description=$4

    print_info "Setting up $description (Port $port)..."

    cd "$service_path"

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_warning "Creating virtual environment for $service_name..."
        python3 -m venv venv
    fi

    # Activate virtual environment and install dependencies
    source venv/bin/activate

    if [ ! -f "installed.marker" ]; then
        pip install -q -r requirements.txt 2>/dev/null
        touch installed.marker
    fi

    # Start the service in background
    print_info "Starting $description..."
    python -m uvicorn app.main:app --host 0.0.0.0 --port $port --reload > /tmp/${service_name}.log 2>&1 &

    local pid=$!
    echo $pid > /tmp/${service_name}.pid

    print_success "$description started (PID: $pid)"

    cd - > /dev/null
}

# Function to start frontend
start_frontend() {
    print_info "Setting up Frontend..."

    cd frontend

    if [ ! -d "node_modules" ]; then
        print_warning "Installing npm dependencies..."
        npm install -q 2>/dev/null
    fi

    print_info "Starting Frontend (Port 5173)..."
    npm run dev > /tmp/frontend.log 2>&1 &

    local pid=$!
    echo $pid > /tmp/frontend.pid

    print_success "Frontend started (PID: $pid)"

    cd - > /dev/null
}

# Start all services
print_info "Starting all services..."
echo ""

start_service "product-service" "services/product-service" 8001 "Product Service"
sleep 1

start_service "customer-service" "services/customer-service" 8002 "Customer Service"
sleep 1

start_service "inventory-service" "services/inventory-service" 8003 "Inventory Service"
sleep 1

start_service "order-service" "services/order-service" 8004 "Order Service"
sleep 1

start_service "payment-service" "services/payment-service" 8005 "Payment Service"
sleep 1

start_service "notification-service" "services/notification-service" 8006 "Notification Service"
sleep 1

start_service "api-gateway" "services/api-gateway" 8000 "API Gateway"
sleep 2

start_frontend
sleep 3

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          All Services Started Successfully! ✓                  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

print_success "Frontend is running at: http://localhost:5173"
echo ""
print_info "API Endpoints:"
echo "  • API Gateway:        http://localhost:8000/docs"
echo "  • Product Service:    http://localhost:8001/docs"
echo "  • Customer Service:   http://localhost:8002/docs"
echo "  • Inventory Service:  http://localhost:8003/docs"
echo "  • Order Service:      http://localhost:8004/docs"
echo "  • Payment Service:    http://localhost:8005/docs"
echo "  • Notification Svc:   http://localhost:8006/docs"
echo ""
print_info "Running Services (PIDs):"
for pid_file in /tmp/*-service.pid /tmp/api-gateway.pid /tmp/frontend.pid; do
    if [ -f "$pid_file" ]; then
        service_name=$(basename "$pid_file" .pid)
        pid=$(cat "$pid_file")
        echo "  • $service_name: $pid"
    fi
done
echo ""

print_warning "Press Ctrl+C to stop all services"
print_info "Service logs are available in /tmp/*.log"
echo ""

# Wait for interrupt
trap cleanup INT

cleanup() {
    echo ""
    print_warning "Stopping all services..."

    for pid_file in /tmp/*-service.pid /tmp/api-gateway.pid /tmp/frontend.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null || true
            fi
            rm "$pid_file"
        fi
    done

    print_success "All services stopped"
    exit 0
}

# Keep the script running
wait
