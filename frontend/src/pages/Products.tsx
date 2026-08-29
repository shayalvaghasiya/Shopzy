import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiClient } from '../api'
import { useStore } from '../store'

interface Product {
  id: string
  name: string
  description: string
  price: number
  sku: string
  category: string
  image_url?: string
}

export default function Products() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [priceRange, setPriceRange] = useState([0, 1000])
  const addToCart = useStore((state) => state.addToCart)

  useEffect(() => {
    loadProducts()
  }, [page, search, category])

  const loadProducts = async () => {
    try {
      setLoading(true)
      let response
      if (search) {
        response = await apiClient.searchProducts(search)
      } else {
        response = await apiClient.getProducts(page, 12)
      }
      setProducts(response.data.items || [])
    } catch (err: any) {
      setError('Failed to load products')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = (product: Product) => {
    addToCart({
      product_id: product.id,
      product_name: product.name,
      quantity: 1,
      unit_price: product.price,
    })
  }

  const filteredProducts = products.filter((p) => {
    if (category && p.category !== category) return false
    if (p.price < priceRange[0] || p.price > priceRange[1]) return false
    return true
  })

  const categories = Array.from(new Set(products.map((p) => p.category)))

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* Filters */}
      <div className="bg-gray-50 p-6 rounded-lg h-fit">
        <h2 className="text-xl font-bold mb-4">Filters</h2>

        {/* Search */}
        <div className="mb-6">
          <label className="block text-sm font-semibold mb-2">Search</label>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search products..."
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        {/* Category */}
        <div className="mb-6">
          <label className="block text-sm font-semibold mb-2">Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-3 py-2 border rounded"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        {/* Price Range */}
        <div className="mb-6">
          <label className="block text-sm font-semibold mb-2">Price Range</label>
          <div className="space-y-2">
            <input
              type="range"
              min="0"
              max="1000"
              value={priceRange[0]}
              onChange={(e) => setPriceRange([parseInt(e.target.value), priceRange[1]])}
              className="w-full"
            />
            <input
              type="range"
              min="0"
              max="1000"
              value={priceRange[1]}
              onChange={(e) => setPriceRange([priceRange[0], parseInt(e.target.value)])}
              className="w-full"
            />
            <div className="text-sm text-gray-600">
              ${priceRange[0]} - ${priceRange[1]}
            </div>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="lg:col-span-3">
        {error && <div className="bg-red-100 text-red-800 p-4 rounded mb-4">{error}</div>}

        {loading ? (
          <div className="text-center py-12">Loading products...</div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {filteredProducts.map((product) => (
                <div key={product.id} className="border rounded-lg overflow-hidden hover:shadow-lg transition">
                  <Link to={`/products/${product.id}`}>
                    <div className="bg-gray-200 h-48 flex items-center justify-center">
                      {product.image_url ? (
                        <img
                          src={product.image_url}
                          alt={product.name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <span className="text-gray-400">No image</span>
                      )}
                    </div>
                  </Link>
                  <div className="p-4">
                    <Link to={`/products/${product.id}`}>
                      <h3 className="font-semibold text-lg hover:text-blue-600">{product.name}</h3>
                    </Link>
                    <p className="text-gray-600 text-sm mb-2">{product.category}</p>
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
                    <div className="flex justify-between items-center">
                      <p className="text-2xl font-bold text-blue-600">${product.price.toFixed(2)}</p>
                      <button
                        onClick={() => handleAddToCart(product)}
                        className="bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700"
                      >
                        Add to Cart
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center items-center gap-2">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="px-4 py-2 border rounded disabled:opacity-50"
              >
                Previous
              </button>
              <span className="px-4 py-2">Page {page}</span>
              <button
                onClick={() => setPage(page + 1)}
                className="px-4 py-2 border rounded hover:bg-gray-100"
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
