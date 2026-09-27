<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON, patchJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null); const err = ref('')
const fabric = computed(() => fabrics.value.find(x => x.id === fid.value))
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
})
async function go(save){
  err.value = ''
  try { out.value = save ? await postJSON('/api/estimate',{window_id:wid.value,fabric_id:fid.value,save:true}) : await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}`) }
  catch(e){ out.value = null; err.value = '校验失败：起订米数或数据非法，未保存' }
}
async function saveM(){
  err.value = ''
  try {
    const f = await patchJSON(`/api/fabrics/${fid.value}`, { min_order_m: Number(fabric.value.min_order_m) })
    fabrics.value = fabrics.value.map(x => x.id === f.id ? f : x)
    await go(false)
  } catch(e){ err.value = '起订米数须为正数' }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label v-if="fabric">起订M <input type="number" step="0.1" min="0" v-model.number="fabric.min_order_m" style="width:5rem"> m</label>
<button @click="saveM">改M</button>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<template v-if="out">
<PanelCut :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" :min-order-m="out.min_order_m" :order-meters="out.order_meters" />
<table class="cmp"><tr><th>基础米</th><th>起订M</th><th>订货米</th></tr>
<tr><td>{{ out.meters }}</td><td>{{ out.min_order_m }}</td><td><b>{{ out.order_meters }}</b></td></tr></table>
</template>
</div></template>
