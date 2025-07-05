<script setup lang="ts">
import {useData, withBase} from "vitepress";

defineProps({
  title: String,
  description: String,
  link: String,
  lightSrc: String,
  darkSrc: String,
})
const {isDark} = useData();
</script>

<template>
  <a :href="link" target="_blank" rel="noopener" class="git-card">
    <img :src="isDark ? withBase(darkSrc) : withBase(lightSrc)" alt="" class="git-card-logo"/>
    <div class="git-card-info">
      <strong>{{ title }}</strong>
      <p>{{ description }}</p>
    </div>
  </a>
</template>

<style scoped>
.git-card {
  display: flex;
  align-items: center;
  padding: 0.8em 1em;
  gap: 1em;
  border: 1px solid var(--vp-c-border);
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  width: 100%;
  transition: box-shadow 0.3s;
}

.git-card-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.git-card-info p {
  margin: 0;
  font-size: 0.9em;
  color: var(--vp-c-text-2);
}
</style>