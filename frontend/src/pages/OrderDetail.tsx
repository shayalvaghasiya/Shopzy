import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { apiClient } from '../api'

interface OrderDetail {
  id: string
  customer_id: string
  status: string
  subtotal: number
  tax: number
  shipping_cost: number
  total_amount: number
  created_at: string
  items: Array<{
    product_id: string
    product_name: string
    quantity: number
    unit_price: number
  }>
}

export default function OrderDetail() {
  const { id } = useParams<{ id: string }>()
  const [order, setOrder] = useState<OrderDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (id) {
      loadOrder()
    }
  }, [id])

  const loadOrder = async () => {
    try {
      const response = await apiClient.getOrder(id!)
      setOrder(response.data)
    } catch (err: any) {
      setError('Failed to load order')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusSteps = () => {
    const steps = ['PENDING', 'PAYMENT_PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED']
    const currentIndex = steps.indexOf(order?.status || '')
    return steps.map((step, index) => ({
      step,
      completed: index < currentIndex,
      current: index === currentIndex,
    }))
  }

  if (loading) return <div className="text-center py-12">Loading order...</div>
  if (error) return <div className="bg-red-100 text-red-800 p-4 rounded">{error}</div>
  if (!order) return <div className="text-center py-12">Order not found</div>

  const statusSteps = getStatusSteps()

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Order Details</h1>
        <p className="text-gray-600">Order ID: {order.id}</p>
      </div>

      {/* Status Timeline */}
      <div className="bg-gray-50 p-6 rounded-lg">
        <h2 className="text-xl font-bold mb-6">Order Status</h2>
        <div className="flex items-center justify-between">
          {statusSteps.map((item, index) => (
            <div key={item.step} className="flex flex-col items-center flex-1">
              <div
                className={`w-12 h-12 rounded-full flex items-center justify-center font-bold mb-2 ${
                  item.completed
                    ? 'bg-green-500 text-white'
                    : item.current
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-300 text-gray-600'
                }`}
              >
                {item.completed ? '✓' : index + 1}
              </div>
              <p className="text-sm text-center text-gray-600">{item.step}</p>
              {index < statusSteps.length - 1 && (
                <div
                  className={`h-1 flex-1 mx-2 mt-2 ${
                    item.completed ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                  style={{ width: '40px', marginTop: '-20px' }}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Order Info */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-50 p-6 rounded-lg">
          <p className="text-gray-600 text-sm mb-2">Order Date</p>
          <p className="text-xl font-bold">{new Date(order.created_at).toLocaleDateString()}</p>
        </div>
        <div className="bg-gray-50 p-6 rounded-lg">
          <p className="text-gray-600 text-sm mb-2">Current Status</p>
          <p className="text-xl font-bold text-blue-600">{order.status}</p>
        </div>
        <div className="bg-gray-50 p-6 rounded-lg">
          <p className="text-gray-600 text-sm mb-2">Total Amount</p>
          <p className="text-xl font-bold text-green-600">${order.total_amount.toFixed(2)}</p>
        </div>
      </div>

      {/* Order Items */}
      <div className="border rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold">Product</th>
              <th className="px-6 py-3 text-center text-sm font-semibold">Quantity</th>
              <th className="px-6 py-3 text-right text-sm font-semibold">Unit Price</th>
              <th className="px-6 py-3 text-right text-sm font-semibold">Total</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map((item) => (
              <tr key={item.product_id} className="border-t hover:bg-gray-50">
                <td className="px-6 py-4">{item.product_name}</td>
                <td className="px-6 py-4 text-center">{item.quantity}</td>
                <td className="px-6 py-4 text-right">${item.unit_price.toFixed(2)}</td>
                <td className="px-6 py-4 text-right font-semibold">
                  ${(item.quantity * item.unit_price).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pricing Summary */}
      <div className="bg-gray-50 p-6 rounded-lg max-w-md ml-auto space-y-3">
        <div className="flex justify-between">
          <span className="text-gray-600">Subtotal</span>
          <span className="font-semibold">${order.subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Tax</span>
          <span className="font-semibold">${order.tax.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Shipping</span>
          <span className="font-semibold">${order.shipping_cost.toFixed(2)}</span>
        </div>
        <div className="border-t pt-3 flex justify-between text-lg">
          <span className="font-bold">Total</span>
          <span className="font-bold text-blue-600">${order.total_amount.toFixed(2)}</span>
        </div>
      </div>
    </div>
  )
}
