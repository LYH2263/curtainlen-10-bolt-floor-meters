<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul>
<li v-for="r in items" :key="r.id">
  #{{ r.id }} {{ r.window_name }} / {{ r.fabric_name }}：
  基础 {{ r.result?.base_meters ?? r.result?.meters }}m
  <template v-if="r.result?.min_order_m != null">｜起订 {{ r.result.min_order_m }}m</template>
  ｜订货 <b>{{ r.result?.order_meters ?? r.result?.meters }}m</b>
</li></ul></div></template>
