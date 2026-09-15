<template>
  <div>
    <!-- Desktop & Top Navbar -->
    <nav class="navbar modern-navbar glass" :class="{ 'scrolled': isScrolled }">
      <div class="container navbar-inner">
        
        <!-- Brand -->
        <RouterLink to="/" class="navbar-brand">
          <div class="brand-icon-wrap">
            <svg xmlns="http://www.w3.org/2000/svg" class="brand-icon" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2" width="24" height="24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <span class="brand-text gradient-text">NusaShop</span>
        </RouterLink>

        <!-- Search Bar (Desktop) -->
        <div v-if="showSearchBar" class="search-container desktop-only">
          <div class="search-bar">
            <svg xmlns="http://www.w3.org/2000/svg" class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input type="text" placeholder="Temukan produk impianmu..." class="nav-search-input" @keyup.enter="handleSearch" v-model="searchQuery" aria-label="Cari produk" />
            <button class="btn-search" @click="handleSearch">Cari</button>
          </div>
        </div>

        <!-- Actions (Desktop) -->
        <div class="navbar-actions desktop-only">
          <NotificationBell v-if="auth.isLoggedIn" />
          
          <RouterLink v-if="auth.isLoggedIn" to="/cart" class="cart-btn" id="nav-cart-btn">
            <div class="cart-icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <span v-if="cart.itemCount > 0" class="cart-badge bounce-in">{{ cart.itemCount }}</span>
            </div>
          </RouterLink>

          <template v-if="auth.isLoggedIn">
            <div class="user-menu" @click="showMenu = !showMenu" v-click-outside="() => showMenu = false">
              <div class="nav-username">
                <img :src="`https://ui-avatars.com/api/?name=${auth.user?.full_name}&background=4f46e5&color=fff`" class="avatar-sm" />
                <span>{{ auth.user?.full_name.split(' ')[0] }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </div>
              
              <!-- Dropdown Menu -->
              <transition name="dropdown-fade">
                <div v-if="showMenu" class="dropdown glass">
                  <div class="dropdown-header">
                    <p class="font-bold">{{ auth.user?.full_name }}</p>
                    <p class="text-sm text-muted">{{ auth.user?.email }}</p>
                  </div>
                  <div class="dropdown-divider"></div>
                  <RouterLink to="/orders" class="dropdown-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
                    Pesanan Saya
                  </RouterLink>
                  <RouterLink v-if="auth.isAdmin" to="/admin" class="dropdown-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                    Admin Dashboard
                  </RouterLink>
                  <div class="dropdown-divider"></div>
                  <button class="dropdown-item danger" @click="handleLogout">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                    Keluar
                  </button>
                </div>
              </transition>
            </div>
          </template>

          <template v-else>
            <div class="auth-links">
              <RouterLink to="/login" class="btn btn-outline btn-sm">Masuk</RouterLink>
              <RouterLink to="/register" class="btn btn-primary btn-sm">Daftar</RouterLink>
            </div>
          </template>
        </div>

      </div>
    </nav>

    <!-- Mobile Bottom Navigation -->
    <nav class="mobile-bottom-nav glass mobile-only">
      <RouterLink to="/" class="mobile-nav-item" exact-active-class="active">
        <svg xmlns="http://www.w3.org/2000/svg" class="mobile-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        <span>Beranda</span>
      </RouterLink>
      
      <RouterLink to="/products" class="mobile-nav-item" exact-active-class="active">
        <svg xmlns="http://www.w3.org/2000/svg" class="mobile-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <span>Cari</span>
      </RouterLink>

      <RouterLink v-if="auth.isLoggedIn" to="/cart" class="mobile-nav-item cart-mobile-nav" exact-active-class="active">
        <div class="cart-icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" class="mobile-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <span v-if="cart.itemCount > 0" class="cart-badge">{{ cart.itemCount }}</span>
        </div>
        <span>Keranjang</span>
      </RouterLink>

      <div v-if="auth.isLoggedIn" class="mobile-nav-item" @click="handleLogout">
        <svg xmlns="http://www.w3.org/2000/svg" class="mobile-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        <span>Keluar</span>
      </div>

      <RouterLink v-else to="/login" class="mobile-nav-item">
        <svg xmlns="http://www.w3.org/2000/svg" class="mobile-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
        </svg>
        <span>Masuk</span>
      </RouterLink>
    </nav>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import NotificationBell from '@/components/NotificationBell.vue'
import { useScroll } from '@vueuse/core'

const auth = useAuthStore()
const cart = useCartStore()
const router = useRouter()
const route = useRoute()
const showMenu = ref(false)
const searchQuery = ref('')
const { y } = useScroll(window)
const isScrolled = ref(false)
let searchTimer = null

const showSearchBar = computed(() => {
  return ['/', '/products'].includes(route.path)
})

watch(y, val => { isScrolled.value = val > 10 })

watch(() => route.query.q, value => {
  const query = value || ''
  if (query !== searchQuery.value) searchQuery.value = query
})

watch(searchQuery, value => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    const query = value.trim()
    if (route.path !== '/products' && !query) return
    const nextQuery = { ...route.query, q: query || undefined }
    router.replace({ path: '/products', query: nextQuery })
  }, 350)
})

const vClickOutside = {
  beforeMount(el, binding) {
    el.__clickOutsideHandler__ = (e) => {
      if (!el.contains(e.target)) binding.value(e)
    }
    document.addEventListener('click', el.__clickOutsideHandler__)
  },
  unmounted(el) {
    document.removeEventListener('click', el.__clickOutsideHandler__)
  }
}

function handleSearch() {
  clearTimeout(searchTimer)
  const query = searchQuery.value.trim()
  router.replace({ path: '/products', query: { ...route.query, q: query || undefined } })
}

function handleLogout() {
  auth.logout()
  cart.reset()
  router.push('/')
}
</script>

<style scoped>
/* ── Navbar Top (Desktop) ── */
.modern-navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  padding: 16px 0;
  border-bottom: 1px solid transparent;
  transition: var(--transition-slow);
}
.modern-navbar.scrolled {
  padding: 12px 0;
  border-bottom: 1px solid var(--border-glass);
  box-shadow: var(--shadow-sm);
}

.navbar-inner { display: flex; align-items: center; justify-content: space-between; gap: 40px; }

/* Brand */
.navbar-brand { display: flex; align-items: center; gap: 12px; }
.brand-icon-wrap {
  background: var(--accent-gradient);
  width: 40px; height: 40px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 12px var(--accent-glow);
}
.brand-icon { font-size: 1.4rem; }
.brand-text { font-size: 1.5rem; letter-spacing: -0.03em; }

/* Search Container */
.search-container { flex: 1; max-width: 600px; }
.search-bar { 
  display: flex; align-items: center;
  background: white; border-radius: var(--radius-round); padding: 4px;
  border: 1px solid var(--border); transition: var(--transition-bounce);
  box-shadow: var(--shadow-sm);
}
.search-bar:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-glow);
  transform: translateY(-1px);
}
.search-icon { font-size: 1.1rem; color: var(--text-muted); margin-left: 12px; margin-right: 8px; }
.nav-search-input {
  flex: 1; border: none; padding: 10px 0; font-size: 0.95rem; background: transparent; color: var(--text-primary);
}
.nav-search-input::placeholder { color: var(--text-muted); }
.btn-search {
  background: var(--accent-gradient); color: white; border: none; padding: 10px 24px; border-radius: 20px; 
  font-weight: 600; cursor: pointer; transition: var(--transition);
  box-shadow: 0 2px 8px var(--accent-glow);
  margin-left: 8px;
}
.btn-search:hover { filter: brightness(1.1); transform: scale(1.02); }

/* Actions */
.navbar-actions { display: flex; align-items: center; gap: 24px; }
.auth-links { display: flex; align-items: center; gap: 12px; }

.cart-icon-wrapper { position: relative; display: flex; align-items: center; justify-content: center; }
.cart-btn {
  color: var(--text-secondary); transition: var(--transition-bounce);
  padding: 8px; border-radius: 50%;
}
.cart-btn:hover { color: var(--accent); background: var(--accent-light); transform: scale(1.05); }
.cart-badge {
  position: absolute; top: -4px; right: -6px; 
  background: var(--danger); color: white;
  font-size: 0.7rem; font-weight: 800; width: 20px; height: 20px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  border: 2px solid white; box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.user-menu { position: relative; cursor: pointer; }
.nav-username { 
  display: flex; align-items: center; gap: 10px;
  padding: 6px 12px 6px 6px; border-radius: var(--radius-round);
  border: 1px solid transparent; transition: var(--transition);
  font-weight: 600; font-size: 0.95rem; color: var(--text-primary);
}
.nav-username:hover { background: white; border-color: var(--border); box-shadow: var(--shadow-sm); }
.avatar-sm { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; }

/* Dropdown */
.dropdown {
  position: absolute; top: calc(100% + 12px); right: 0;
  min-width: 240px; border-radius: var(--radius-lg);
  padding: 8px 0; border: 1px solid var(--border-glass);
  transform-origin: top right;
}
.dropdown-header { padding: 12px 16px; }
.dropdown-header .font-bold { color: var(--text-primary); font-weight: 700; margin-bottom: 2px; }
.text-sm { font-size: 0.85rem; }
.dropdown-divider { height: 1px; background: var(--border-glass); margin: 4px 0; }

.dropdown-item {
  display: flex; align-items: center; gap: 12px; width: 100%; text-align: left;
  padding: 12px 16px; font-size: 0.95rem; font-weight: 600;
  color: var(--text-secondary); background: none; transition: var(--transition);
}
.dropdown-item:hover { background: rgba(255,255,255,0.8); color: var(--accent); padding-left: 20px; }
.dropdown-item.danger:hover { color: var(--danger); background: var(--danger-light); }

/* Vue Animations */
.dropdown-fade-enter-active, .dropdown-fade-leave-active { transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.dropdown-fade-enter-from, .dropdown-fade-leave-to { opacity: 0; transform: scale(0.95) translateY(-10px); }
.bounce-in { animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes popIn { 0% { transform: scale(0); } 80% { transform: scale(1.2); } 100% { transform: scale(1); } }


/* ── Mobile Bottom Navigation (Android App Style) ── */
.desktop-only { display: flex; }
.mobile-only { display: none; }

@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: flex; }
  
  .navbar-inner { justify-content: center; } /* Center brand on mobile top */
  
  .mobile-bottom-nav {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000;
    display: flex; justify-content: space-around; align-items: center;
    padding: 12px 8px; padding-bottom: calc(12px + env(safe-area-inset-bottom));
    background: rgba(255, 255, 255, 0.9);
    border-top: 1px solid var(--border-glass);
    border-radius: 20px 20px 0 0;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
  }

  .mobile-nav-item {
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    color: var(--text-secondary); font-size: 0.75rem; font-weight: 600;
    transition: var(--transition-bounce);
    width: 60px;
  }
  .mobile-icon { width: 24px; height: 24px; transition: var(--transition-bounce); }
  
  .mobile-nav-item.active { color: var(--accent); }
  .mobile-nav-item.active .mobile-icon { transform: translateY(-4px) scale(1.1); filter: drop-shadow(0 4px 6px var(--accent-glow)); stroke-width: 2.5; }
  .mobile-nav-item:active { transform: scale(0.9); }
}
</style>
