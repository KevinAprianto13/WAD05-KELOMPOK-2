<template>
  <NavBar />
  <div class="page">
    <div class="container">
      <div class="products-layout">
        <!-- Sidebar Filters -->
        <aside class="sidebar">
          <div class="filter-group">
            <label>Kategori</label>
            <div class="category-list">
              <div class="cat-item" :class="{ active: filters.category_id === '' }" @click="setCategory('')">Semua Kategori</div>
              <div class="cat-item" v-for="cat in categories" :key="cat.id" :class="{ active: filters.category_id === cat.id }" @click="setCategory(cat.id)">
                {{ cat.name }}
              </div>
            </div>
          </div>

          <div class="filter-group">
            <label>Batas Harga</label>
            <div class="price-filters">
              <input id="filter-min-price" v-model="filters.min_price" type="number" class="form-input" placeholder="MIN" @change="fetchProducts" />
              <span class="price-separator">-</span>
              <input id="filter-max-price" v-model="filters.max_price" type="number" class="form-input" placeholder="MAX" @change="fetchProducts" />
            </div>
          </div>

          <button class="shopee-btn-outline" @click="clearFilters">Hapus</button>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
          <div class="results-info" v-if="!loading">
            <span v-if="filters.search">Hasil pencarian untuk '{{ filters.search }}'</span>
            <span v-else>Menampilkan <strong>{{ products.length }}</strong> produk</span>
          </div>

          <div v-if="loading" class="loading-center"><div class="spinner"></div></div>
          <div v-else-if="products.length === 0" class="empty-state">
            <div class="icon">📦</div>
            <h3>Produk tidak ditemukan</h3>
            <p>Coba sesuaikan filter pencarian kamu.</p>
          </div>
          <div v-else class="shopee-product-grid">
            <ProductCard v-for="p in products" :key="p.id" :product="p" />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import ProductCard from '@/components/ProductCard.vue'
import { productsApi, categoriesApi } from '@/api'

const route = useRoute()
const products = ref([])
const categories = ref([])
const loading = ref(false)

const filters = reactive({
  search: route.query.q || '',
  category_id: route.query.category || '',
  min_price: '',
  max_price: '',
})

watch(() => route.query, (query) => {
  filters.search = query.q || ''
  if (query.category !== undefined) {
    filters.category_id = query.category
  }
  fetchProducts()
})

let debounceTimer = null
function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchProducts, 400)
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = {}
    if (filters.search) params.search = filters.search
    if (filters.category_id) params.category_id = filters.category_id
    if (filters.min_price) params.min_price = filters.min_price
    if (filters.max_price) params.max_price = filters.max_price
    const { data } = await productsApi.list(params)
    products.value = data
  } finally {
    loading.value = false
  }
}

function clearFilters() {
  filters.search = ''
  filters.category_id = ''
  filters.min_price = ''
  filters.max_price = ''
  fetchProducts()
}

function setCategory(id) {
  filters.category_id = id
  fetchProducts()
}

onMounted(async () => {
  const [, catRes] = await Promise.all([fetchProducts(), categoriesApi.list()])
  categories.value = catRes.data
})
</script>

<style scoped>
.products-page { background: var(--bg-primary); padding: 130px 0 60px; min-height: 100vh; }
.products-layout { display: grid; grid-template-columns: 240px 1fr; gap: 32px; align-items: start; }

/* Filter Sidebar */
.sidebar { display: flex; flex-direction: column; gap: 32px; position: sticky; top: 90px; }
.filter-group { margin-bottom: 8px; }
.filter-group label { font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin-bottom: 16px; display: block; border-bottom: 1px solid var(--border); padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }

.search-wrap { position: relative; width: 100%; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-muted); }
.search-input { width: 100%; padding: 10px 12px 10px 36px; background: white; border-radius: var(--radius-md); border: 1px solid var(--border); transition: var(--transition); }
.search-input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--border); }

.category-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.cat-item { display: flex; align-items: center; gap: 8px; cursor: pointer; color: var(--text-secondary); font-size: 0.95rem; padding: 4px 0; transition: var(--transition); }
.cat-item:hover { color: var(--text-primary); transform: translateX(4px); }
.cat-item.active { color: var(--text-primary); font-weight: 600; }

.price-filters { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.price-filters .form-input { width: 100%; background: white; border-radius: var(--radius-md); padding: 8px 12px; font-size: 0.85rem; border: 1px solid var(--border); transition: var(--transition); }
.price-filters .form-input:focus { border-color: var(--accent); }
.price-separator { color: var(--text-muted); }
.shopee-btn-outline {
  width: 100%; background: white; color: var(--text-primary); padding: 8px 0;
  border: 1px solid var(--border); border-radius: var(--radius-md); font-size: 0.9rem; font-weight: 600;
  cursor: pointer; transition: var(--transition);
}
.shopee-btn-outline:hover { background: var(--bg-card-hover); border-color: var(--text-primary); }

/* Main Content */
.main-content { flex: 1; min-width: 0; }
.results-info {
  margin-bottom: 24px; font-size: 0.95rem; color: var(--text-primary);
  display: flex; align-items: center; background: transparent; padding: 0;
}

.shopee-product-grid {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px;
}

@media (max-width: 1200px) { .shopee-product-grid { grid-template-columns: repeat(4, 1fr); } }
@media (max-width: 992px) { .products-layout { grid-template-columns: 200px 1fr; } .shopee-product-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) {
  .products-layout { grid-template-columns: 1fr; }
  .sidebar { position: static; gap: 16px; }
  .shopee-product-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) { .shopee-product-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
