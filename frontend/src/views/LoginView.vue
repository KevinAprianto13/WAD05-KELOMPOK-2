<template>
  <NavBar />
  <div class="page">
    <div class="container">
      <div class="auth-wrap">
        <div class="auth-card card">
          <div class="auth-header">
            <RouterLink to="/" class="back-link">← Kembali</RouterLink>
            <h1>Masuk</h1>
            <p class="text-secondary">Selamat datang kembali di NusaShop</p>
          </div>

          <form @submit.prevent="handleLogin" class="auth-form" id="login-form">
            <div class="form-group">
              <label class="form-label">Email</label>
              <input
                id="login-email"
                v-model="form.email"
                type="email"
                class="form-input"
                placeholder="email@kamu.com"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label">Password</label>
              <input
                id="login-password"
                v-model="form.password"
                type="password"
                class="form-input"
                placeholder="••••••••"
                required
              />
            </div>

            <div v-if="error" class="error-msg">{{ error }}</div>

            <button id="login-submit" type="submit" class="btn btn-primary w-full" :disabled="loading">
              {{ loading ? 'Masuk...' : 'Masuk' }}
            </button>
          </form>

          <div class="demo-accounts">
            <p class="text-muted" style="font-size:0.8rem; margin-bottom: 8px;">Demo akun:</p>
            <button class="demo-btn" @click="fillDemo('admin')">Admin</button>
            <button class="demo-btn" @click="fillDemo('customer')">Customer</button>
          </div>

          <p class="auth-footer">
            Belum punya akun?
            <RouterLink to="/register" class="text-accent" id="login-to-register">Daftar sekarang</RouterLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const auth = useAuthStore()
const cart = useCartStore()
const router = useRouter()
const toast = inject('toast')

const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

function fillDemo(type) {
  if (type === 'admin') { form.value.email = 'admin@nusashop.com'; form.value.password = 'admin123' }
  else { form.value.email = 'customer@nusashop.com'; form.value.password = 'customer123' }
}

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    await auth.login(form.value.email, form.value.password)
    await cart.fetchCart()
    toast('Selamat datang kembali!', 'success')
    router.push(auth.isAdmin ? '/admin' : '/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Email atau password salah'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-wrap { display: flex; justify-content: center; padding: 40px 0; }
.auth-card { width: 100%; max-width: 440px; padding: 48px 40px; }
.auth-header { margin-bottom: 32px; }
.back-link { color: var(--text-muted); font-size: 0.85rem; display: inline-block; margin-bottom: 24px; transition: var(--transition); }
.back-link:hover { color: var(--text-primary); }
.auth-header h1 { font-size: 1.8rem; margin-bottom: 8px; }
.auth-form { display: flex; flex-direction: column; gap: 4px; margin-bottom: 20px; }
.w-full { width: 100%; justify-content: center; }
.error-msg { background: var(--danger-light); color: var(--danger); padding: 12px 16px; border-radius: var(--radius-sm); font-size: 0.85rem; }
.auth-footer { text-align: center; font-size: 0.9rem; color: var(--text-secondary); margin-top: 24px; }
.demo-accounts { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 8px; }
.demo-btn {
  padding: 6px 14px; border-radius: var(--radius-sm); font-size: 0.8rem; font-weight: 600;
  background: var(--bg-secondary); color: var(--text-secondary); border: 1px solid var(--border);
  transition: var(--transition);
}
.demo-btn:hover { border-color: var(--accent); color: var(--accent); }
</style>
