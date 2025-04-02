<template>
  <div>
    <el-menu default-active="1-4-1" class="el-menu-vertical-demo"
             @open="handleOpen" @close="handleClose" :collapse="isCollapse"
             background-color="#545c64"
             text-color="#fff"
             active-text-color="#ffd04b">

      <div class="system-tilte">
        <i class="el-icon-s-promotion"></i>
        <h3 v-if="!isCollapse">管理系统</h3>
      </div>
      <el-menu-item @click="clickMenu(item)" v-for="item in menuList" :key="item.name" :index="item.name">
        <i :class="`el-icon-${item.icon}`"></i>
        <span slot="title">{{ item.label }}</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "CommonAside",
  data() {
    return {
      menuList: [
        {
          path: '/',
          name: 'home',
          label: '首页',
          icon: 's-home',
          url: 'Home/Home'
        },
        {
          path: '/airline',
          name: 'airline',
          label: '航线管理',
          icon: 'video-play',
          url: 'AirlineManage/AirlineManage'
        },
        {
          path: '/task',
          name: 'task',
          label: '任务列表',
          icon: 'document',
          url: 'Task/Task'
        },
        {
          path: '/detectRecord',
          name: 'detectRecord',
          label: '检测记录',
          icon: 'notebook-2',
          url: 'DetectRecord/DetectRecord'
        },
        {
          path: '/detectModel',
          name: 'detectModel',
          label: '检测模型管理',
          icon: 'monitor',
          url: 'DetectModel/DetectModel'
        },
        {
          path: '/engineer',
          name: 'engineer',
          label: '工程师管理',
          icon: 'user',
          url: 'Engineer/Engineer'
        },
        {
          path: '/dictionary',
          name: 'dictionary',
          label: '字典管理',
          icon: 'bank-card',
          url: 'Dictionary/Dictionary'
        }

      ]
    };
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    clickMenu(item){
      // 防止自己跳自己的报错
      if(this.$route.path!==item.path&&!(this.$route.path==='/home'&&(item.path==='/'))){
        this.$router.push(item.path)
      }
      // 更新面包屑
      this.$store.commit('SelectMenu', item)
    }
  },
  computed: {
    isCollapse() {
      return this.$store.state.tab.isCollapse
    }
  }
}
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 100%;
  text-align: left;
}

.el-menu{
  height: 100vh;;
}

/*.h3{*/
/*  text-align: center;*/
/*  line-height: 48px;*/
/*  color: #fff;*/
/*  font-size: 16px;*/
/*  font-weight: 400;*/
/*  background-color: #545c64;*/
/*}*/

.system-tilte{
  width: 100%;
  height: 80px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  background-color: #545c64;
  line-height: 48px;
  color: #fff;
  font-size: 16px;
  font-weight: 400;
}
</style>