import 'overlayscrollbars/overlayscrollbars.css';
import {
    OverlayScrollbars,
    ScrollbarsHidingPlugin,
    SizeObserverPlugin,
    ClickScrollPlugin
} from 'overlayscrollbars';
import '@ant-design/v5-patch-for-react-19';
import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import './index.css'
import MyApp from './MyApp.tsx'
import {App, ConfigProvider} from "antd";

import zhCN from 'antd/locale/zh_CN';
import {BrowserRouter} from "react-router";

// 全局初始化 OverlayScrollbars
OverlayScrollbars.plugin([
    ScrollbarsHidingPlugin,
    SizeObserverPlugin,
    ClickScrollPlugin
]);

// 为 body 元素应用 OverlayScrollbars
document.addEventListener('DOMContentLoaded', () => {
    OverlayScrollbars(document.body, {
        overflow: {
            x: 'hidden',
            y: 'scroll'
        },
        scrollbars: {
            theme: 'os-theme-dark',
            visibility: 'auto',
            autoHide: 'move',
            autoHideDelay: 1300
        }
    });
});

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <BrowserRouter>
            <ConfigProvider locale={zhCN} theme={{
                token: {
                    colorPrimary: '#d9d3d3',
                    borderRadius: 8,
                    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                },
            }}>
                <App>
                    <MyApp/>
                </App>
            </ConfigProvider>
        </BrowserRouter>
    </StrictMode>
)