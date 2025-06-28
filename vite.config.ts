import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src')
        }
    },
    server: {
        port: 13744
    },
    build: {
        // 启用 CSS 代码分割
        cssCodeSplit: true,
        // 启用 gzip 压缩提示
        reportCompressedSize: true,
        // 设置打包块大小警告限制
        chunkSizeWarningLimit: 1000,
        rollupOptions: {
            output: {
                // 手动分割代码块
                manualChunks: {
                    // React 相关
                    'react-vendor': ['react', 'react-dom'],
                    // 路由相关
                    'router': ['react-router'],
                    // UI 组件库
                    'antd': ['antd', '@ant-design/v5-patch-for-react-19'],
                    'lobe-ui': ['@lobehub/ui'],
                    // 3D 图形库
                    'three': ['three', '@react-three/fiber', '@react-three/drei'],
                    // 工具库
                    'utils': ['validator', 'immer', 'qs', 'zod'],
                    // 状态管理
                    'store': ['zustand'],
                    // 图标库
                    'icons': ['lucide-react', 'react-nice-avatar'],
                },
                chunkFileNames: 'assets/js/[name]-[hash].js',
                entryFileNames: 'assets/js/[name]-[hash].js'
            }
        },
        // 压缩配置
        minify: 'terser',
        terserOptions: {
            compress: {
                // 删除 console.log
                drop_console: true,
                // 删除 debugger
                drop_debugger: true,
                // 删除未使用的代码
                pure_funcs: ['console.log']
            }
        }
    },
    // 优化依赖预构建
    optimizeDeps: {
        include: [
            'react',
            'react-dom',
            'antd',
            'lucide-react',
            'three',
            '@react-three/fiber',
            '@react-three/drei'
        ],
        exclude: [
            // 排除大型库的预构建，让它们在运行时按需加载
        ]
    },
    // 静态资源处理
    assetsInclude: ['**/*.gltf', '**/*.glb', '**/*.fbx'],
    // 定义全局常量，用于生产环境优化
    define: {
        __DEV__: JSON.stringify(process.env.NODE_ENV !== 'production')
    }
})