import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from "@/router";
import store from "@/store";
import plugins from "@/plugins";
// 自定义表格工具组件
import RightToolbar from "@/components/RightToolbar";
// 分页组件
import Pagination from "@/components/Pagination";
//重置查询表单
import {resetForm} from "@/api/utils/common";

// 全局组件挂载
Vue.component('RightToolbar', RightToolbar)
Vue.component('Pagination', Pagination)

// 全局方法挂载
Vue.prototype.resetForm = resetForm

Vue.config.productionTip = false


Vue.use(ElementUI);
Vue.use(plugins)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
