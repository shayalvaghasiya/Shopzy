import { create } from 'zustand'

export interface CartItem {
  product_id: string
  product_name: string
  quantity: number
  unit_price: number
}

interface Store {
  cart: CartItem[]
  addToCart: (item: CartItem) => void
  removeFromCart: (productId: string) => void
  updateQuantity: (productId: string, quantity: number) => void
  clearCart: () => void
}

export const useStore = create<Store>((set) => ({
  cart: [],
  addToCart: (item) =>
    set((state) => {
      const existing = state.cart.find((i) => i.product_id === item.product_id)
      if (existing) {
        return {
          cart: state.cart.map((i) =>
            i.product_id === item.product_id
              ? { ...i, quantity: i.quantity + item.quantity }
              : i
          ),
        }
      }
      return {
        cart: [...state.cart, item],
      }
    }),
  removeFromCart: (productId) =>
    set((state) => ({
      cart: state.cart.filter((i) => i.product_id !== productId),
    })),
  updateQuantity: (productId, quantity) =>
    set((state) => ({
      cart:
        quantity > 0
          ? state.cart.map((i) =>
              i.product_id === productId ? { ...i, quantity } : i
            )
          : state.cart.filter((i) => i.product_id !== productId),
    })),
  clearCart: () => set({ cart: [] }),
}))
