import Vue from "vue";
import Router from 'vue-router'
import Home from "@/views/Home";
import Main from "@/views/Main";
import AirlineManage from "@/views/AirlineManage";
import DetectRecord from "@/views/DetectRecord";
import DetectModel from "@/views/DetectModel";
import Task from "@/views/Task";
import Engineer from "@/views/Engineer";
import Dictionary from "@/views/Dictionary";
import Login from "@/views/Login";


Vue.use(Router)

const routes = [
    {
        path: '/',
        component: Main,
        redirect: '/home',
        children: [
            {path:'home', name: 'Home', component: Home},
            {path:'airline', name: 'airline', component: AirlineManage},
            {path:'task', name: 'task', component: Task},
            {path:'detectRecord', name: 'detectRecord', component: DetectRecord},
            {path:'detectModel', name: 'detectModel', component: DetectModel},
            {path:'engineer', name: 'engineer', component: Engineer},
            {path:'dictionary', name: 'dictionary', component: Dictionary},
        ]
    },
    {path:'/login',
     name:'login',
     component:Login
    }

]

// 防止连续点击多次路由报错
let routerPush = Router.prototype.push;
let routerReplace = Router.prototype.replace;
// push
Router.prototype.push = function push(location) {
    return routerPush.call(this, location).catch(err => err)
}
// replace
Router.prototype.replace = function push(location) {
    return routerReplace.call(this, location).catch(err => err)
}

const router = new Router({
    mode: 'history',
    scrollBehavior: () => ({ y: 0 }),
    routes: routes // (缩写) 相当于 routes: routes
})

export default router

