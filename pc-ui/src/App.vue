<template>
  <div id="app">
<!--    <el-row>-->
<!--      <el-button>默认按钮</el-button>-->
<!--      <el-button type="primary">主要按钮</el-button>-->
<!--      <el-button type="success">成功按钮</el-button>-->
<!--      <el-button type="info">信息按钮</el-button>-->
<!--      <el-button type="warning">警告按钮</el-button>-->
<!--      <el-button type="danger">危险按钮</el-button>-->
<!--    </el-row>-->
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

html, body, h3, p {
  margin: 0;
  padding: 0
}

.el-aside::-webkit-scrollbar {
  display: none;
}
</style>
