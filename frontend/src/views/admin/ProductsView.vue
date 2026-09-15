<template>
  <div>
    <div class="flex-between mb-header">
      <h1>Manajemen Produk</h1>
      <button class="btn btn-primary" id="admin-add-product-btn" @click="openModal()">+ Tambah Produk</button>
    </div>

    <div v-if="loading" class="loading-center"><div class="spinner"></div></div>
    <div v-else class="table-wrapper">
      <table id="products-table">
        <thead>
          <tr>
            <th>Gambar</th><th>Nama</th><th>Kategori</th><th>Harga</th><th>Stok</th><th>Status</th><th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id" :id="`product-row-${p.id}`">
            <td>
              <div class="prod-thumb-wrap">
                <img v-if="thumbnailUrl(p) && !brokenThumbnails.has(p.id)" :src="thumbnailUrl(p)" :alt="p.name" class="prod-thumb" @error="markThumbnailBroken(p.id)" />
                <div v-else class="prod-thumb prod-thumb-placeholder">▧</div>
                <span v-if="productImageCount(p) > 1" class="thumb-count">+{{ productImageCount(p) - 1 }}</span>
              </div>
            </td>
            <td><div class="prod-name">{{ p.name }}</div></td>
            <td><span class="text-secondary">{{ p.category?.name || '—' }}</span></td>
            <td class="price">{{ formatPrice(p.price) }}</td>
            <td :class="p.stock < 5 ? 'text-danger' : ''">{{ p.stock }}</td>
            <td><span :class="['badge', p.is_active ? 'badge-delivered' : 'badge-cancelled']">{{ p.is_active ? 'Aktif' : 'Nonaktif' }}</span></td>
            <td>
              <div class="action-btns">
                <button class="btn btn-secondary btn-sm" :id="`edit-product-${p.id}`" @click="openModal(p)">Edit</button>
                <button class="btn btn-danger btn-sm" :id="`delete-product-${p.id}`" @click="deleteProduct(p)">Hapus</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-box card" id="product-modal">
        <div class="modal-header">
          <div><h3>{{ editId ? 'Edit Produk' : 'Tambah Produk' }}</h3><p class="text-muted">Lengkapi informasi produk dengan singkat.</p></div>
          <button class="modal-close" id="modal-close-btn" @click="closeModal">✕</button>
        </div>
        <form @submit.prevent="saveProduct" class="modal-form">
          <div class="form-row">
            <div class="form-group"><label class="form-label">Nama Produk</label><input id="prod-name" v-model.trim="form.name" class="form-input" placeholder="Contoh: Sneakers Casual" required /></div>
            <div class="form-group"><label class="form-label">Kategori</label><select id="prod-category" v-model="form.category_id" class="form-input"><option value="">Pilih kategori</option><option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option></select></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label class="form-label">Harga (Rp)</label><input id="prod-price" v-model="form.price" type="number" min="0" class="form-input" placeholder="0" required /></div>
            <div class="form-group"><label class="form-label">Stok</label><input id="prod-stock" v-model="form.stock" type="number" min="0" class="form-input" placeholder="0" required /></div>
          </div>
          <div class="form-group"><label class="form-label">Deskripsi <span class="optional">(opsional)</span></label><textarea id="prod-desc" v-model.trim="form.description" class="form-input" rows="2" placeholder="Jelaskan produk secara singkat"></textarea></div>
          <div class="image-section">
            <div class="section-label">Gambar produk</div>
            <div class="source-tabs"><button type="button" :class="{ active: imageSource === 'file' }" @click="imageSource = 'file'">File lokal</button><button type="button" :class="{ active: imageSource === 'url' }" @click="imageSource = 'url'">URL gambar</button></div>
            <input v-if="imageSource === 'file'" id="prod-image-file" class="form-input" type="file" accept="image/jpeg,image/png,image/webp" multiple @change="handleImageFiles" :required="!editId && !form.image_url" />
            <input v-else id="prod-image" v-model.trim="form.image_url" type="url" class="form-input" placeholder="https://contoh.com/gambar.jpg" />
            <small class="form-hint">JPG, PNG, WebP, maksimal 10 MB. Gambar lokal akan dioptimalkan otomatis.</small>
            <div v-if="existingImages.length || newImagePreviews.length" class="image-previews">
              <div v-for="image in existingImages" :key="image.id || image.url" class="image-preview">
                <img :src="image.url" alt="Gambar produk" />
                <button type="button" class="remove-image" :aria-label="`Hapus gambar ${image.primary ? 'utama' : 'galeri'}`" @click="removeExistingImage(image)">×</button>
                <span v-if="image.primary" class="primary-label">Utama</span>
              </div>
              <div v-for="preview in newImagePreviews" :key="preview" class="image-preview new-image-preview"><img :src="preview" alt="Gambar baru" /><span class="new-label">Baru</span></div>
            </div>
          </div>
          <div class="modal-actions"><button type="button" class="btn btn-secondary" @click="closeModal">Batal</button><button id="prod-save-btn" type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Menyimpan...' : 'Simpan Produk' }}</button></div>
        </form>
      </div>
    </div>
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal-box card confirm-modal"><div class="confirm-icon">!</div><h3>Hapus produk?</h3><p class="text-secondary">Produk <strong>{{ deleteTarget.name }}</strong> akan dinonaktifkan dari toko.</p><div class="modal-actions"><button class="btn btn-secondary" @click="deleteTarget = null">Batal</button><button class="btn btn-danger" :disabled="deleting" @click="confirmDelete">{{ deleting ? 'Menghapus...' : 'Ya, hapus' }}</button></div></div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { productsApi, categoriesApi } from '@/api'

const toast = inject('toast')
const products = ref([])
const categories = ref([])
const loading = ref(false)
const showModal = ref(false)
const saving = ref(false)
const editId = ref(null)
const deleting = ref(false)
const deleteTarget = ref(null)
const imageSource = ref('file')
const selectedImages = ref([])
const existingImages = ref([])
const newImagePreviews = ref([])
const removedImageIds = ref([])
const removePrimaryImage = ref(false)
const brokenThumbnails = ref(new Set())

const form = reactive({ name: '', description: '', price: '', stock: 0, image_url: '', category_id: '' })

function formatPrice(p) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p)
}

function thumbnailUrl(product) {
  return product.image_url || product.images?.[0]?.image_url || ''
}

function productImageCount(product) {
  return (product.image_url ? 1 : 0) + (product.images?.length || 0)
}

function markThumbnailBroken(productId) {
  brokenThumbnails.value = new Set([...brokenThumbnails.value, productId])
}

function openModal(product = null) {
  editId.value = product?.id || null
  imageSource.value = product?.image_url?.startsWith('/uploads/') ? 'file' : 'url'
  selectedImages.value = []
  existingImages.value = [
    ...(product?.image_url ? [{ id: null, url: product.image_url, primary: true }] : []),
    ...(product?.images || []).map(image => ({ id: image.id, url: image.image_url, primary: false })),
  ]
  newImagePreviews.value = []
  removedImageIds.value = []
  removePrimaryImage.value = false
  Object.assign(form, {
    name: product?.name || '', description: product?.description || '',
    price: product?.price || '', stock: product?.stock || 0,
    image_url: product?.image_url || '', category_id: product?.category_id || '',
  })
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedImages.value = []
  existingImages.value = []
  newImagePreviews.value = []
  removedImageIds.value = []
  removePrimaryImage.value = false
}

function handleImageFiles(event) {
  selectedImages.value = Array.from(event.target.files || [])
  newImagePreviews.value = selectedImages.value.map(file => URL.createObjectURL(file))
}

function removeExistingImage(image) {
  if (image.primary) removePrimaryImage.value = true
  else removedImageIds.value.push(image.id)
  existingImages.value = existingImages.value.filter(item => item !== image)
}

async function saveProduct() {
  saving.value = true
  try {
    const productData = { ...form }
    if (removePrimaryImage.value) productData.image_url = ''
    if (editId.value) {
      let { data: saved } = await productsApi.update(editId.value, productData)
      for (const imageId of removedImageIds.value) {
        saved = (await productsApi.deleteImage(editId.value, imageId)).data
      }
      if (selectedImages.value.length) {
        const imageData = new FormData()
        selectedImages.value.forEach(image => imageData.append('images', image))
        saved = (await productsApi.uploadImages(editId.value, imageData)).data
      }
      products.value = products.value.map(product => product.id === saved.id ? saved : product)
      toast('Produk berhasil diperbarui', 'success')
    } else {
      let { data: saved } = await productsApi.create(productData)
      if (selectedImages.value.length) {
        const imageData = new FormData()
        selectedImages.value.forEach(image => imageData.append('images', image))
        saved = (await productsApi.uploadImages(saved.id, imageData)).data
      }
      toast('Produk berhasil ditambahkan', 'success')
    }
    closeModal()
    await fetchProducts()
  } catch (e) {
    toast(e.response?.data?.detail || 'Gagal menyimpan', 'error')
  } finally { saving.value = false }
}

async function deleteProduct(p) {
  deleteTarget.value = p
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await productsApi.delete(deleteTarget.value.id)
    toast('Produk dinonaktifkan', 'success')
    deleteTarget.value = null
    await fetchProducts()
  } catch (error) { toast(error.response?.data?.detail || 'Gagal menghapus', 'error')
  } finally { deleting.value = false }
}

async function fetchProducts() {
  loading.value = true
  try { const { data } = await productsApi.list({ limit: 100 }); products.value = data }
  finally { loading.value = false }
}

onMounted(async () => {
  const [, c] = await Promise.all([fetchProducts(), categoriesApi.list()])
  categories.value = c.data
})
</script>

<style scoped>
.mb-header { margin-bottom: 28px; }
.prod-thumb-wrap { position: relative; width: 58px; height: 58px; }
.prod-thumb { width: 58px; height: 58px; object-fit: cover; border-radius: 8px; }
.prod-thumb-placeholder { display: grid; place-items: center; color: #94a3b8; background: linear-gradient(145deg, #f8fafc, #e2e8f0); font-size: 1.5rem; }
.thumb-count { position: absolute; right: -6px; bottom: -5px; min-width: 22px; padding: 2px 5px; border: 2px solid white; border-radius: 999px; color: white; background: var(--accent); font-size: .68rem; font-weight: 800; text-align: center; }
.prod-name { font-weight: 600; font-size: 0.9rem; }
.action-btns { display: flex; gap: 8px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.7); backdrop-filter: blur(4px); z-index: 9000; display: flex; align-items: center; justify-content: center; padding: 24px; }
.modal-box { width: 100%; max-width: 590px; max-height: 88vh; overflow-y: auto; padding: 22px; }
.modal-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }
.modal-header h3 { margin-bottom: 4px; }
.modal-header p { font-size: .8rem; }
.modal-close { background: none; color: var(--text-muted); font-size: 1.2rem; transition: var(--transition); padding: 4px; }
.modal-close:hover { color: var(--text-primary); }
.modal-form { display: flex; flex-direction: column; gap: 11px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { margin: 0; }
.form-label, .section-label { display: block; margin-bottom: 6px; font-size: .82rem; font-weight: 700; }
.optional, .form-hint { color: var(--text-muted); font-size: .74rem; font-weight: 400; }
.image-section { padding: 12px; border: 1px solid var(--border); border-radius: 9px; background: #fafbff; }
.source-tabs { display: flex; gap: 5px; margin-bottom: 9px; padding: 3px; border-radius: 7px; background: var(--bg-secondary); }
.source-tabs button { flex: 1; border: 0; padding: 7px; border-radius: 5px; color: var(--text-secondary); background: transparent; cursor: pointer; font-size: .8rem; font-weight: 700; }
.source-tabs button.active { color: var(--accent); background: white; box-shadow: 0 1px 4px rgba(15,23,42,.1); }
.form-hint { display: block; margin-top: 6px; }
.image-previews { display: flex; gap: 8px; overflow-x: auto; margin-top: 9px; padding: 3px 2px 5px; }
.image-preview { position: relative; width: 72px; height: 72px; flex: 0 0 auto; overflow: hidden; border-radius: 7px; border: 1px solid var(--border); background: white; }
.image-preview img { width: 100%; height: 100%; object-fit: cover; }
.remove-image { position: absolute; top: 3px; right: 3px; width: 20px; height: 20px; display: grid; place-items: center; padding: 0; border-radius: 50%; color: white; background: rgba(15,23,42,.78); font-size: 1rem; line-height: 1; }
.remove-image:hover { background: var(--danger); }
.primary-label, .new-label { position: absolute; right: 3px; bottom: 3px; left: 3px; padding: 2px; border-radius: 3px; color: white; background: rgba(79,70,229,.86); font-size: .58rem; font-weight: 700; text-align: center; }
.new-image-preview { border-color: var(--accent); }
.new-label { background: rgba(16,185,129,.9); }
.modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 8px; }
.confirm-modal { max-width: 390px; text-align: center; padding: 28px; }
.confirm-modal .modal-actions { justify-content: center; margin-top: 22px; }
.confirm-icon { width: 38px; height: 38px; margin: 0 auto 12px; display: grid; place-items: center; border-radius: 50%; background: #fef2f2; color: var(--danger); font-weight: 800; font-size: 1.2rem; }
.confirm-modal h3 { margin-bottom: 8px; }
.confirm-modal p { font-size: .9rem; line-height: 1.5; }
@media (max-width: 600px) { .form-row { grid-template-columns: 1fr; gap: 8px; } .modal-box { padding: 18px; } }
</style>
