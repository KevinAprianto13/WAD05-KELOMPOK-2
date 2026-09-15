<template>
  <NavBar />
  <div class="page">
    <div class="container">
      <h1>Pesanan Saya</h1>

      <div v-if="loading" class="loading-center"><div class="spinner"></div></div>

      <div v-else-if="orders.length === 0" class="empty-state">
        <div class="icon">📋</div>
        <h3>Belum ada pesanan</h3>
        <p>Yuk mulai belanja dan buat pesanan pertamamu!</p>
        <RouterLink to="/products" class="btn btn-primary" style="margin-top:24px" id="orders-go-shop">Belanja Sekarang</RouterLink>
      </div>

      <div v-else class="orders-list">
        <div v-for="order in orders" :key="order.id" class="order-card card" :id="`order-${order.id}`">
          <div class="order-header">
            <div>
              <div class="order-id">#{{ String(order.id).padStart(5, '0') }}</div>
              <div class="order-date text-muted">{{ formatDate(order.created_at) }}</div>
            </div>
            <span :class="['badge', `badge-${order.status}`]">{{ statusLabel(order.status) }}</span>
          </div>

          <div class="order-items">
            <div v-for="item in order.items" :key="item.id" class="order-item">
              <img :src="item.product.image_url || '/placeholder.jpg'" class="oi-img" />
              <div class="oi-info">
                <div class="oi-name">{{ item.product.name }}</div>
                <div class="oi-meta text-muted">{{ item.quantity }} × {{ formatPrice(item.unit_price) }}</div>
              </div>
              <div class="oi-subtotal">{{ formatPrice(item.unit_price * item.quantity) }}</div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-addr">
              <span class="text-muted">📍</span>
              <span class="text-secondary">{{ order.shipping_address.slice(0, 60) }}{{ order.shipping_address.length > 60 ? '...' : '' }}</span>
            </div>
            <div class="order-total">
              <span class="text-secondary">Total:</span>
              <span class="price">{{ formatPrice(order.total_price) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { ordersApi } from '@/api'

const orders = ref([])
const loading = ref(false)

const statusLabels = {
  pending: 'Menunggu', processing: 'Diproses',
  shipped: 'Dikirim', delivered: 'Selesai', cancelled: 'Dibatalkan'
}
function statusLabel(s) { return statusLabels[s] || s }
function formatPrice(p) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p)
}
function formatDate(d) {
  return new Date(d).toLocaleDateString('id-ID', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  loading.value = true
  try { const { data } = await ordersApi.myOrders(); orders.value = data }
  finally { loading.value = false }
})
</script>

<style scoped>
h1 { margin-bottom: 32px; }
.orders-list { display: flex; flex-direction: column; gap: 20px; }
.order-card { padding: 28px; }
.order-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.order-id { font-weight: 800; font-size: 1.1rem; margin-bottom: 4px; }
.order-date { font-size: 0.82rem; }
.order-items { display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; }
.order-item { display: flex; gap: 14px; align-items: center; }
.oi-img { width: 56px; height: 56px; object-fit: cover; border-radius: var(--radius-sm); flex-shrink: 0; }
.oi-info { flex: 1; }
.oi-name { font-weight: 600; font-size: 0.9rem; margin-bottom: 4px; }
.oi-meta { font-size: 0.8rem; }
.oi-subtotal { font-weight: 700; font-size: 0.9rem; }
.order-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 16px; border-top: 1px solid var(--border); gap: 16px; flex-wrap: wrap; }
.order-addr { display: flex; gap: 8px; align-items: center; font-size: 0.85rem; flex: 1; }
.order-total { display: flex; gap: 12px; align-items: center; font-size: 0.9rem; }
</style>
