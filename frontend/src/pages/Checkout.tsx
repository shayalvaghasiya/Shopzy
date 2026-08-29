import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiClient } from '../api'
import { useStore } from '../store'

export default function Checkout() {
  const navigate = useNavigate()
  const cart = useStore((state) => state.cart)
  const clearCart = useStore((state) => state.clearCart)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [formData, setFormData] = useState({
    customerId: '',
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    cardNumber: '',
    cardExpiry: '',
    cardCvv: '',
  })

  const subtotal = cart.reduce((sum, item) => sum + item.unit_price * item.quantity, 0)
  const tax = subtotal * 0.1
  const shippingCost = subtotal > 50 ? 0 : 10
  const total = subtotal + tax + shippingCost

  if (cart.length === 0) {
    return (
      <div className="text-center py-12">
        <h1 className="text-3xl font-bold mb-4">Your cart is empty</h1>
        <button
          onClick={() => navigate('/products')}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          Continue Shopping
        </button>
      </div>
    )
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // Create or get customer
      const customerResponse = await apiClient.createCustomer({
        first_name: formData.firstName,
        last_name: formData.lastName,
        email: formData.email,
        phone: formData.phone,
      })

      const customerId = customerResponse.data.id

      // Add address
      await apiClient.updateCustomer(customerId, {
        first_name: formData.firstName,
        last_name: formData.lastName,
        email: formData.email,
        phone: formData.phone,
      })

      // Create order
      const orderResponse = await apiClient.createOrder({
        customer_id: customerId,
        items: cart,
      })

      const orderId = orderResponse.data.id

      // Process payment
      await apiClient.getPayment(orderId) // This would be a payment creation in real scenario

      clearCart()
      navigate(`/order-confirmation/${orderId}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process order')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Checkout Form */}
      <div className="lg:col-span-2">
        <h1 className="text-3xl font-bold mb-8">Checkout</h1>

        {error && <div className="bg-red-100 text-red-800 p-4 rounded mb-6">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Shipping Information */}
          <section className="border-b pb-8">
            <h2 className="text-xl font-bold mb-4">Shipping Address</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                name="firstName"
                placeholder="First Name"
                value={formData.firstName}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded"
              />
              <input
                type="text"
                name="lastName"
                placeholder="Last Name"
                value={formData.lastName}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded"
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded md:col-span-2"
              />
              <input
                type="tel"
                name="phone"
                placeholder="Phone"
                value={formData.phone}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded md:col-span-2"
              />
              <input
                type="text"
                name="address"
                placeholder="Street Address"
                value={formData.address}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded md:col-span-2"
              />
              <input
                type="text"
                name="city"
                placeholder="City"
                value={formData.city}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded"
              />
              <input
                type="text"
                name="state"
                placeholder="State"
                value={formData.state}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded"
              />
              <input
                type="text"
                name="zipCode"
                placeholder="ZIP Code"
                value={formData.zipCode}
                onChange={handleInputChange}
                required
                className="px-4 py-2 border rounded"
              />
            </div>
          </section>

          {/* Payment Information */}
          <section className="border-b pb-8">
            <h2 className="text-xl font-bold mb-4">Payment Method</h2>
            <div className="space-y-4">
              <input
                type="text"
                name="cardNumber"
                placeholder="Card Number"
                value={formData.cardNumber}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border rounded"
              />
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  name="cardExpiry"
                  placeholder="MM/YY"
                  value={formData.cardExpiry}
                  onChange={handleInputChange}
                  required
                  className="px-4 py-2 border rounded"
                />
                <input
                  type="text"
                  name="cardCvv"
                  placeholder="CVV"
                  value={formData.cardCvv}
                  onChange={handleInputChange}
                  required
                  className="px-4 py-2 border rounded"
                />
              </div>
            </div>
          </section>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Place Order'}
          </button>
        </form>
      </div>

      {/* Order Summary */}
      <div className="bg-gray-50 p-6 rounded-lg h-fit">
        <h2 className="text-xl font-bold mb-6">Order Summary</h2>

        <div className="space-y-3 mb-6">
          {cart.map((item) => (
            <div key={item.product_id} className="flex justify-between text-sm">
              <span>{item.product_name} x {item.quantity}</span>
              <span>${(item.unit_price * item.quantity).toFixed(2)}</span>
            </div>
          ))}
        </div>

        <div className="space-y-3 mb-6 pb-6 border-b">
          <div className="flex justify-between">
            <span className="text-gray-600">Subtotal</span>
            <span>${subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Tax (10%)</span>
            <span>${tax.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Shipping</span>
            <span>${shippingCost.toFixed(2)}</span>
          </div>
        </div>

        <div className="flex justify-between text-xl font-bold">
          <span>Total</span>
          <span className="text-blue-600">${total.toFixed(2)}</span>
        </div>
      </div>
    </div>
  )
}
