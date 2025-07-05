<script setup lang="ts">
import {useData, withBase} from "vitepress";

const {isDark} = useData();
defineProps({
  lightSrc: String,
  darkSrc: String,
  alt: String,
})
</script>

<template>
  <img :src="isDark ? withBase(darkSrc) : withBase(lightSrc)" :alt="alt">
</template>

<style scoped>

</style>