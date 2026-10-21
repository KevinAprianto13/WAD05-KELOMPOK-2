<template>
  <div>
    <h1 style="margin-bottom:28px">Manajemen Pesanan</h1>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>
    <div v-else class="table-wrapper">
      <table id="orders-table">
        <thead>
          <tr>
            <th>ID</th><th>Customer</th><th>Total</th><th>Metode</th><th>Status</th><th>Tanggal</th><th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id" :id="`admin-order-${order.id}`">
            <td class="font-bold">#{{ String(order.id).padStart(5, '0') }}</td>
            <td>
              <div style="font-weight:600;font-size:.9rem">{{ order.user?.full_name }}</div>
              <div class="text-muted" style="font-size:.8rem">{{ order.user?.email }}</div>
            </td>
            <td class="price">{{ formatPrice(order.total_price) }}</td>
            <td class="text-secondary">{{ order.payment?.method || '—' }}</td>
            <td>
              <select
                class="status-select"
                :id="`order-status-${order.id}`"
                :value="order.status"
                @change="updateStatus(order.id, $event.target)"
              >
                <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </td>
            <td class="text-muted" style="font-size:.82rem">{{ formatDate(order.created_at) }}</td>
            <td>
              <button class="btn btn-secondary btn-sm" :id="`view-order-${order.id}`" @click="selected = order">Detail</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Order Detail Modal -->
    <div v-if="selected" class="modal-overlay" @click.self="selected = null">
      <div class="modal-box card">
        <div class="modal-header">
          <h3>Detail Pesanan #{{ String(selected.id).padStart(5, '0') }}</h3>
          <button class="modal-close" id="order-modal-close" @click="selected = null">✕</button>
        </div>
        <div class="order-detail-items">
          <div v-for="item in selected.items" :key="item.id" class="od-item">
            <img :src="item.product.image_url || '/placeholder.jpg'" class="od-img" />
            <div class="od-info">
              <div style="font-weight:600">{{ item.product.name }}</div>
              <div class="text-muted" style="font-size:.8rem">{{ item.quantity }} × {{ formatPrice(item.unit_price) }}</div>
            </div>
            <div class="price" style="font-size:.9rem">{{ formatPrice(item.unit_price * item.quantity) }}</div>
          </div>
        </div>
        <div class="divider"></div>
        <div class="od-footer">
          <div><span class="text-muted">Alamat:</span> {{ selected.shipping_address }}</div>
          <div style="margin-top:8px"><span class="text-muted">Total:</span> <strong class="price">{{ formatPrice(selected.total_price) }}</strong></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { ordersApi } from '@/api'

const toast = inject('toast')
const orders = ref([])
const loading = ref(false)
const selected = ref(null)

const statuses = [
  { value: 'pending', label: 'Menunggu' },
  { value: 'processing', label: 'Diproses' },
  { value: 'shipped', label: 'Dikirim' },
  { value: 'delivered', label: 'Selesai' },
  { value: 'cancelled', label: 'Dibatalkan' },
]

function formatPrice(p) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p)
}
function formatDate(d) {
  return new Date(d).toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function updateStatus(id, select) {
  const idx = orders.value.findIndex(o => o.id === id)
  try {
    const { data } = await ordersApi.updateStatus(id, select.value)
    if (idx !== -1) orders.value[idx] = data
    toast('Status pesanan diperbarui', 'success')
  } catch (e) {
    select.value = orders.value[idx].status
    toast(e.response?.data?.detail || 'Gagal memperbarui status', 'error')
  }
}

onMounted(async () => {
  loading.value = true
  try { const { data } = await ordersApi.allOrders(); orders.value = data }
  finally { loading.value = false }
})
</script>

<style scoped>
.status-select {
  background: var(--bg-secondary); border: 1px solid var(--border);
  color: var(--text-primary); padding: 6px 12px;
  border-radius: var(--radius-sm); font-size: 0.82rem; cursor: pointer;
}
.status-select:focus { border-color: var(--accent); }
.font-bold { font-weight: 700; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.7); backdrop-filter: blur(4px); z-index: 9000; display: flex; align-items: center; justify-content: center; padding: 24px; }
.modal-box { width: 100%; max-width: 600px; padding: 32px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.modal-close { background: none; color: var(--text-muted); font-size: 1.2rem; transition: var(--transition); }
.modal-close:hover { color: var(--text-primary); }
.order-detail-items { display: flex; flex-direction: column; gap: 12px; }
.od-item { display: flex; gap: 12px; align-items: center; }
.od-img { width: 52px; height: 52px; object-fit: cover; border-radius: var(--radius-sm); }
.od-info { flex: 1; }
.od-footer { font-size: 0.9rem; line-height: 1.8; }
</style>
