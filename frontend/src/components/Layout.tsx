import { Outlet, Link } from 'react-router-dom'
import { useStore } from '../store'

export default function Layout() {
  const cart = useStore((state) => state.cart)
  const cartItemCount = cart.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="text-2xl font-bold text-blue-600">
              Shopzy
            </Link>

            {/* Menu */}
            <div className="flex items-center gap-6">
              <Link to="/" className="text-gray-600 hover:text-blue-600 font-medium">
                Home
              </Link>
              <Link to="/products" className="text-gray-600 hover:text-blue-600 font-medium">
                Products
              </Link>
              <Link to="/my-orders" className="text-gray-600 hover:text-blue-600 font-medium">
                My Orders
              </Link>

              {/* Cart */}
              <Link to="/cart" className="relative">
                <div className="text-2xl">🛒</div>
                {cartItemCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                    {cartItemCount}
                  </span>
                )}
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-lg font-bold mb-4">About Shopzy</h3>
              <p className="text-gray-400 text-sm">Your one-stop shop for quality products at great prices.</p>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-4">Quick Links</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>
                  <Link to="/products" className="hover:text-white">
                    Shop
                  </Link>
                </li>
                <li>
                  <Link to="/my-orders" className="hover:text-white">
                    Orders
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-4">Support</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>
                  <a href="#" className="hover:text-white">
                    Contact Us
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white">
                    FAQ
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-4">Legal</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>
                  <a href="#" className="hover:text-white">
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white">
                    Terms of Service
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400 text-sm">
            <p>&copy; 2024 Shopzy. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
