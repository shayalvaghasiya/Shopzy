import axios, { AxiosInstance } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api`,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Products
  getProducts(page = 1, limit = 20) {
    return this.client.get('/products', { params: { page, limit } });
  }

  getProduct(id: string) {
    return this.client.get(`/products/${id}`);
  }

  searchProducts(query: string) {
    return this.client.get('/products/search', { params: { query } });
  }

  // Customers
  createCustomer(data: any) {
    return this.client.post('/customers', data);
  }

  getCustomer(id: string) {
    return this.client.get(`/customers/${id}`);
  }

  updateCustomer(id: string, data: any) {
    return this.client.put(`/customers/${id}`, data);
  }

  // Orders
  createOrder(data: any) {
    return this.client.post('/orders', data, {
      headers: {
        'Idempotency-Key': this.generateIdempotencyKey(),
      },
    });
  }

  getOrders(customerId?: string, page = 1, limit = 20) {
    return this.client.get('/orders', {
      params: { customer_id: customerId, page, limit }
    });
  }

  getOrder(id: string) {
    return this.client.get(`/orders/${id}`);
  }

  cancelOrder(id: string) {
    return this.client.delete(`/orders/${id}`);
  }

  // Inventory
  getInventory(productId: string) {
    return this.client.get(`/inventory/${productId}`);
  }

  // Payments
  getPayment(id: string) {
    return this.client.get(`/payments/${id}`);
  }

  // Notifications
  getNotifications(customerId?: string) {
    return this.client.get('/notifications', {
      params: { customer_id: customerId },
    });
  }

  markNotificationAsRead(id: string) {
    return this.client.patch(`/notifications/${id}/read`);
  }

  private generateIdempotencyKey(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

export const apiClient = new ApiClient();
