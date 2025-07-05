import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "LargePassenger Aircraft Docs",
    vite: {
        server: {
            port: 25375
        }
    },
    description: "Api docs for largepassenger Aircraft proj",
    base: "/Graduation-project/",
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {text: '首页', link: '/'},
            {text: "项目说明", link: '/docs/env/index.md'},
            {text: '接口文档', link: '/markdown-examples'}
        ],


        socialLinks: [
            {icon: 'github', link: 'https://github.com/RidiculousBuffal/Graduation-project'}
        ],
        sidebar: {
            '/docs/env/': [
                {text: "开始", link: '/docs/env/index'},
                {text: "技术架构", link: "/docs/env/architecture"}
            ]
        }
    }
})
