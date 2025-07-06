import DefaultTheme from "vitepress/theme";
import ThemeImage from "./components/ThemeImage.vue";
import GitCard from "./components/GitCard.vue";
import AttachmentDownload from "./components/AttachmentDownload.vue";
import './index.css'
import TeamMembers from "./components/TeamMembers.vue";
import './cyberdocs-theme.css'
import {EnhanceAppContext} from "vitepress";
import Layout from "./Layout.vue";

export default {
    extends: DefaultTheme,
    Layout: Layout,
    enhanceApp({app, router}: EnhanceAppContext) {
        app.component('ThemeImage', ThemeImage)
        app.component('GitCard', GitCard)
        app.component('AttachmentDownload', AttachmentDownload)
        app.component('TeamMembers', TeamMembers)
        // 页面切换动画
        if (typeof window !== 'undefined') {
            let isTransitioning = false

            // 获取主内容区域
            const getContentElement = () => {
                return document.querySelector('.VPContent') as HTMLElement ||
                    document.querySelector('main') as HTMLElement ||
                    document.querySelector('.content') as HTMLElement
            }

            // 应用淡出效果
            const fadeOut = (element: HTMLElement) => {
                element.style.transition = 'opacity 0.2s ease-in-out'
                element.style.opacity = '0'
            }

            // 应用淡入效果
            const fadeIn = (element: HTMLElement) => {
                element.style.transition = 'opacity 0.3s ease-in-out'
                element.style.opacity = '1'
            }

            // 清理样式
            const cleanup = (element: HTMLElement) => {
                setTimeout(() => {
                    element.style.transition = ''
                }, 300)
            }

            router.onBeforeRouteChange = (to) => {
                if (isTransitioning) return

                isTransitioning = true
                const content = getContentElement()

                if (content) {
                    fadeOut(content)
                }
            }

            router.onAfterPageLoad = (to) => {
                if (!isTransitioning) return

                // 等待 DOM 更新
                setTimeout(() => {
                    const content = getContentElement()

                    if (content) {
                        // 确保元素是隐藏的
                        content.style.opacity = '0'

                        // 短暂延迟后开始淡入
                        requestAnimationFrame(() => {
                            fadeIn(content)
                            cleanup(content)
                        })
                    }

                    isTransitioning = false
                }, 50)
            }

            // 错误恢复 - 如果动画卡住了
            router.onAfterRouteChange = (to) => {
                setTimeout(() => {
                    if (isTransitioning) {
                        const content = getContentElement()
                        if (content) {
                            content.style.opacity = '1'
                            content.style.transition = ''
                        }
                        isTransitioning = false
                    }
                }, 500)
            }
        }
    }
}