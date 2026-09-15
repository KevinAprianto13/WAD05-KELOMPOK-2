<template>
  <NavBar />
  <main class="shopee-main">
    
    <div class="container">
      
      <!-- Hero Banner Section (Modern Aesthetic) -->
      <section class="hero-section mt-main">
        <div class="hero-main glass">
          <div class="hero-content">
            <span class="badge badge-processing mb-2">Promo Spesial</span>
            <h1 class="hero-title">{{ mainBanner?.title || 'Belanja Cerdas, Gaya Hidup Modern.' }}</h1>
            <p class="hero-subtitle">{{ mainBanner?.subtitle || 'Temukan ribuan produk pilihan dengan harga terbaik dan gratis ongkir setiap hari.' }}</p>
            <button class="btn btn-primary btn-lg mt-4" @click="$router.push('/products')">Mulai Belanja</button>
          </div>
          <div class="hero-image-wrap">
             <img :src="mainBanner?.image_url || fallbackBanners.main" alt="Banner utama" class="hero-image" />
             <div class="hero-overlay"></div>
          </div>
        </div>

        <div class="hero-side">
          <div class="side-banner glass" @click="openBanner(sideBanners.side_1)">
            <img :src="sideBanners.side_1?.image_url || fallbackBanners.side_1" alt="Banner promo" class="side-img"/>
            <div class="side-content">
              <h4>{{ sideBanners.side_1?.title || 'Cashback 100RB' }}</h4>
              <p>{{ sideBanners.side_1?.subtitle || 'Belanja Puas!' }}</p>
            </div>
          </div>
          <div class="side-banner glass" @click="openBanner(sideBanners.side_2)">
            <img :src="sideBanners.side_2?.image_url || fallbackBanners.side_2" alt="Banner promo" class="side-img"/>
            <div class="side-content">
              <h4>{{ sideBanners.side_2?.title || 'Gratis Ongkir' }}</h4>
              <p>{{ sideBanners.side_2?.subtitle || 'Ke Seluruh Indonesia' }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Categories -->
      <section class="section">
        <div class="section-header">
          <h2>Kategori Pilihan</h2>
          <span class="text-muted">Temukan yang Anda cari</span>
        </div>
        <div class="categories-grid">
          <RouterLink
            v-for="(cat, index) in categories"
            :key="cat.slug"
            :to="`/products?category=${cat.id}`"
            class="category-card glass"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="cat-icon-wrap" v-html="catIcons[cat.slug] || defaultCatIcon"></div>
            <div class="cat-info">
              <div class="cat-name">{{ cat.name }}</div>
              <div class="cat-desc">Jelajahi Sekarang ➜</div>
            </div>
          </RouterLink>
        </div>
      </section>

      <!-- Daily Discover (Rekomendasi) -->
      <section class="section">
        <div class="section-header">
          <h2>Rekomendasi Spesial</h2>
          <span class="text-muted">Disesuaikan untuk Anda</span>
        </div>
        
        <div v-if="loading" class="loading-center">
          <div class="spinner"></div>
        </div>
        
        <div v-else class="product-grid">
          <ProductCard v-for="p in products" :key="p.id" :product="p" />
        </div>
        
        <div class="flex-center" style="margin-top: 48px;">
          <RouterLink to="/products" class="btn btn-primary btn-lg pulse-hover">Lihat Semua Produk</RouterLink>
        </div>
      </section>

    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import ProductCard from '@/components/ProductCard.vue'
import { productsApi, categoriesApi, bannersApi } from '@/api'

const products = ref([])
const categories = ref([])
const loading = ref(false)
const mainBanner = ref(null)
const sideBanners = ref({})
const fallbackBanners = {
  main: 'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?q=80&w=2070&auto=format&fit=crop',
  side_1: 'https://images.unsplash.com/photo-1556740738-b6a63e27c4df?q=80&w=2070&auto=format&fit=crop',
  side_2: 'https://images.unsplash.com/photo-1607082350899-7e105aa886ae?q=80&w=2070&auto=format&fit=crop',
}

function openBanner(banner) {
  if (banner?.link_url) window.open(banner.link_url, '_blank', 'noopener')
}

const catIcons = {
  'elektronik': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="28" height="28"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
  'fashion': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="28" height="28"><path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
  'rumah-dapur': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="28" height="28"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>',
  'olahraga': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="28" height="28"><path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
  'kecantikan': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="28" height="28"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
}
const defaultCatIcon = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="28" height="28"><path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>'

onMounted(async () => {
  loading.value = true
  try {
    const [prod, cat, banners] = await Promise.all([
      productsApi.list({ limit: 10 }), // Show 10 for better grid display (5x2 or 2x5)
      categoriesApi.list(),
      bannersApi.list(),
    ])
    products.value = prod.data
    categories.value = cat.data
    const activeBanners = Object.fromEntries(banners.data.map(banner => [banner.position, banner]))
    mainBanner.value = activeBanners.main || null
    sideBanners.value = activeBanners
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.shopee-main { min-height: 100vh; overflow-x: hidden; }
.mt-main { margin-top: 120px; }
.mb-2 { margin-bottom: 12px; }
.mt-4 { margin-top: 24px; }

/* ── Hero Section (Modern) ── */
.hero-section {
  display: flex; gap: 24px; height: 440px; margin-bottom: 40px;
}
.hero-main {
  flex: 2; border-radius: var(--radius-xl); overflow: hidden;
  display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(224,231,255,0.4));
  position: relative;
}
.hero-content { padding: 48px; z-index: 2; max-width: 50%; }
.hero-title { font-size: 2.8rem; margin-bottom: 16px; }
.hero-subtitle { font-size: 1.1rem; color: var(--text-secondary); line-height: 1.6; }

.hero-image-wrap { position: absolute; right: 0; top: 0; bottom: 0; width: 55%; clip-path: polygon(15% 0, 100% 0, 100% 100%, 0 100%); }
.hero-image { width: 100%; height: 100%; object-fit: cover; }
.hero-overlay { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(248,250,252,1) 0%, rgba(248,250,252,0) 100%); }

.hero-side { flex: 1; display: flex; flex-direction: column; gap: 24px; }
.side-banner { 
  flex: 1; border-radius: var(--radius-xl); overflow: hidden; position: relative;
  display: flex; align-items: flex-end; padding: 24px; cursor: pointer; transition: var(--transition-bounce);
}
.side-banner:hover { transform: translateY(-4px) scale(1.02); box-shadow: var(--shadow-hover); }
.side-img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; transition: var(--transition-slow); }
.side-banner:hover .side-img { transform: scale(1.1); }
.side-banner::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); z-index: 1; }
.side-content { position: relative; z-index: 2; color: white; }
.side-content h4 { font-size: 1.4rem; font-weight: 800; margin-bottom: 4px; }
.side-content p { font-size: 0.9rem; opacity: 0.9; }

/* ── Section Header ── */
.section-header { margin-bottom: 40px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 12px; }
.section-header h2 { display: inline-block; position: relative; margin: 0; }
.section-header h2::after {
  content: ''; position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%);
  width: 60px; height: 4px; background: var(--accent-gradient); border-radius: 4px;
}
.section-header .text-muted { margin-top: 4px; }

/* ── Categories Grid ── */
.categories-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
.category-card {
  display: flex; align-items: center; gap: 16px;
  padding: 20px; border-radius: var(--radius-lg);
  transition: var(--transition-bounce); cursor: pointer;
  animation: fadeUp 0.6s backwards;
}
.category-card:hover { transform: translateY(-6px); border-color: var(--accent-light); box-shadow: var(--shadow-hover); }

.cat-icon-wrap {
  width: 60px; height: 60px; border-radius: var(--radius-md);
  background: var(--accent-light); color: var(--accent);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; transition: var(--transition-bounce);
}
.category-card:hover .cat-icon-wrap { background: var(--accent-gradient); color: white; transform: rotate(-10deg) scale(1.1); }

.cat-info { display: flex; flex-direction: column; gap: 4px; }
.cat-name { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); }
.cat-desc { font-size: 0.8rem; font-weight: 600; color: var(--accent); opacity: 0; transform: translateX(-10px); transition: var(--transition); }
.category-card:hover .cat-desc { opacity: 1; transform: translateX(0); }

/* ── Product Grid ── */
.product-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 24px; }

/* Animations */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.pulse-hover:hover { animation: pulseBtn 1s infinite; }
@keyframes pulseBtn {
  0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4); }
  70% { box-shadow: 0 0 0 15px rgba(79, 70, 229, 0); }
  100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
}


/* ── Mobile Optimizations (Android Focused) ── */
@media (max-width: 1200px) {
  .product-grid { grid-template-columns: repeat(4, 1fr); }
}

@media (max-width: 992px) {
  .hero-section { height: 380px; }
  .hero-content { max-width: 60%; padding: 32px; }
  .hero-title { font-size: 2.2rem; }
  .product-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 768px) {
  .mt-main { margin-top: 80px; }
  .hero-section { flex-direction: column; height: auto; gap: 16px; }
  
  .hero-main { flex-direction: column; text-align: center; padding-bottom: 200px; }
  .hero-content { max-width: 100%; padding: 32px 24px; align-items: center; display: flex; flex-direction: column; }
  .hero-title { font-size: 2rem; }
  .hero-image-wrap { width: 100%; top: auto; height: 250px; clip-path: polygon(0 15%, 100% 0, 100% 100%, 0 100%); }
  .hero-overlay { background: linear-gradient(0deg, rgba(248,250,252,1) 0%, rgba(248,250,252,0) 100%); }

  .hero-side { flex-direction: row; height: 160px; }
  .side-content h4 { font-size: 1.1rem; }

  .product-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; }
  .categories-grid { grid-template-columns: repeat(1, 1fr); }
}

@media (max-width: 480px) {
  .hero-side { flex-direction: column; height: auto; }
  .side-banner { height: 140px; }
  .section { padding: 40px 0; }
  .section-header h2 { font-size: 1.6rem; }
}
</style>
