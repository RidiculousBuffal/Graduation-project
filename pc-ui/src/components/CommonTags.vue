<template>
  <el-row type="flex" justify="start" class="tags">
    <el-tag v-for="(item, index) in tags" :key="item.path"
            :closable="item.name !== 'home'"
            size="mini"
            :style="{color: item.name === $route.name ? '#99CCFF' : '#CCCCCC', borderColor: item.name === $route.name ? '#99CCFF' : '#CCCCCC'}"
            @close="handleClose(item, index)"
            @click="handleChange(item)">
      {{ item.label }}
    </el-tag>
  </el-row>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "CommonTags",
  methods: {
    handleClose(item, idx){
      this.$store.commit('closeTag', item)
      console.log(item.name)
      console.log(this.$route)
      if(item.name === this.$route.name) {
        const len = this.tags.length
        // 删的是最后一个，跳转至前面一个
        if(len === idx){
          this.$router.push(this.tags[idx -1].path)
        }else{//否则往后跳转
          this.$router.push(this.tags[idx].path)
        }
      }
    },
    handleChange(item){
      if(this.$route.path!==item.path&&!(this.$route.path==='/home'&&(item.path==='/'))){
        this.$router.push(item.path)
      }
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
.tags{
  padding: 10px 10px;
  border: 2px solid grey;
}

.el-tag{
  margin-right: 15px;
  cursor: pointer;
  background-color: white;
}
</style>