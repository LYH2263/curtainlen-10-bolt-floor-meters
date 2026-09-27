<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([]); const cur = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
async function open(id){ cur.value = await getJSON(`/api/runs/${id}`) }
const order = r => r.result?.order_meters ?? r.result?.meters
</script>
<template><div class="page"><h1>记录</h1>
<table class="cmp"><tr><th>#</th><th>窗户</th><th>面料</th><th>基础米</th><th>起订M</th><th>订货米</th></tr>
<tr v-for="r in items" :key="r.id" @click="open(r.id)" style="cursor:pointer">
<td>{{ r.id }}</td><td>{{ r.window_name }}</td><td>{{ r.fabric_name }}</td>
<td>{{ r.result?.meters }}</td><td>{{ r.result?.min_order_m ?? '—' }}</td><td><b>{{ order(r) }}</b></td>
</tr></table>
<div v-if="cur" class="fab">#{{ cur.id }} 当初订货 <b>{{ order(cur) }}</b> m（基础 {{ cur.result?.meters }} m / 起订 {{ cur.result?.min_order_m ?? '—' }} m，{{ cur.created_at }}）</div>
</div></template>
