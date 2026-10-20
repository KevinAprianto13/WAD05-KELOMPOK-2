<template>
  <NavBar />
  <div class="page">
    <div class="container">
      <div class="auth-wrap">
        <div class="auth-card card">
          <div class="auth-header">
            <RouterLink to="/" class="back-link">← Kembali</RouterLink>
            <h1>Buat Akun</h1>
            <p class="text-secondary">Bergabung dengan NusaShop sekarang</p>
          </div>

          <form @submit.prevent="handleRegister" class="auth-form" id="register-form">
            <div class="form-group">
              <label class="form-label">Nama Lengkap</label>
              <input id="reg-name" v-model="form.fullName" type="text" class="form-input" placeholder="Nama Lengkapmu" required />
            </div>
            <div class="form-group">
              <label class="form-label">Email</label>
              <input id="reg-email" v-model="form.email" type="email" class="form-input" placeholder="email@kamu.com" required />
            </div>
            <div class="form-group">
              <label class="form-label">Password</label>
              <input id="reg-password" v-model="form.password" type="password" class="form-input" placeholder="Min. 8 karakter" required minlength="8" />
            </div>

            <div v-if="error" class="error-msg">{{ error }}</div>

            <button id="register-submit" type="submit" class="btn btn-primary w-full" :disabled="loading">
              {{ loading ? 'Mendaftar...' : 'Daftar Sekarang' }}
            </button>
          </form>

          <p class="auth-footer">
            Sudah punya akun?
            <RouterLink to="/login" class="text-accent" id="register-to-login">Masuk di sini</RouterLink>
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

const auth = useAuthStore()
const router = useRouter()
const toast = inject('toast')

const form = ref({ fullName: '', email: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  loading.value = true; error.value = ''
  try {
    await auth.register(form.value.email, form.value.fullName, form.value.password)
    toast('Akun berhasil dibuat! Selamat datang!', 'success')
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Pendaftaran gagal, coba lagi'
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
</style>
