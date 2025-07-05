<script setup lang="ts">
import { VPTeamMembers } from "vitepress/theme";
import { withBase } from "vitepress";

type member = {
  avatar: string,
  name: string,
  title: string
}

interface members {
  members: member[]
}

const props = defineProps<members>()

// 处理 avatar 路径
const allMembers = props.members.map(m => ({
  ...m,
  avatar: withBase(m.avatar)
}))

// 前两个成员
const firstRowMembers = allMembers.slice(0, 2)
// 剩余成员
const restMembers = allMembers.slice(2)

// 将剩余成员分成每3个一组
function chunk(arr: typeof restMembers, size: number) {
  const res = []
  for(let i=0; i<arr.length; i+=size) {
    res.push(arr.slice(i, i+size))
  }
  return res
}
const chunkedRestMembers = chunk(restMembers, 3)

</script>

<template>
  <div>
    <!-- 第一排两个成员，使用一个 VPTeamMembers 实例 -->
    <!-- VPTeamMembers 内部会处理居中和排列 -->
    <div v-if="firstRowMembers.length" class="team-row-wrapper">
      <VPTeamMembers :members="firstRowMembers" size="medium" />
    </div>

    <!-- 后面的每3个一排，每个 chunk 使用一个 VPTeamMembers 实例 -->
    <div v-for="(group, idx) in chunkedRestMembers" :key="idx" class="team-row-wrapper">
      <VPTeamMembers :members="group" />
    </div>
  </div>
</template>

<style scoped>
</style>
