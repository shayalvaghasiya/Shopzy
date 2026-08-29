import { useParams, Link } from 'react-router-dom'

export default function OrderConfirmation() {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="text-center py-12">
      <div className="bg-green-100 text-green-800 p-4 rounded-lg inline-block mb-6">
        <div className="text-5xl mb-2">✓</div>
        <p className="text-xl font-semibold">Order Confirmed!</p>
      </div>

      <h1 className="text-4xl font-bold mb-4">Thank you for your order</h1>
      <p className="text-xl text-gray-600 mb-8">Your order has been successfully placed</p>

      {id && (
        <div className="bg-gray-50 p-6 rounded-lg inline-block mb-8">
          <p className="text-gray-600 mb-2">Order ID:</p>
          <p className="text-2xl font-mono font-bold">{id}</p>
        </div>
      )}

      <p className="text-gray-600 mb-8">
        We'll send you an email confirmation shortly with tracking information and details about your order.
      </p>

      <div className="space-x-4">
        <Link
          to={id ? `/orders/${id}` : '/my-orders'}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 inline-block"
        >
          View Order Details
        </Link>
        <Link
          to="/products"
          className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 inline-block"
        >
          Continue Shopping
        </Link>
      </div>
    </div>
  )
}
