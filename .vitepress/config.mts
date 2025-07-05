import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "LargePassenger Aircraft",
    head: [
        ['link', {rel: 'icon', href: 'https://zlcminio.ridiculousbuffal.com/dhu/dhu.svg'}],

    ],
    vite: {
        server: {
            port: 25375
        }
    },
    lang: "zh-CN",
    lastUpdated: true,
    description: "Api docs for largepassenger Aircraft proj",
    base: "/Graduation-project/",
    themeConfig: {
        editLink: {
            pattern: ({filePath}) => {
                return `https://github.com/RidiculousBuffal/Graduation-project/tree/docs/${filePath}`
            },
            text:"在github上编辑本页面"
        },
        outline: [1, 6],
        logo: "https://zlcminio.ridiculousbuffal.com/dhu/dhu.svg",
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {text: '首页', link: '/'},
            {text: "项目说明", link: '/docs/env/index.md'},
            {text: '接口文档', link: '/docs/api/index.md'},
        ],
        search: {
            provider: 'local'
        },
        footer: {
            message: 'Released under the MIT License.',
            copyright: 'Copyright © 2025-present Licheng Zhou'
        },

        socialLinks: [
            {icon: 'github', link: 'https://github.com/RidiculousBuffal/Graduation-project'}
        ],
        sidebar: {
            '/docs/env/': [
                {text: "开始", link: '/docs/env/index'},
                {text: "技术架构", link: "/docs/env/architecture"},
                {text: "Apifox调试", link: "/docs/env/apifox"},
                {text: "环境变量配置", link: "/docs/env/config"},
            ],
            '/docs/api': [
                {text: "开始", link: "/docs/api/index"},
                {text: "登录/注册/刷新令牌", link: "/docs/api/auth"},
                {text: "飞机 aircraft", link: "/docs/api/aircraft"},
                {text: "飞机类型", link: "/docs/api/aircraftType"},
                {text: "飞机底图", link: "/docs/api/aircraft_image"},
                {text: "航站楼", link: "/docs/api/terminal"},
                {text: "ipfs", link: "/docs/api/ipfs"},
                {text:"字典",link:"/docs/api/dict"},
                {text:"航班",link:"/docs/api/flight"},
                {text:"工程师",link:"/docs/api/engineers"},
            ]
        }
    }
})
