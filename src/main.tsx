import '@ant-design/v5-patch-for-react-19';
import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import './index.css'
import MyApp from './MyApp.tsx'
import {App, ConfigProvider} from "antd";
import {BrowserRouter} from "react-router";
import zhCN from 'antd/locale/zh_CN';

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
