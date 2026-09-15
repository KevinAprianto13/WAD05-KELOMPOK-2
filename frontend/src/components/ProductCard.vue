<template>
  <div class="product-card glass" @click="$router.push(`/products/${product.id}`)">
    
    <div class="product-img-wrap">
      <img v-if="imageSrc" :src="imageSrc" :alt="product.name" class="product-img" loading="lazy" @error="handleImageError" />
      <div v-else class="product-image-placeholder" aria-label="Gambar produk tidak tersedia">
        <svg xmlns="http://www.w3.org/2000/svg" width="42" height="42" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.4">
          <path stroke-linecap="round" stroke-linejoin="round" d="m3 16 5-5 4 4 2-2 7 7M14 8h.01M5 21h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2Z" />
        </svg>
        <span>Gambar belum tersedia</span>
      </div>
      
      <!-- Overlay gradients on hover -->
      <div class="img-overlay"></div>

      <!-- Badges -->
      <div class="badges-container">
        <div class="badge badge-pending" v-if="product.stock > 0 && product.stock <= 5">Sisa {{product.stock}}!</div>
        <div class="badge badge-cancelled" v-if="product.stock === 0">Habis</div>
      </div>
      
      <!-- Quick Actions (Hover) -->
      <div class="quick-actions">
        <button class="action-btn" title="Lihat Detail">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </button>
      </div>
    </div>
    
    <div class="product-body">
      <div class="product-category">Kategori Utama</div>
      <h3 class="product-name">{{ product.name }}</h3>
      
      <div class="rating-row">
        <span class="stars">
          <svg v-for="i in 5" :key="i" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="14" height="14" style="color: #f59e0b; display: inline-block;">
            <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z" clip-rule="evenodd" />
          </svg>
        </span>
        <span class="sold-count">({{ Math.floor(Math.random() * 200) + 10 }} Terjual)</span>
      </div>

      <div class="product-footer">
        <span class="price gradient-text">{{ formatPrice(product.price) }}</span>
        
        <!-- Cart Button -->
        <button
          class="btn-cart-add"
          :class="{ 'adding': adding }"
          :disabled="product.stock === 0 || adding"
          @click.stop="handleAddToCart"
        >
          <svg v-if="!adding" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          <div v-else class="spinner-mini"></div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'

const props = defineProps({ product: Object })
const auth = useAuthStore()
const cart = useCartStore()
const router = useRouter()
const toast = inject('toast')
const adding = ref(false)
const imageSrc = ref(props.product?.image_url || '')

function handleImageError() {
  imageSrc.value = ''
}

function formatPrice(p) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p)
}

async function handleAddToCart() {
  if (!auth.isLoggedIn) { router.push('/login'); return }
  adding.value = true
  try {
    await cart.addItem(props.product.id)
    toast('Berhasil ditambahkan ke keranjang!', 'success')
  } catch (e) {
    toast(e.response?.data?.detail || 'Gagal menambahkan produk', 'error')
  } finally {
    adding.value = false
  }
}
</script>

<style scoped>
.product-card {
  cursor: pointer; 
  display: flex; flex-direction: column;
  background: white; border-radius: var(--radius-xl);
  border: 1px solid var(--border);
  transition: var(--transition-bounce);
  overflow: hidden;
  position: relative;
}
.product-card:hover { 
  border-color: var(--accent-light); 
  box-shadow: var(--shadow-hover); 
  transform: translateY(-8px); 
}

/* Image Area */
.product-img-wrap { 
  position: relative; overflow: hidden; aspect-ratio: 1/1; 
  background: var(--bg-secondary);
}
.product-img { 
  width: 100%; height: 100%; object-fit: cover; 
  transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1); 
}
.product-image-placeholder { width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: #94a3b8; background: linear-gradient(145deg, #f8fafc, #e2e8f0); font-size: .72rem; font-weight: 600; text-align: center; }
.product-card:hover .product-img { transform: scale(1.08); }

.img-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.3) 0%, transparent 40%);
  opacity: 0; transition: var(--transition);
}
.product-card:hover .img-overlay { opacity: 1; }

.badges-container {
  position: absolute; top: 12px; left: 12px;
  display: flex; flex-direction: column; gap: 6px;
}

/* Hover Quick Actions */
.quick-actions {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -30%);
  opacity: 0; transition: var(--transition-bounce);
  display: flex; gap: 10px;
}
.product-card:hover .quick-actions { opacity: 1; transform: translate(-50%, -50%); }

.action-btn {
  background: rgba(255,255,255,0.9); backdrop-filter: blur(4px);
  border-radius: 50%; width: 44px; height: 44px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-primary); transition: var(--transition);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.action-btn:hover { background: var(--accent); color: white; transform: scale(1.1); }

/* Body Area */
.product-body { padding: 20px; display: flex; flex-direction: column; flex: 1; gap: 8px; }

.product-category { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }

.product-name {
  font-size: 1.05rem; line-height: 1.4; color: var(--text-primary); font-weight: 700;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis;
  min-height: 2.8em; margin: 0;
}

.rating-row { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; font-size: 0.8rem; }
.stars { display: flex; align-items: center; gap: 2px; }
.sold-count { color: var(--text-muted); font-weight: 500; margin-left: 4px; white-space: nowrap; }

.product-footer { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: auto; padding-top: 12px; }
.price { white-space: nowrap; font-size: 1.05rem; line-height: 1.2; letter-spacing: -0.02em; }

/* Add Button */
.btn-cart-add {
  flex-shrink: 0;
  width: 44px; height: 44px; border-radius: var(--radius-lg);
  background: var(--bg-secondary); color: var(--accent);
  border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  transition: var(--transition-bounce);
}
.product-card:hover .btn-cart-add:not(:disabled) {
  background: var(--accent-gradient); color: white; border-color: transparent;
  box-shadow: 0 4px 12px var(--accent-glow);
}
.btn-cart-add:active { transform: scale(0.9); }
.btn-cart-add:disabled { opacity: 0.5; background: var(--bg-secondary); color: var(--text-muted); cursor: not-allowed; }

.spinner-mini {
  width: 20px; height: 20px; border-radius: 50%;
  border: 2px solid white; border-top-color: transparent;
  animation: spin 0.8s linear infinite;
}

/* Mobile Optimizations */
@media (max-width: 480px) {
  .product-body { padding: 12px; gap: 4px; }
  .product-name { font-size: 0.95rem; min-height: 2.8em; }
  .price { font-size: 1rem; }
  .quick-actions { display: none; } /* Disable hover buttons on mobile */
  .btn-cart-add { width: 36px; height: 36px; border-radius: var(--radius-md); }
  .product-card:hover { transform: translateY(-4px); } /* Less lift on mobile */
}
</style>
