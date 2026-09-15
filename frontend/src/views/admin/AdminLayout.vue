<template>
  <div class="admin-layout">
    <!-- Mobile Overlay -->
    <div class="sidebar-overlay" :class="{ 'show': isSidebarOpen }" @click="isSidebarOpen = false"></div>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'open': isSidebarOpen }">
      <div class="sidebar-brand">
        <div class="brand-icon-wrap">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2" width="20" height="20">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>
        <span class="gradient-text">NusaShop</span>
      </div>
    <nav class="sidebar-nav">
        <RouterLink to="/admin" exact class="sidebar-link" id="admin-nav-dashboard">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
          Dashboard
        </RouterLink>
        <RouterLink to="/admin/products" class="sidebar-link" id="admin-nav-products">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
          Produk
        </RouterLink>
        <RouterLink to="/admin/banners" class="sidebar-link" id="admin-nav-banners">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><path d="m21 15-5-5L5 21"></path></svg>
          Banner Promo
        </RouterLink>
        <RouterLink to="/admin/orders" class="sidebar-link" id="admin-nav-orders">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          Pesanan
        </RouterLink>
        <RouterLink to="/admin/chat" class="sidebar-link" id="admin-nav-chat">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          Chat Inbox
        </RouterLink>
        <div class="sidebar-divider"></div>
        <RouterLink to="/" class="sidebar-link" id="admin-nav-store">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          Lihat Toko
        </RouterLink>
        <button class="sidebar-link sidebar-logout" id="admin-nav-logout" @click="handleLogout">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          Keluar
        </button>
      </nav>
    </aside>

    <!-- Main -->
    <main class="admin-main">
      <header class="admin-header">
        <button class="hamburger-btn" @click="isSidebarOpen = true">
          <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
        <NotificationBell />
      </header>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import NotificationBell from '@/components/NotificationBell.vue'

const auth = useAuthStore()
const cart = useCartStore()
const router = useRouter()
const route = useRoute()

const isSidebarOpen = ref(false)

watch(() => route.path, () => {
  isSidebarOpen.value = false
})

function handleLogout() {
  auth.logout()
  cart.reset()
  router.push('/')
}
</script>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background: var(--bg-secondary); }
.sidebar {
  width: 260px; flex-shrink: 0; background: white;
  border-right: 1px solid var(--border); padding: 40px 24px;
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  display: flex; flex-direction: column;
}
.sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 0 16px; margin-bottom: 40px; font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; }
.brand-icon-wrap { background: linear-gradient(135deg, var(--accent), var(--accent-hover)); width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); flex-shrink: 0; }
.sidebar-nav { display: flex; flex-direction: column; gap: 8px; flex: 1; }
.sidebar-link {
  display: flex; align-items: center; gap: 16px; padding: 14px 20px;
  border-radius: var(--radius-sm); font-size: 0.95rem; font-weight: 600; color: var(--text-secondary);
  transition: var(--transition); background: none; border: none; width: 100%; text-align: left; cursor: pointer;
}
.sidebar-link:hover { background: var(--bg-secondary); color: var(--text-primary); }
.sidebar-link.router-link-active { background: var(--accent); color: white; }
.sidebar-divider { height: 1px; background: var(--border); margin: 24px 0; }
.sidebar-logout { margin-top: auto; color: var(--danger) !important; }
.sidebar-logout:hover { background: var(--danger-light) !important; }
.admin-main { flex: 1; padding: 32px 48px; min-height: 100vh; overflow-x: hidden; display: flex; flex-direction: column; }
.admin-header { display: flex; justify-content: flex-end; margin-bottom: 24px; align-items: center; }
.hamburger-btn { display: none; background: transparent; border: none; color: var(--text-primary); cursor: pointer; padding: 8px; border-radius: var(--radius-sm); transition: var(--transition); }
.hamburger-btn:hover { background: var(--bg-secondary); color: var(--accent); }
.sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 40; opacity: 0; transition: var(--transition); pointer-events: none; }

@media (max-width: 900px) {
  .sidebar { position: fixed; left: -260px; z-index: 50; transition: var(--transition-slow); }
  .sidebar.open { transform: translateX(260px); }
  .sidebar-overlay { display: block; }
  .sidebar-overlay.show { opacity: 1; pointer-events: auto; }
  .admin-main { padding: 24px 20px; }
  .admin-header { justify-content: space-between; }
  .hamburger-btn { display: flex; }
}
</style>
