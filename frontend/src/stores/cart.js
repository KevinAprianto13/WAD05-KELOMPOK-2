import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartApi } from '@/api'

export const useCartStore = defineStore('cart', () => {
  const cart = ref(null)
  const loading = ref(false)

  const items = computed(() => cart.value?.items || [])
  const itemCount = computed(() => items.value.reduce((sum, i) => sum + i.quantity, 0))
  const total = computed(() =>
    items.value.reduce((sum, i) => sum + i.product.price * i.quantity, 0)
  )

  async function fetchCart() {
    loading.value = true
    try {
      const { data } = await cartApi.get()
      cart.value = data
    } finally {
      loading.value = false
    }
  }

  async function addItem(productId, quantity = 1) {
    const { data } = await cartApi.addItem({ product_id: productId, quantity })
    cart.value = data
  }

  async function updateItem(itemId, quantity) {
    const { data } = await cartApi.updateItem(itemId, { quantity })
    cart.value = data
  }

  async function removeItem(itemId) {
    const { data } = await cartApi.removeItem(itemId)
    cart.value = data
  }

  async function clearCart() {
    await cartApi.clear()
    cart.value = null
  }

  function reset() {
    cart.value = null
  }

  return { cart, items, itemCount, total, loading, fetchCart, addItem, updateItem, removeItem, clearCart, reset }
})
