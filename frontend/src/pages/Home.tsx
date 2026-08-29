import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiClient } from '../api'

interface Product {
  id: string
  name: string
  description: string
  price: number
  sku: string
  category: string
  image_url?: string
}

export default function Home() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadFeaturedProducts()
  }, [])

  const loadFeaturedProducts = async () => {
    try {
      const response = await apiClient.getProducts(1, 6)
      setFeaturedProducts(response.data.items || [])
    } catch (err: any) {
      setError('Failed to load products')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20 rounded-lg">
        <div className="text-center">
          <h1 className="text-5xl font-bold mb-4">Welcome to Shopzy</h1>
          <p className="text-xl mb-8">Your one-stop shop for everything you need</p>
          <Link
            to="/products"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100"
          >
            Shop Now
          </Link>
        </div>
      </section>

      {/* Featured Products */}
      <section>
        <h2 className="text-3xl font-bold mb-8">Featured Products</h2>
        {error && <div className="bg-red-100 text-red-800 p-4 rounded mb-4">{error}</div>}
        {loading ? (
          <div className="text-center py-12">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredProducts.map((product) => (
              <Link
                key={product.id}
                to={`/products/${product.id}`}
                className="border rounded-lg overflow-hidden hover:shadow-lg transition"
              >
                <div className="bg-gray-200 h-48 flex items-center justify-center">
                  {product.image_url ? (
                    <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
                  ) : (
                    <span className="text-gray-400">No image</span>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-lg">{product.name}</h3>
                  <p className="text-gray-600 text-sm mb-2">{product.category}</p>
                  <p className="text-2xl font-bold text-blue-600">${product.price.toFixed(2)}</p>
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Info Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="text-center">
          <div className="text-4xl mb-2">🚚</div>
          <h3 className="font-semibold mb-2">Fast Shipping</h3>
          <p className="text-gray-600">Free shipping on orders over $50</p>
        </div>
        <div className="text-center">
          <div className="text-4xl mb-2">🛡️</div>
          <h3 className="font-semibold mb-2">Secure Payment</h3>
          <p className="text-gray-600">Your payment is secure and encrypted</p>
        </div>
        <div className="text-center">
          <div className="text-4xl mb-2">↩️</div>
          <h3 className="font-semibold mb-2">Easy Returns</h3>
          <p className="text-gray-600">30-day money-back guarantee</p>
        </div>
      </section>
    </div>
  )
}
