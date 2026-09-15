<template>
  <div class="banner-page">
    <div class="page-heading">
      <div>
        <h1>Banner Promo</h1>
        <p class="text-secondary">Kelola gambar promo yang tampil di halaman utama.</p>
      </div>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>
    <div v-else class="banner-grid">
      <article v-for="slot in slots" :key="slot.position" class="banner-card card">
        <div class="banner-card-head">
          <div>
            <h3>{{ slot.label }}</h3>
            <p class="text-muted">{{ slot.help }}</p>
          </div>
          <span class="size-badge">{{ slot.size }}</span>
        </div>
        <div class="banner-preview" :class="slot.position">
          <img v-if="getBanner(slot.position)?.image_url" :src="getBanner(slot.position).image_url" :alt="getBanner(slot.position)?.title || slot.label" />
          <div v-else class="empty-preview">Belum ada gambar</div>
        </div>
        <div class="banner-meta" v-if="getBanner(slot.position)">
          <strong>{{ getBanner(slot.position).title || 'Tanpa judul' }}</strong>
          <span>{{ getBanner(slot.position).subtitle || 'Tidak ada subtitle' }}</span>
        </div>
        <div class="banner-actions">
          <button class="btn btn-primary btn-sm" @click="openEditor(slot.position)">{{ getBanner(slot.position) ? 'Edit' : 'Tambah gambar' }}</button>
          <button v-if="getBanner(slot.position)" class="btn btn-danger btn-sm" @click="openDelete(slot.position)">Hapus</button>
        </div>
      </article>
    </div>

    <div v-if="editorOpen" class="modal-overlay" @click.self="closeEditor">
      <div class="modal-box card compact-modal">
        <div class="modal-header">
          <div><h3>{{ editingPosition ? 'Edit banner' : 'Tambah banner' }}</h3><p class="text-muted">{{ currentSlot?.label }} · {{ currentSlot?.size }}</p></div>
          <button class="modal-close" @click="closeEditor">✕</button>
        </div>
        <form @submit.prevent="saveBanner" class="modal-form">
          <div class="source-tabs">
            <button type="button" :class="{ active: source === 'file' }" @click="source = 'file'">File lokal</button>
            <button type="button" :class="{ active: source === 'url' }" @click="source = 'url'">URL gambar</button>
          </div>
          <div v-if="source === 'file'" class="form-group">
            <label class="form-label">Pilih gambar</label>
            <input class="form-input" type="file" accept="image/jpeg,image/png,image/webp" @change="handleFile" :required="!getBanner(editingPosition)" />
            <small class="form-hint">JPG, PNG, atau WebP. Maksimal 10 MB. Gambar akan disesuaikan otomatis.</small>
          </div>
          <div v-else class="form-group">
            <label class="form-label">URL gambar</label>
            <input v-model.trim="form.image_url" class="form-input" type="url" placeholder="https://contoh.com/banner.jpg" required />
          </div>
          <div v-if="previewUrl" class="upload-preview"><img :src="previewUrl" alt="Preview banner" /></div>
          <div class="form-row">
            <div class="form-group"><label class="form-label">Judul</label><input v-model.trim="form.title" class="form-input" placeholder="Contoh: Cashback 100RB" /></div>
            <div class="form-group"><label class="form-label">Subtitle</label><input v-model.trim="form.subtitle" class="form-input" placeholder="Belanja puas!" /></div>
          </div>
          <div class="form-group"><label class="form-label">Link saat banner diklik <span class="optional">(opsional)</span></label><input v-model.trim="form.link_url" class="form-input" type="url" placeholder="https://..." /></div>
          <div class="modal-actions"><button type="button" class="btn btn-secondary" @click="closeEditor">Batal</button><button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Menyimpan...' : 'Simpan banner' }}</button></div>
        </form>
      </div>
    </div>

    <div v-if="deletePosition" class="modal-overlay" @click.self="deletePosition = null">
      <div class="modal-box card confirm-modal">
        <div class="confirm-icon">!</div>
        <h3>Hapus banner ini?</h3>
        <p class="text-secondary">Banner akan hilang dari halaman utama. Anda bisa menambahkan gambar baru kapan saja.</p>
        <div class="modal-actions"><button class="btn btn-secondary" @click="deletePosition = null">Batal</button><button class="btn btn-danger" :disabled="deleting" @click="deleteBanner">{{ deleting ? 'Menghapus...' : 'Ya, hapus banner' }}</button></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, reactive, ref } from 'vue'
import { bannersApi } from '@/api'

const toast = inject('toast')
const slots = [
  { position: 'main', label: 'Banner utama', size: '1600 × 886 px', help: 'Area besar di sebelah kiri' },
  { position: 'side_1', label: 'Banner samping 1', size: '1200 × 625 px', help: 'Area kanan bagian atas' },
  { position: 'side_2', label: 'Banner samping 2', size: '1200 × 625 px', help: 'Area kanan bagian bawah' },
]
const banners = ref([])
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editorOpen = ref(false)
const deletePosition = ref(null)
const editingPosition = ref(null)
const source = ref('file')
const selectedFile = ref(null)
const previewUrl = ref('')
const form = reactive({ title: '', subtitle: '', link_url: '', image_url: '' })
const currentSlot = computed(() => slots.find(slot => slot.position === editingPosition.value))

function getBanner(position) { return banners.value.find(banner => banner.position === position) }
function openEditor(position) {
  const banner = getBanner(position)
  editingPosition.value = position
  source.value = 'file'
  selectedFile.value = null
  previewUrl.value = banner?.image_url || ''
  Object.assign(form, { title: banner?.title || '', subtitle: banner?.subtitle || '', link_url: banner?.link_url || '', image_url: '' })
  editorOpen.value = true
}
function closeEditor() { editorOpen.value = false; selectedFile.value = null; previewUrl.value = '' }
function handleFile(event) { selectedFile.value = event.target.files[0] || null; previewUrl.value = selectedFile.value ? URL.createObjectURL(selectedFile.value) : '' }
async function fetchBanners() { loading.value = true; try { banners.value = (await bannersApi.list()).data } finally { loading.value = false } }
async function saveBanner() {
  if (source.value === 'file' && !selectedFile.value && !getBanner(editingPosition.value)) { toast('Pilih file gambar terlebih dahulu', 'error'); return }
  saving.value = true
  try {
    const data = new FormData()
    if (source.value === 'file' && selectedFile.value) data.append('image', selectedFile.value)
    else data.append('image_url', form.image_url)
    data.append('title', form.title)
    data.append('subtitle', form.subtitle)
    data.append('link_url', form.link_url)
    const { data: saved } = await bannersApi.save(editingPosition.value, data)
    banners.value = [...banners.value.filter(banner => banner.position !== saved.position), saved]
    toast('Banner berhasil disimpan', 'success')
    closeEditor()
  } catch (error) { toast(error.response?.data?.detail || 'Gagal menyimpan banner', 'error') } finally { saving.value = false }
}
function openDelete(position) { deletePosition.value = position }
async function deleteBanner() {
  deleting.value = true
  try { await bannersApi.delete(deletePosition.value); banners.value = banners.value.filter(banner => banner.position !== deletePosition.value); toast('Banner berhasil dihapus', 'success'); deletePosition.value = null }
  catch (error) { toast(error.response?.data?.detail || 'Gagal menghapus banner', 'error') } finally { deleting.value = false }
}
onMounted(fetchBanners)
</script>

<style scoped>
.banner-page { max-width: 1100px; }
.page-heading { margin-bottom: 28px; }
.page-heading h1 { margin-bottom: 4px; }
.banner-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
.banner-card { padding: 20px; }
.banner-card:last-child { grid-column: span 2; }
.banner-card-head, .banner-actions, .modal-header, .modal-actions { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.banner-card-head { align-items: flex-start; margin-bottom: 14px; }
.banner-card-head h3 { margin-bottom: 4px; }
.banner-card-head p { font-size: .82rem; }
.size-badge { white-space: nowrap; padding: 5px 8px; border-radius: 6px; background: var(--bg-secondary); color: var(--text-muted); font-size: .72rem; }
.banner-preview { aspect-ratio: 1600 / 886; overflow: hidden; border-radius: 10px; background: var(--bg-secondary); }
.banner-preview.side_1, .banner-preview.side_2 { aspect-ratio: 1200 / 625; }
.banner-preview img, .upload-preview img { width: 100%; height: 100%; object-fit: cover; display: block; }
.empty-preview { height: 100%; display: grid; place-items: center; color: var(--text-muted); font-size: .9rem; }
.banner-meta { display: flex; flex-direction: column; gap: 3px; padding: 12px 0; min-height: 58px; }
.banner-meta span { color: var(--text-secondary); font-size: .85rem; }
.banner-actions { justify-content: flex-start; }
.modal-overlay { position: fixed; inset: 0; z-index: 9000; display: flex; align-items: center; justify-content: center; padding: 20px; background: rgba(15, 23, 42, .62); backdrop-filter: blur(4px); }
.modal-box { width: 100%; background: white; border-radius: 12px; }
.compact-modal { max-width: 620px; max-height: 90vh; overflow-y: auto; padding: 24px; }
.confirm-modal { max-width: 390px; padding: 28px; text-align: center; }
.confirm-modal .modal-actions { justify-content: center; margin-top: 22px; }
.modal-header { margin-bottom: 18px; align-items: flex-start; }
.modal-close { background: none; color: var(--text-muted); font-size: 1.1rem; padding: 4px; }
.modal-form { display: flex; flex-direction: column; gap: 10px; }
.source-tabs { display: flex; gap: 6px; padding: 4px; border-radius: 8px; background: var(--bg-secondary); }
.source-tabs button { flex: 1; border: 0; padding: 9px; border-radius: 6px; color: var(--text-secondary); background: transparent; cursor: pointer; font-weight: 600; }
.source-tabs button.active { background: white; color: var(--accent); box-shadow: 0 1px 4px rgba(15,23,42,.1); }
.form-group { margin: 0; }
.form-label { display: block; margin-bottom: 6px; font-size: .84rem; font-weight: 600; }
.form-hint, .optional { color: var(--text-muted); font-size: .75rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.upload-preview { height: 130px; overflow: hidden; border-radius: 8px; background: var(--bg-secondary); }
.confirm-icon { width: 38px; height: 38px; margin: 0 auto 12px; border-radius: 50%; display: grid; place-items: center; background: #fef2f2; color: var(--danger); font-size: 1.2rem; font-weight: 800; }
.confirm-modal h3 { margin-bottom: 8px; }
.confirm-modal p { font-size: .9rem; line-height: 1.5; }
@media (max-width: 700px) { .banner-grid { grid-template-columns: 1fr; } .banner-card:last-child { grid-column: auto; } .form-row { grid-template-columns: 1fr; } }
</style>
