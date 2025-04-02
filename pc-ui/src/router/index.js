import Vue from "vue";
import VueRouter from 'vue-router'
import Home from "@/views/Home";
import Main from "@/views/Main";
import AirlineManage from "@/views/AirlineManage";
import DetectRecord from "@/views/DetectRecord";
import DetectModel from "@/views/DetectModel";
import Task from "@/views/Task";
import Engineer from "@/views/Engineer";
import Dictionary from "@/views/Dictionary";


Vue.use(VueRouter)

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

]

const router = new VueRouter({
    routes // (缩写) 相当于 routes: routes
})

export default router

