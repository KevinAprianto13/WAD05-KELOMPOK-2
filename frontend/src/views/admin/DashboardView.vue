<template>
  <div class="dashboard">
    <div class="dash-header">
      <div>
        <h1>Dashboard</h1>
        <p class="text-secondary">Selamat datang kembali, {{ auth.user?.full_name }}</p>
      </div>
      <div class="dash-date text-muted">{{ today }}</div>
    </div>

    <!-- Stat Cards -->
    <div v-if="statsLoading" class="loading-center"><div class="spinner"></div></div>
    <div v-else class="stats-grid">
      <div v-for="s in statCards" :key="s.label" class="stat-card card" :id="`stat-${s.id}`">
        <div class="stat-icon" v-html="s.icon"></div>
        <div class="stat-info">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
        <div class="stat-accent" :style="{ background: s.color }"></div>
      </div>
    </div>

    <!-- Sales Chart -->
    <div class="card chart-card">
      <div class="flex-between chart-header">
        <h3>Grafik Penjualan (30 Hari Terakhir)</h3>
        <div class="chart-legend">
          <span class="legend-dot" style="background: #7c3aed"></span> Revenue
          <span class="legend-dot" style="background: #06b6d4; margin-left:16px"></span> Orders
        </div>
      </div>
      <div v-if="chartLoading" class="loading-center"><div class="spinner"></div></div>
      <div v-else-if="chartData" style="position: relative; height: 350px; width: 100%;">
        <Line :data="chartData" :options="chartOptions" id="sales-chart" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'
import { dashboardApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const auth = useAuthStore()
const stats = ref(null)
const salesData = ref([])
const statsLoading = ref(false)
const chartLoading = ref(false)

const today = new Date().toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })

function formatCurrency(v) {
  if (v >= 1000000) return `Rp ${(v / 1000000).toFixed(1)}jt`
  if (v >= 1000) return `Rp ${(v / 1000).toFixed(0)}rb`
  return `Rp ${v}`
}

const statCards = computed(() => {
  if (!stats.value) return []
  return [
    { id: 'revenue', icon: '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>', label: 'Total Revenue', value: formatCurrency(stats.value.total_revenue), color: '#7c3aed' },
    { id: 'orders', icon: '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>', label: 'Total Pesanan', value: stats.value.total_orders, color: '#06b6d4' },
    { id: 'customers', icon: '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>', label: 'Total Customer', value: stats.value.total_customers, color: '#10b981' },
    { id: 'products', icon: '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>', label: 'Produk Aktif', value: stats.value.total_products, color: '#f59e0b' },
    { id: 'pending', icon: '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>', label: 'Pesanan Pending', value: stats.value.pending_orders, color: '#ef4444' },
  ]
})

const chartData = computed(() => {
  if (!salesData.value.length) return null
  return {
    labels: salesData.value.map(d => {
      const date = new Date(d.date)
      return date.toLocaleDateString('id-ID', { month: 'short', day: 'numeric' })
    }),
    datasets: [
      {
        label: 'Revenue (Rp)',
        data: salesData.value.map(d => d.revenue),
        borderColor: '#7c3aed',
        backgroundColor: 'rgba(124,58,237,0.1)',
        fill: true, tension: 0.4, pointRadius: 3, yAxisID: 'y',
      },
      {
        label: 'Orders',
        data: salesData.value.map(d => d.orders),
        borderColor: '#06b6d4',
        backgroundColor: 'rgba(6,182,212,0.1)',
        fill: true, tension: 0.4, pointRadius: 3, yAxisID: 'y1',
      },
    ]
  }
})

const chartOptions = {
  responsive: true, maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { color: 'rgba(255,255,255,.05)' }, ticks: { color: '#9898b0', maxTicksLimit: 10 } },
    y: { type: 'linear', position: 'left', grid: { color: 'rgba(255,255,255,.05)' }, ticks: { color: '#9898b0' } },
    y1: { type: 'linear', position: 'right', grid: { drawOnChartArea: false }, ticks: { color: '#06b6d4' } },
  }
}

onMounted(async () => {
  statsLoading.value = true
  chartLoading.value = true
  try {
    const [s, c] = await Promise.all([dashboardApi.stats(), dashboardApi.sales()])
    stats.value = s.data
    salesData.value = c.data
  } finally {
    statsLoading.value = false
    chartLoading.value = false
  }
})
</script>

<style scoped>
.dashboard { max-width: 1100px; }
.dash-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
.dash-header h1 { margin-bottom: 4px; }
.dash-date { font-size: 0.85rem; padding-top: 8px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; margin-bottom: 32px; }
.stat-card { padding: 24px; position: relative; overflow: hidden; display: flex; gap: 16px; align-items: center; }
.stat-icon { font-size: 2rem; flex-shrink: 0; }
.stat-value { font-size: 1.4rem; font-weight: 800; margin-bottom: 4px; }
.stat-label { font-size: 0.8rem; color: var(--text-muted); font-weight: 500; }
.stat-accent { position: absolute; top: 0; right: 0; width: 4px; height: 100%; border-radius: 0 var(--radius-lg) var(--radius-lg) 0; }
.chart-card { padding: 28px; margin-bottom: 32px; }
.chart-header { margin-bottom: 24px; }
.chart-legend { display: flex; align-items: center; font-size: 0.85rem; color: var(--text-secondary); }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 6px; }
</style>
