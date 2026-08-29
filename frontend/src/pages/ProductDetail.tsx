import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
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

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [quantity, setQuantity] = useState(1)
  const addToCart = useStore((state) => state.addToCart)

  useEffect(() => {
    if (id) {
      loadProduct()
    }
  }, [id])

  const loadProduct = async () => {
    try {
      const response = await apiClient.getProduct(id!)
      setProduct(response.data)
    } catch (err: any) {
      setError('Failed to load product')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = () => {
    if (product) {
      addToCart({
        product_id: product.id,
        product_name: product.name,
        quantity,
        unit_price: product.price,
      })
      navigate('/cart')
    }
  }

  if (loading) return <div className="text-center py-12">Loading...</div>
  if (error) return <div className="bg-red-100 text-red-800 p-4 rounded">{error}</div>
  if (!product) return <div className="text-center py-12">Product not found</div>

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {/* Image */}
      <div className="bg-gray-200 rounded-lg h-96 flex items-center justify-center">
        {product.image_url ? (
          <img src={product.image_url} alt={product.name} className="w-full h-full object-cover rounded-lg" />
        ) : (
          <span className="text-gray-400">No image available</span>
        )}
      </div>

      {/* Details */}
      <div>
        <p className="text-gray-600 mb-2">{product.category}</p>
        <h1 className="text-4xl font-bold mb-2">{product.name}</h1>
        <p className="text-gray-600 mb-4">SKU: {product.sku}</p>

        <p className="text-5xl font-bold text-blue-600 mb-6">${product.price.toFixed(2)}</p>

        <p className="text-gray-700 mb-8">{product.description}</p>

        {/* Quantity Selector */}
        <div className="flex items-center gap-4 mb-6">
          <label className="font-semibold">Quantity:</label>
          <div className="flex items-center border rounded">
            <button
              onClick={() => setQuantity(Math.max(1, quantity - 1))}
              className="px-3 py-2 hover:bg-gray-100"
            >
              -
            </button>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
              className="w-16 text-center py-2 border-x"
            />
            <button onClick={() => setQuantity(quantity + 1)} className="px-3 py-2 hover:bg-gray-100">
              +
            </button>
          </div>
        </div>

        {/* Add to Cart Button */}
        <button
          onClick={handleAddToCart}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 mb-4"
        >
          Add to Cart
        </button>

        {/* Additional Info */}
        <div className="border-t pt-6 space-y-4">
          <div className="flex justify-between">
            <span className="text-gray-600">Availability:</span>
            <span className="font-semibold text-green-600">In Stock</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Shipping:</span>
            <span className="font-semibold">Free on orders over $50</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Returns:</span>
            <span className="font-semibold">30-day guarantee</span>
          </div>
        </div>
      </div>
    </div>
  )
}
