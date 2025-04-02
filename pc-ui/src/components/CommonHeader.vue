<template>
  <div class="header-container">
    <div class="header-container-left">
      <i class="el-icon-s-fold" style="color: white; font-size: 25px" @click="handleMenu"></i>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item v-for="item in tags" :key="item.path">
          {{ item.label }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="header-container-right">
      <el-avatar :src="userInfo.avator" class="avator" size="large"/>
      <el-dropdown>
        <span class="el-dropdown-link">
          {{ userInfo.name }}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>个人信息</el-dropdown-item>
          <el-dropdown-item>退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "CommonHeader",
  data(){
    return {
      userInfo: {
        name: '张三',
        avator: "../assets/logo.png"
      }
    }
  },
  methods: {
    handleMenu(){
      this.$store.commit('CollapseMenu')
    }
  },
  computed: {
    ...mapState({
      tags: state => state.tab.tabList
    })
  }
}
</script>

<style scoped>
.header-container{
  background-color: #333;
  height: 60px;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-container-left{
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-breadcrumb{
  margin-left: 15px;
}

::v-deep .el-breadcrumb__item .el-breadcrumb__inner{
  color: #666;
  font-size: 10px;
}

.header-container-right{
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.avator {
  /*width: 40px;*/
  /*height: 40px;*/
  /*border-radius: 50%;*/
  margin-right: 5px;
}

.el-dropdown-link{
  cursor: pointer;
  color: #fff;
}

</style>