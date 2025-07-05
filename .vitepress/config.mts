import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "LargePassenger Aircraft Docs",
    head:[
        ['link', {rel: 'icon', href: 'https://zlcminio.ridiculousbuffal.com/dhu/dhu.svg'}],

    ],
    vite: {
        server: {
            port: 25375
        }
    },
    description: "Api docs for largepassenger Aircraft proj",
    base: "/Graduation-project/",
    themeConfig: {
        logo:"https://zlcminio.ridiculousbuffal.com/dhu/dhu.svg",
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
