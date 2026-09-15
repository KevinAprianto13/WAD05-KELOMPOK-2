<template>
  <NavBar />
  <div class="page shopee-checkout-page">
    <div class="container">
      <div v-if="success" class="success-screen card">
        <div class="success-icon">✅</div>
        <h2>Pesanan Berhasil Dibuat</h2>
        <p class="text-secondary">Pesanan Anda telah berhasil dibuat dan sedang diproses.</p>
        <div class="success-actions">
          <RouterLink to="/orders" class="btn btn-outline" id="checkout-view-orders">Lihat Pesanan Saya</RouterLink>
          <RouterLink to="/products" class="shopee-btn-buy" id="checkout-continue">Kembali ke Beranda</RouterLink>
        </div>
      </div>

      <div v-else class="checkout-layout">
        <!-- Address -->
        <div class="shopee-card address-card">
          <div class="card-title"><span class="icon-pin">📍</span> Alamat Pengiriman</div>
          <form @submit.prevent="handleCheckout" id="checkout-form">
            <textarea
              id="checkout-address"
              v-model="form.shipping_address"
              class="form-input address-input"
              rows="3"
              placeholder="Masukkan alamat pengiriman lengkap Anda..."
              required
            ></textarea>
          </form>
        </div>

        <!-- Products -->
        <div class="shopee-card products-card">
          <div class="shopee-cart-header">
            <div class="col-product">Produk Dipesan</div>
            <div class="col-price">Harga Satuan</div>
            <div class="col-qty">Jumlah</div>
            <div class="col-total">Subtotal Produk</div>
          </div>
          
          <div class="shopee-cart-items">
            <div v-for="item in cart.items" :key="item.id" class="shopee-cart-item">
              <div class="col-product">
                <img :src="item.product.image_url || '/placeholder.jpg'" class="item-img" />
                <div class="item-info">
                  <div class="item-name">{{ item.product.name }}</div>
                </div>
              </div>
              <div class="col-price">{{ formatPrice(item.product.price) }}</div>
              <div class="col-qty">{{ item.quantity }}</div>
              <div class="col-total price">{{ formatPrice(item.product.price * item.quantity) }}</div>
            </div>
          </div>
          
          <div class="notes-row">
            <label>Pesan:</label>
            <input id="checkout-notes" v-model="form.notes" type="text" class="form-input notes-input" placeholder="(Opsional) Tinggalkan pesan ke penjual" />
          </div>
        </div>

        <!-- Payment -->
        <div class="shopee-card payment-card">
          <div class="card-title">Metode Pembayaran</div>
          <div class="payment-options">
            <label v-for="m in paymentMethods" :key="m.value" class="payment-option" :class="{ active: form.payment_method === m.value }">
              <input type="radio" v-model="form.payment_method" :value="m.value" style="display:none" />
              <span>{{ m.label }}</span>
              <span class="active-mark" v-if="form.payment_method === m.value">✓</span>
            </label>
          </div>
        </div>

        <!-- Summary Footer -->
        <div class="shopee-checkout-footer">
          <div class="footer-summary">
            <div class="summary-line">
              <span>Subtotal untuk Produk:</span>
              <span>{{ formatPrice(cart.total) }}</span>
            </div>
            <div class="summary-line">
              <span>Total Ongkos Kirim:</span>
              <span>Rp0</span>
            </div>
            <div class="summary-line total-line">
              <span>Total Pembayaran:</span>
              <span class="final-total">{{ formatPrice(cart.total) }}</span>
            </div>
          </div>
          
          <div class="footer-actions">
            <div v-if="error" class="error-msg">{{ error }}</div>
            <button id="checkout-submit" type="submit" class="shopee-btn-buy place-order-btn" form="checkout-form" :disabled="loading || cart.items.length === 0">
              {{ loading ? 'Memproses...' : 'Buat Pesanan' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useCartStore } from '@/stores/cart'
import { ordersApi } from '@/api'

const cart = useCartStore()
const router = useRouter()
const toast = inject('toast')

const form = ref({ shipping_address: '', notes: '', payment_method: 'transfer' })
const loading = ref(false)
const error = ref('')
const success = ref(false)

const paymentMethods = [
  { value: 'transfer', label: 'Transfer Bank', icon: '🏦' },
  { value: 'gopay', label: 'GoPay', icon: '💚' },
  { value: 'ovo', label: 'OVO', icon: '💜' },
  { value: 'qris', label: 'QRIS', icon: '📱' },
]

function formatPrice(p) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p)
}

async function handleCheckout() {
  if (!form.value.shipping_address.trim()) { error.value = 'Alamat pengiriman wajib diisi'; return }
  loading.value = true; error.value = ''
  try {
    await ordersApi.checkout(form.value)
    cart.reset()
    success.value = true
    toast('Pesanan berhasil dibuat!', 'success')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Checkout gagal, coba lagi'
  } finally { loading.value = false }
}

onMounted(() => cart.fetchCart())
</script>

<style scoped>
.shopee-checkout-page { background: var(--bg-primary); padding: 130px 0 60px; min-height: 100vh; }
.checkout-layout { display: flex; flex-direction: column; gap: 24px; }

.shopee-card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border); padding: 24px; transition: var(--transition); }
.card-title { font-size: 1.1rem; color: var(--text-primary); font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
.icon-pin { color: var(--text-primary); font-size: 1.2rem; }

.address-card { border-top: 1px solid var(--border); }
.address-input { border: 1px solid var(--border); border-radius: var(--radius-md); font-size: 1rem; padding: 16px; background: white; resize: none; width: 100%; transition: var(--transition); }
.address-input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--border); }

.products-card { padding: 0; }
.shopee-cart-header {
  display: flex; align-items: center; padding: 16px 24px;
  font-size: 0.95rem; color: var(--text-secondary); border-bottom: 1px solid var(--border); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
}
.shopee-cart-items { padding: 0 24px; }
.shopee-cart-item {
  display: flex; align-items: center; padding: 24px 0; border-bottom: 1px solid var(--border);
}
.col-product { flex: 4; display: flex; align-items: center; gap: 16px; }
.col-price { flex: 2; text-align: center; color: var(--text-primary); font-size: 1rem; }
.col-qty { flex: 2; text-align: center; color: var(--text-primary); font-size: 1rem; }
.col-total { flex: 2; text-align: right; color: var(--text-primary); font-weight: 600; font-size: 1rem; }

.item-img { width: 48px; height: 48px; object-fit: cover; border: 1px solid var(--border); border-radius: var(--radius-md); }
.item-info { flex: 1; }
.item-name { font-size: 1rem; color: var(--text-primary); font-weight: 500; }

.notes-row { display: flex; align-items: center; padding: 24px; background: transparent; border-top: 1px solid var(--border); gap: 16px; }
.notes-row label { font-size: 0.95rem; font-weight: 500; color: var(--text-primary); }
.notes-input { flex: 1; max-width: 400px; padding: 10px 16px; border: 1px solid var(--border); border-radius: var(--radius-md); font-size: 0.95rem; background: white; transition: var(--transition); }
.notes-input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--border); }

.payment-options { display: flex; flex-wrap: wrap; gap: 16px; }
.payment-option {
  position: relative; display: flex; align-items: center; justify-content: center;
  padding: 12px 24px; border: 1px solid var(--border); border-radius: var(--radius-md);
  cursor: pointer; font-size: 0.95rem; font-weight: 500; color: var(--text-primary); min-width: 140px; transition: var(--transition);
  background: white;
}
.payment-option:hover { border-color: var(--text-primary); background: var(--bg-card-hover); }
.payment-option.active { border-color: var(--accent); background: var(--accent); color: white; }
.active-mark { display: none; }

.shopee-checkout-footer {
  background: white; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);
  margin-top: 24px; border: 1px solid var(--border); transition: var(--transition);
}
.footer-summary { padding: 32px 32px 0; display: flex; flex-direction: column; align-items: flex-end; gap: 16px; border-bottom: 1px solid var(--border); padding-bottom: 32px; }
.summary-line { display: flex; justify-content: space-between; width: 340px; font-size: 0.95rem; color: var(--text-secondary); }
.total-line { margin-top: 16px; align-items: center; }
.final-total { font-size: 2rem; color: var(--text-primary); font-weight: 700; }

.footer-actions { padding: 32px; display: flex; justify-content: flex-end; align-items: center; gap: 24px; background: transparent; }
.place-order-btn { padding: 0 40px; height: 56px; line-height: 56px; font-size: 1.1rem; font-weight: 600; border-radius: var(--radius-md); }
.shopee-btn-buy { background: var(--text-primary); color: white; border: none; cursor: pointer; display: inline-block; text-align: center; transition: var(--transition); }
.shopee-btn-buy:hover { background: black; transform: translateY(-2px); box-shadow: var(--shadow-sm); }
.shopee-btn-buy:disabled { background: var(--text-muted); cursor: not-allowed; transform: none; box-shadow: none; }

.error-msg { color: var(--danger); font-size: 0.95rem; font-weight: 500; }

.success-screen { text-align: center; padding: 100px 0; background: white; margin-top: 24px; border-radius: var(--radius-lg); border: 1px solid var(--border); }
.success-icon { font-size: 5rem; margin-bottom: 32px; }
.success-screen h2 { font-size: 2rem; font-weight: 700; margin-bottom: 16px; color: var(--text-primary); letter-spacing: -0.02em; }
.success-actions { display: flex; justify-content: center; gap: 16px; margin-top: 48px; }
.btn-outline { border: 1px solid var(--border); padding: 16px 32px; border-radius: var(--radius-md); font-weight: 600; color: var(--text-primary); transition: var(--transition); }
.btn-outline:hover { background: var(--bg-card-hover); border-color: var(--text-primary); }
.success-actions .shopee-btn-buy { padding: 16px 32px; line-height: normal; height: auto; border-radius: var(--radius-md); }

@media (max-width: 768px) {
  .shopee-cart-header { display: none; }
  .shopee-cart-item { flex-direction: column; align-items: flex-start; gap: 12px; }
  .col-product, .col-price, .col-qty, .col-total { width: 100%; text-align: left; }
  .footer-summary { align-items: stretch; padding: 24px; }
  .summary-line { width: 100%; }
}
</style>
