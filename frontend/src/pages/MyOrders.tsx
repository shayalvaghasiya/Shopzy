import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiClient } from '../api'

interface Order {
  id: string
  customer_id: string
  status: string
  total_amount: number
  created_at: string
  items: Array<{
    product_id: string
    product_name: string
    quantity: number
    unit_price: number
  }>
}

export default function MyOrders() {
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadOrders()
  }, [])

  const loadOrders = async () => {
    try {
      const response = await apiClient.getOrders(undefined, 1, 20)
      setOrders(response.data.items || [])
    } catch (err: any) {
      setError('Failed to load orders')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800'
      case 'PAYMENT_PENDING':
        return 'bg-orange-100 text-orange-800'
      case 'CONFIRMED':
        return 'bg-blue-100 text-blue-800'
      case 'SHIPPED':
        return 'bg-purple-100 text-purple-800'
      case 'DELIVERED':
        return 'bg-green-100 text-green-800'
      case 'CANCELLED':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) return <div className="text-center py-12">Loading orders...</div>

  if (orders.length === 0) {
    return (
      <div className="text-center py-12">
        <h1 className="text-3xl font-bold mb-4">No Orders Yet</h1>
        <p className="text-gray-600 mb-6">You haven't placed any orders yet</p>
        <Link to="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
          Start Shopping
        </Link>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">My Orders</h1>

      {error && <div className="bg-red-100 text-red-800 p-4 rounded mb-6">{error}</div>}

      <div className="space-y-4">
        {orders.map((order) => (
          <div key={order.id} className="border rounded-lg p-6 hover:shadow-lg transition">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <div>
                <p className="text-gray-600 text-sm">Order ID</p>
                <p className="font-mono font-semibold">{order.id.slice(0, 8)}...</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Date</p>
                <p className="font-semibold">
                  {new Date(order.created_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Total</p>
                <p className="font-semibold text-lg text-blue-600">${order.total_amount.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Status</p>
                <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(order.status)}`}>
                  {order.status}
                </span>
              </div>
            </div>

            <div className="border-t pt-4">
              <p className="text-sm font-semibold text-gray-600 mb-2">Items:</p>
              <ul className="text-sm space-y-1">
                {order.items?.map((item) => (
                  <li key={item.product_id}>
                    {item.product_name} x {item.quantity} @ ${item.unit_price.toFixed(2)}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-4 flex gap-2">
              <Link
                to={`/orders/${order.id}`}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
