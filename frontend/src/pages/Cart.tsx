import { Link } from 'react-router-dom'
import { useStore } from '../store'

interface CartItem {
  product_id: string
  product_name: string
  quantity: number
  unit_price: number
}

export default function Cart() {
  const cart = useStore((state) => state.cart)
  const removeFromCart = useStore((state) => state.removeFromCart)
  const updateQuantity = useStore((state) => state.updateQuantity)
  const clearCart = useStore((state) => state.clearCart)

  const subtotal = cart.reduce((sum, item) => sum + item.unit_price * item.quantity, 0)
  const tax = subtotal * 0.1
  const shippingCost = subtotal > 50 ? 0 : 10
  const total = subtotal + tax + shippingCost

  if (cart.length === 0) {
    return (
      <div className="text-center py-12">
        <h1 className="text-3xl font-bold mb-4">Your cart is empty</h1>
        <p className="text-gray-600 mb-6">Start shopping to add items to your cart</p>
        <Link to="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
          Continue Shopping
        </Link>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Cart Items */}
      <div className="lg:col-span-2">
        <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>

        <div className="space-y-4">
          {cart.map((item) => (
            <div key={item.product_id} className="border rounded-lg p-4 flex justify-between items-center">
              <div className="flex-1">
                <h3 className="font-semibold text-lg">{item.product_name}</h3>
                <p className="text-gray-600">${item.unit_price.toFixed(2)} each</p>
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center border rounded">
                  <button
                    onClick={() => updateQuantity(item.product_id, Math.max(1, item.quantity - 1))}
                    className="px-3 py-1 hover:bg-gray-100"
                  >
                    -
                  </button>
                  <input
                    type="number"
                    value={item.quantity}
                    onChange={(e) => updateQuantity(item.product_id, Math.max(1, parseInt(e.target.value) || 1))}
                    className="w-12 text-center py-1 border-x"
                  />
                  <button
                    onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                    className="px-3 py-1 hover:bg-gray-100"
                  >
                    +
                  </button>
                </div>

                <div className="text-right w-24">
                  <p className="font-semibold">${(item.unit_price * item.quantity).toFixed(2)}</p>
                </div>

                <button
                  onClick={() => removeFromCart(item.product_id)}
                  className="text-red-600 hover:text-red-800 font-semibold"
                >
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={clearCart}
          className="mt-6 px-4 py-2 border text-red-600 border-red-600 rounded hover:bg-red-50"
        >
          Clear Cart
        </button>
      </div>

      {/* Order Summary */}
      <div className="bg-gray-50 p-6 rounded-lg h-fit">
        <h2 className="text-xl font-bold mb-6">Order Summary</h2>

        <div className="space-y-3 mb-6 pb-6 border-b">
          <div className="flex justify-between">
            <span className="text-gray-600">Subtotal</span>
            <span className="font-semibold">${subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Tax (10%)</span>
            <span className="font-semibold">${tax.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Shipping</span>
            <span className="font-semibold">${shippingCost.toFixed(2)}</span>
          </div>
        </div>

        <div className="flex justify-between text-xl font-bold mb-6">
          <span>Total</span>
          <span className="text-blue-600">${total.toFixed(2)}</span>
        </div>

        <Link
          to="/checkout"
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 text-center block"
        >
          Proceed to Checkout
        </Link>
      </div>
    </div>
  )
}
