<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([]); const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/fabrics')).items })
async function save(f){
  err.value = ''
  try {
    const u = await patchJSON(`/api/fabrics/${f.id}`, { min_order_m: Number(f.min_order_m) })
    Object.assign(f, u)
  } catch(e){ err.value = `${f.name}：起订米数须为正数` }
}
</script>
<template><div class="page"><h1>面料</h1>
<p v-if="err" class="bad">{{ err }}</p>
<table class="cmp"><tr><th>面料</th><th>门幅</th><th>起订M(m)</th><th></th></tr>
<tr v-for="f in items" :key="f.id">
<td>{{ f.name }}</td><td>{{ f.fabric_width }}m</td>
<td><input type="number" step="0.1" min="0" v-model.number="f.min_order_m" style="width:5rem"></td>
<td><button @click="save(f)">保存M</button></td>
</tr></table>
</div></template>
