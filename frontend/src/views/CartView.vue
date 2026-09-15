<template>
  <NavBar />
  <div class="page shopee-cart-page">
    <div class="container">
      <div v-if="cart.loading" class="loading-center"><div class="spinner"></div></div>

      <div v-else-if="cart.items.length === 0" class="empty-state card mt-4">
        <div class="icon">🛒</div>
        <h3>Keranjang belanjamu kosong</h3>
        <RouterLink to="/products" class="btn btn-outline" style="margin-top:24px" id="cart-go-shop">Belanja Sekarang</RouterLink>
      </div>

      <div v-else class="shopee-cart-container mt-4">
        <!-- Header -->
        <div class="shopee-cart-header">
          <div class="col-product">Produk</div>
          <div class="col-price">Harga Satuan</div>
          <div class="col-qty">Kuantitas</div>
          <div class="col-total">Total Harga</div>
          <div class="col-action">Aksi</div>
        </div>

        <!-- Items -->
        <div class="shopee-cart-items">
          <div v-for="item in cart.items" :key="item.id" class="shopee-cart-item" :id="`cart-item-${item.id}`">
            <div class="col-product">
              <img :src="item.product.image_url || '/placeholder.jpg'" :alt="item.product.name" class="item-img" />
              <div class="item-info">
                <RouterLink :to="`/products/${item.product.id}`" class="item-name">{{ item.product.name }}</RouterLink>
                <div class="item-category text-muted" v-if="item.product.category">Kategori: {{ item.product.category.name }}</div>
              </div>
            </div>
            <div class="col-price">{{ formatPrice(item.product.price) }}</div>
            <div class="col-qty">
              <div class="qty-control">
                <button class="qty-btn" :id="`item-minus-${item.id}`" @click="changeQty(item, item.quantity - 1)">−</button>
                <span class="qty-val">{{ item.quantity }}</span>
                <button class="qty-btn" :id="`item-plus-${item.id}`" @click="changeQty(item, item.quantity + 1)" :disabled="item.quantity >= item.product.stock">+</button>
              </div>
            </div>
            <div class="col-total price">{{ formatPrice(item.product.price * item.quantity) }}</div>
            <div class="col-action">
              <button class="btn-remove" :id="`item-remove-${item.id}`" @click="cart.removeItem(item.id)">Hapus</button>
            </div>
          </div>
        </div>

        <!-- Sticky Footer -->
        <div class="shopee-cart-footer">
          <div class="footer-left">
            <button class="btn-remove" @click="cart.clearCart()" id="cart-clear-btn">Kosongkan Keranjang</button>
          </div>
          <div class="footer-right">
            <div class="footer-total-text">Total ({{ cart.itemCount }} produk): </div>
            <div class="footer-total-price">{{ formatPrice(cart.total) }}</div>
            <RouterLink to="/checkout" class="shopee-btn-checkout" id="cart-checkout-btn">Checkout</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

function formatPrice(p) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p)
}

async function changeQty(item, qty) {
  if (qty < 1) { await cart.removeItem(item.id) }
  else { await cart.updateItem(item.id, qty) }
}

onMounted(() => cart.fetchCart())
</script>

<style scoped>
.shopee-cart-page { background: var(--bg-primary); padding: 130px 0 60px; min-height: 100vh; }
.mt-4 { margin-top: 24px; }

.shopee-cart-header {
  display: flex; align-items: center; background: white; padding: 16px 20px;
  border-radius: var(--radius-md); border: 1px solid var(--border); margin-bottom: 12px;
  font-size: 0.95rem; color: var(--text-secondary); text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;
}

.shopee-cart-card { 
  background: white; 
  border-radius: var(--radius-lg); 
  border: 1px solid var(--border); 
  margin-bottom: 16px; 
  padding: 0 20px;
}
.shopee-cart-item {
  display: flex; align-items: center; padding: 24px 0; border-bottom: 1px solid var(--border);
}
.shopee-cart-item:last-child { border-bottom: none; }

.col-product { flex: 4; display: flex; align-items: center; gap: 16px; }
.col-price { flex: 2; text-align: center; color: var(--text-primary); font-size: 1rem; }
.col-qty { flex: 2; display: flex; justify-content: center; }
.col-total { flex: 2; text-align: center; color: var(--text-primary); font-weight: 600; font-size: 1rem; }
.col-action { flex: 1; text-align: center; }

.item-img { width: 80px; height: 80px; object-fit: cover; border: 1px solid var(--border); border-radius: var(--radius-md); transition: var(--transition); }
.shopee-cart-item:hover .item-img { transform: scale(1.03); }
.item-info { display: flex; flex-direction: column; gap: 4px; }
.item-name { font-size: 1rem; font-weight: 500; color: var(--text-primary); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; }
.item-name:hover { color: var(--accent); }
.item-category { font-size: 0.85rem; color: var(--text-muted); }

.qty-control { display: flex; align-items: center; border: 1px solid var(--border); border-radius: var(--radius-md); overflow: hidden; }
.qty-btn { width: 32px; height: 32px; background: white; border: none; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
.qty-btn:hover:not(:disabled) { background: var(--bg-card-hover); }
.qty-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.qty-val { width: 40px; text-align: center; border-left: 1px solid var(--border); border-right: 1px solid var(--border); font-size: 0.95rem; line-height: 32px; }

.btn-remove { background: none; border: none; color: var(--text-secondary); font-size: 0.95rem; font-weight: 500; cursor: pointer; transition: color 0.2s; }
.btn-remove:hover { color: var(--danger); }

.shopee-cart-footer {
  position: sticky; bottom: 0; background: white;
  display: flex; align-items: center; justify-content: flex-end; gap: 24px;
  padding: 24px; margin-top: 24px;
  box-shadow: 0 -4px 12px rgba(0,0,0,0.02); border-radius: var(--radius-lg);
  border: 1px solid var(--border); z-index: 10;
}
.footer-left { display: flex; align-items: center; margin-right: auto; }
.footer-right { display: flex; align-items: center; gap: 24px; }
.footer-total-text { font-size: 1rem; color: var(--text-secondary); }
.footer-total-price { font-size: 1.5rem; color: var(--text-primary); font-weight: 700; }
.shopee-btn-checkout {
  background: var(--text-primary); color: white; padding: 0 40px;
  line-height: 48px; border-radius: var(--radius-md); font-size: 1.05rem; font-weight: 600;
  cursor: pointer; border: none; transition: var(--transition);
}
.shopee-btn-checkout:hover { background: black; transform: translateY(-2px); box-shadow: var(--shadow-sm); }

@media (max-width: 900px) {
  .shopee-cart-header { display: none; }
  .shopee-cart-item { flex-direction: column; align-items: flex-start; gap: 16px; position: relative; }
  .col-product, .col-price, .col-qty, .col-total, .col-action { width: 100%; text-align: left; justify-content: flex-start; }
  .col-action { position: absolute; right: 0; bottom: 24px; width: auto; }
  .footer-right { flex-direction: column; align-items: flex-end; gap: 12px; }
}
</style>
