<template>
  <NavBar />
  <div class="page shopee-detail-page">
    <div class="container" v-if="loading"><div class="loading-center"><div class="spinner"></div></div></div>
    <div class="container" v-else-if="product">
      <div class="shopee-breadcrumb">
        <RouterLink to="/">Shopee</RouterLink> > 
        <RouterLink to="/products">Produk</RouterLink> > 
        <span v-if="product.category">{{ product.category.name }} > </span>
        <span>{{ product.name }}</span>
      </div>

      <div class="shopee-detail-card">
        <!-- Image -->
        <div class="detail-img-col" @touchstart="startSwipe" @touchend="endSwipe">
          <button v-if="gallery.length > 1" class="gallery-arrow gallery-prev" aria-label="Gambar sebelumnya" @click="previousImage">‹</button>
          <img :src="gallery[selectedImage]" :alt="`${product.name} - gambar ${selectedImage + 1}`" class="detail-img" />
          <button v-if="gallery.length > 1" class="gallery-arrow gallery-next" aria-label="Gambar berikutnya" @click="nextImage">›</button>
          <div v-if="gallery.length > 1" class="gallery-controls">
            <button v-for="(image, index) in gallery" :key="image" class="gallery-thumb" :class="{ active: selectedImage === index }" :aria-label="`Pilih gambar ${index + 1}`" @click="selectedImage = index"><img :src="image" :alt="`Thumbnail ${index + 1}`" /></button>
          </div>
        </div>

        <!-- Info -->
        <div class="detail-info-col">
          <h1 class="shopee-product-title">{{ product.name }}</h1>
          
          <div class="shopee-price-box">
            <div class="detail-price">{{ formatPrice(product.price) }}</div>
          </div>

          <div class="shopee-detail-row">
            <label>Pengiriman</label>
            <div>Gratis Ongkir</div>
          </div>

          <!-- Qty selector -->
          <div class="shopee-detail-row" v-if="product.stock > 0">
            <label>Kuantitas</label>
            <div class="qty-control">
              <button class="qty-btn" id="qty-minus" @click="qty = Math.max(1, qty - 1)">−</button>
              <input type="number" class="qty-input" v-model="qty" id="qty-value" min="1" :max="product.stock" />
              <button class="qty-btn" id="qty-plus" @click="qty = Math.min(product.stock, qty + 1)">+</button>
            </div>
            <span class="stock-text">Tersisa {{ product.stock }} buah</span>
          </div>
          <div class="shopee-detail-row" v-else>
            <label>Kuantitas</label>
            <span class="stock-text error">Habis Terjual</span>
          </div>

          <div class="shopee-actions">
            <button
              class="shopee-btn-add"
              id="add-to-cart-detail"
              :disabled="product.stock === 0 || adding"
              @click="handleAddToCart"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13l-1.5 7h13M7 13L5.4 5M10 21a1 1 0 100-2 1 1 0 000 2zm7 0a1 1 0 100-2 1 1 0 000 2z"/>
              </svg>
              {{ adding ? 'Menambahkan...' : 'Masukkan Keranjang' }}
            </button>
            <button class="shopee-btn-buy" :disabled="product.stock === 0" @click="handleAddToCart">Beli Sekarang</button>
          </div>
        </div>
      </div>

      <!-- Description -->
      <div class="shopee-desc-card mt-4">
        <div class="desc-header">Spesifikasi & Deskripsi Produk</div>
        <div class="desc-content">{{ product.description || 'Tidak ada deskripsi.' }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { productsApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()
const toast = inject('toast')

const product = ref(null)
const loading = ref(false)
const qty = ref(1)
const adding = ref(false)
const selectedImage = ref(0)
const touchStartX = ref(0)
const gallery = computed(() => {
  const urls = [product.value?.image_url, ...(product.value?.images || []).map(image => image.image_url)]
  return [...new Set(urls.filter(Boolean))].length ? [...new Set(urls.filter(Boolean))] : ['/placeholder.jpg']
})

function formatPrice(p) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p)
}

function nextImage() { selectedImage.value = (selectedImage.value + 1) % gallery.value.length }
function previousImage() { selectedImage.value = (selectedImage.value - 1 + gallery.value.length) % gallery.value.length }
function startSwipe(event) { touchStartX.value = event.changedTouches[0].clientX }
function endSwipe(event) {
  const distance = event.changedTouches[0].clientX - touchStartX.value
  if (Math.abs(distance) < 40 || gallery.value.length < 2) return
  distance < 0 ? nextImage() : previousImage()
}

async function handleAddToCart() {
  if (!auth.isLoggedIn) { router.push('/login'); return }
  adding.value = true
  try {
    await cart.addItem(product.value.id, qty.value)
    toast(`${product.value.name} ditambahkan ke keranjang!`, 'success')
  } catch (e) {
    toast(e.response?.data?.detail || 'Gagal menambahkan', 'error')
  } finally {
    adding.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await productsApi.get(route.params.id)
    product.value = data
  } catch { router.push('/products') }
  finally { loading.value = false }
})
</script>

<style scoped>
.shopee-detail-page { min-height: 100vh; padding: 112px 0 64px; background: var(--bg-primary); }
.shopee-breadcrumb { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-bottom: 18px; color: var(--text-muted); font-size: .82rem; }
.shopee-breadcrumb a { color: var(--accent); font-weight: 600; }
.shopee-breadcrumb a:hover { text-decoration: underline; }
.shopee-detail-card { display: grid; grid-template-columns: minmax(360px, 46%) 1fr; overflow: hidden; margin-bottom: 22px; border: 1px solid var(--border); border-radius: 18px; background: white; box-shadow: var(--shadow-md); }
.detail-img-col { position: relative; min-height: 510px; padding: 32px 56px 104px; display: flex; align-items: center; justify-content: center; border-right: 1px solid var(--border); background: linear-gradient(145deg, #f8fafc, #eef2ff); touch-action: pan-y; }
.detail-img { width: 100%; height: 450px; object-fit: contain; mix-blend-mode: multiply; user-select: none; }
.gallery-arrow { position: absolute; top: 50%; z-index: 2; width: 36px; height: 36px; transform: translateY(-50%); border: 1px solid var(--border); border-radius: 50%; color: var(--text-primary); background: rgba(255,255,255,.9); font-size: 1.8rem; line-height: 1; box-shadow: var(--shadow-sm); }
.gallery-arrow:hover { color: var(--accent); border-color: var(--accent); }
.gallery-prev { left: 16px; }
.gallery-next { right: 16px; }
.gallery-controls { position: absolute; right: 32px; bottom: 22px; left: 32px; display: flex; justify-content: center; gap: 8px; overflow-x: auto; }
.gallery-thumb { width: 52px; height: 52px; flex: 0 0 auto; overflow: hidden; padding: 0; border: 2px solid transparent; border-radius: 7px; background: white; opacity: .65; }
.gallery-thumb.active { border-color: var(--accent); opacity: 1; box-shadow: 0 0 0 2px var(--accent-glow); }
.gallery-thumb img { width: 100%; height: 100%; object-fit: cover; }
.detail-info-col { display: flex; flex-direction: column; padding: 38px 42px; }
.shopee-product-title { max-width: 650px; margin-bottom: 20px; color: var(--text-primary); font-size: clamp(1.8rem, 3vw, 2.7rem); line-height: 1.14; letter-spacing: -.035em; }
.shopee-price-box { margin: 0 -42px 26px; padding: 18px 42px; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); background: #fbfcff; }
.detail-price { color: var(--accent); font-size: 2rem; font-weight: 800; letter-spacing: -.03em; }
.shopee-detail-row { display: grid; grid-template-columns: 112px 1fr; align-items: center; gap: 16px; margin-bottom: 18px; color: var(--text-secondary); font-size: .92rem; }
.shopee-detail-row > label { color: var(--text-muted); }
.qty-control { width: fit-content; display: flex; align-items: center; overflow: hidden; border: 1px solid var(--border); border-radius: 8px; background: white; }
.qty-btn { width: 38px; height: 36px; color: var(--text-secondary); background: white; font-size: 1.1rem; }
.qty-btn:hover { color: var(--accent); background: var(--accent-light); }
.qty-input { width: 48px; height: 36px; border: 0; border-right: 1px solid var(--border); border-left: 1px solid var(--border); color: var(--text-primary); text-align: center; font-weight: 700; }
.qty-input::-webkit-inner-spin-button, .qty-input::-webkit-outer-spin-button { appearance: none; }
.stock-text { grid-column: 2; margin-top: -10px; color: var(--text-muted); font-size: .8rem; }
.stock-text.error { grid-column: 2; margin: 0; color: var(--danger); font-weight: 700; }
.shopee-actions { display: flex; gap: 12px; margin-top: auto; padding-top: 22px; }
.shopee-btn-add, .shopee-btn-buy { min-height: 48px; padding: 0 20px; border-radius: 9px; font-weight: 700; font-size: .9rem; transition: var(--transition-bounce); }
.shopee-btn-add { display: inline-flex; align-items: center; justify-content: center; gap: 9px; flex: 1; color: var(--accent); border: 1px solid var(--accent); background: var(--accent-light); }
.shopee-btn-add:hover:not(:disabled) { color: white; background: var(--accent); transform: translateY(-2px); }
.shopee-btn-buy { flex: 1; color: white; background: var(--accent-gradient); box-shadow: 0 5px 14px var(--accent-glow); }
.shopee-btn-buy:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 18px var(--accent-glow); }
.shopee-btn-add:disabled, .shopee-btn-buy:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }
.shopee-desc-card { padding: 28px 32px; border: 1px solid var(--border); border-radius: 14px; background: white; box-shadow: var(--shadow-sm); }
.desc-header { margin-bottom: 14px; color: var(--text-primary); font-size: 1.05rem; font-weight: 800; }
.desc-content { color: var(--text-secondary); font-size: .9rem; line-height: 1.8; white-space: pre-wrap; }
@media (max-width: 900px) { .shopee-detail-card { grid-template-columns: 1fr; } .detail-img-col { min-height: 360px; border-right: 0; border-bottom: 1px solid var(--border); } .detail-img { height: 330px; } .detail-info-col { padding: 28px; } .shopee-price-box { margin-right: -28px; margin-left: -28px; padding-right: 28px; padding-left: 28px; } }
@media (max-width: 560px) { .shopee-detail-page { padding-top: 92px; } .detail-img-col { min-height: 280px; padding: 18px 44px 82px; } .detail-img { height: 260px; } .gallery-controls { right: 18px; bottom: 14px; left: 18px; } .gallery-thumb { width: 44px; height: 44px; } .detail-info-col { padding: 22px 18px; } .shopee-product-title { font-size: 1.7rem; } .shopee-price-box { margin-right: -18px; margin-left: -18px; padding-right: 18px; padding-left: 18px; } .shopee-detail-row { grid-template-columns: 92px 1fr; } .shopee-actions { flex-direction: column; } .shopee-desc-card { padding: 22px 18px; } }
</style>
