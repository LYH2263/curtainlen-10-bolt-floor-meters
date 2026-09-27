<script setup>
defineProps({ panels: Number, cutHeight: Number, meters: Number, minOrderM: Number, orderMeters: Number })
</script>
<template>
  <div class="panel-cut">
    <div v-for="n in Math.min(panels||0,8)" :key="n" class="panel" :style="{height: `${(cutHeight||1)*40}px`}"></div>
    <p>{{ panels }} 幅 × {{ cutHeight }} m = {{ meters }} m</p>
    <p v-if="orderMeters != null">起订 {{ minOrderM }} m 托底 → 订货 <b>{{ orderMeters }}</b> m</p>
  </div>
</template>
