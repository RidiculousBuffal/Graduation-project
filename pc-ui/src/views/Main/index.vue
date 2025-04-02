<template>
  <div>
    <el-container>
      <el-aside style="width: auto">
        <common-aside></common-aside>
      </el-aside>
      <el-container>
        <el-header>
          <common-header></common-header>
        </el-header>
        <common-tags></common-tags>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>

</template>

<script>
import CommonAside from "@/components/CommonAside";
import CommonHeader from "@/components/CommonHeader";
import CommonTags from "@/components/CommonTags";
export default {
  name: "Main",
  components: {
    CommonAside,
    CommonHeader,
    CommonTags
  }
}
</script>

<style scoped>
.el-header{
  padding: 0;
}
</style>