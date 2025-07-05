---
# https://vitepress.dev/reference/default-theme-home-page
layout: home
title: "首页"
hero:
  name: "LargePassenger Aircraft API Doc"
  text: "大飞机检测项目接口文档"
  image:
    src: /Airplane.svg


features:
  - title: 后端
    details: 基于python 3.12 使用Flask构建
  - title: 前端
    details: 基于React 19 + typescript + antdesign 使用 vite 构建
  - title: 中间件
    details: 集成IPFS去中心化存储,redis消息队列,hardhat区块链网络
---

<script setup>
    const members = [
        {
            avatar:"/avatar/frank.jpg",
            name:"Frank Li",
            title:"Guide Teacher"
        },
        {
            avatar:"/avatar/chai.jpg",
            name:"Zijian Chai",
            title:"Tutor | Yolo Expert"
        },
        {
            avatar:"/avatar/cow.jpg",
            name:"Licheng Zhou",
            title:"FullStack Developer"
        },
        {
            avatar:"/avatar/dai.jpg",
            name:"Charlie Dai",
            title:"APP Developer"
        },
        
        {
            avatar:"/avatar/qifeng.jpg",
            name:"起风的季节",
            title:"Backend Developer"
        },
        {
            avatar:"/avatar/mu.jpg",
            name:"木矞",
            title:"Frontend (Vue Team) Developer"
        },
        {
            avatar:"/avatar/fuchun.jpg",
            name:"付春",
            title:"Frontend (Vue Team) Developer"
        },
        {
            avatar:"/avatar/ruiming.jpg",
            name:"Ruimin Zhou",
            title:"Frontend (Vue Team) Developer"
        },
    ]
</script>


--- 

# 团队成员

<TeamMembers :members="members"></TeamMembers>