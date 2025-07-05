<script setup lang="ts">
import {useData} from "vitepress";

const {isDark} = useData();
defineProps({
  lightSrc: String,
  darkSrc: String,
  alt: String,
})
</script>

<template>
  <img :src="isDark ? darkSrc : lightSrc" :alt="alt">
</template>

<style scoped>

</style>