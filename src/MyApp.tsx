import './App.css'
import LandingPage from "./pages/Landing/LandingPage.tsx";
import React from 'react';
import './App.css';
import {AuthService} from "./services/AuthService.ts";
import {Navigate, Route, Routes} from "react-router";
import Login from "./pages/Login";
import Home from "./pages/Home";

// 受保护的路由组件
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({children}) => {
    if (!AuthService.isLoggedIn()) {
        return <Navigate to="/" replace/>;
    }
    return <>{children}</>;
};

// 公共路由组件（已登录用户将被重定向到首页）
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({children}) => {
    if (AuthService.isLoggedIn()) {
        return <Navigate to="/home" replace/>;
    }
    return <>{children}</>;
};

function MyApp() {
    return (
        <>
            <Routes>
                <Route path="/" element={<LandingPage/>}/>
                <Route
                    path="/login"
                    element={
                        <PublicRoute>
                            <Login/>
                        </PublicRoute>
                    }
                />
                <Route
                    path="/home"
                    element={
                        <ProtectedRoute>
                            <Home/>
                        </ProtectedRoute>
                    }
                />
                <Route path="*" element={<Navigate to="/" replace/>}/>
            </Routes>
        </>
    )
}

export default MyApp
