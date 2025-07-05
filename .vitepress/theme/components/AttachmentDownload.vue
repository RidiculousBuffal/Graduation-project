<script setup lang="ts">
import {defineProps} from 'vue'
import {useData, withBase} from "vitepress";

const props = defineProps({
  filePath: {type: String, required: true},
  fileName: {type: String, default: ''},
  label: {type: String, default: '下载附件'},
  logoLightSrc: {type: String, default: '/file-light.svg'},
  logoDarkSrc: {type: String, default: '/file-dark.svg'}, // 可选 logo 图片路径
  logoAlt: {type: String, default: '附件图标'}
})
const {isDark} = useData();
const href = withBase(props.filePath)

function extractFileName(filePath) {
  const match = filePath.match(/[^/\\]*$/);
  return match ? match[0] : '';
}

const downloadName = props.fileName || extractFileName(props.filePath);
</script>

<template>
  <a
      :href="href"
      :download="downloadName"
      target="_blank"
      rel="noopener noreferrer"
      class="attachment-download"
  >
    <img v-if="logoDarkSrc||logoLightSrc" :src="isDark ? withBase(logoDarkSrc) : withBase(logoLightSrc)" :alt="logoAlt"
         class="attachment-logo"/>
    <span>{{ label }}</span>
  </a>
</template>

<style scoped>
.attachment-download {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  padding: 6px 12px;
  background-color: var(--vp-c-brand-1, #409EFF);
  color: white;
  font-weight: 600;
  text-decoration: none;
  border-radius: 4px;
  user-select: none;
  transition: background-color 0.2s ease;
}

.attachment-download:hover {
  background-color: var(--vp-c-brand-2, #66b1ff);
  text-decoration: none;
  color: white;
}

.attachment-logo {
  width: 20px;
  height: 20px;
  object-fit: contain;
}
</style>