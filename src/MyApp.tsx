import './App.css'
import LandingPage from "./pages/Landing/LandingPage.tsx";
import React from 'react';
import './App.css';
import {AuthService} from "./services/AuthService.ts";
import {Navigate, Route, Routes} from "react-router";
import Login from "./pages/Login";
import Home from "./pages/Home";
import DashBoard from "./pages/dashboard/DashBoard.tsx";
import AircraftList from "./pages/aircraft/list/AircraftList.tsx";
import AircraftType from "./pages/aircraft/type/AircraftType.tsx";
import Flight from "./pages/flight/Flight.tsx";
import My from "./pages/user/my/My.tsx";
import ModernPermissionDenied from "./pages/denied/ModernPermissionDenied.tsx";
import {Permissions} from "./consts/permissions.ts";
import Terminal from "./pages/terminal/Terminal.tsx";
import Security from "./pages/user/secure/Security.tsx";
import AircraftImageManager from "./pages/aircraft/image/AircraftImageManager.tsx";
import TaskCenter from "@/pages/tasks/TaskCenter.tsx";
import InspectionRecordCenter from "@/pages/inspection/inspectionRecords/InspectionRecordCenter.tsx";
import InspectionRecordHall from "@/pages/inspection/inspectionRecords/InspectionRecordHall.tsx";
import UserManagement from "@/pages/user/admin/user/UserManagement.tsx";
import RoleManagement from "@/pages/user/admin/role/RoleManagement.tsx";
import LogManagement from "@/pages/Audit/LogManagement.tsx";
// 受保护的路由组件
const ProtectedRoute = ({children, permission}: { children: React.ReactNode, permission?: string }) => {
    if (!AuthService.isLoggedIn()) {
        return <Navigate to="/" replace/>;
    }
    if (permission && !AuthService.checkedPermission(permission)) {
        console.log(permission)
        console.log(AuthService.checkedPermission(permission))
        return <Navigate to="/permissiondenied" replace/>;
    }
    return <>{children}</>;
};

// 公共路由组件（已登录用户将被重定向到首页）
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({children}) => {
    if (AuthService.isLoggedIn()) {
        return <Navigate to="/console" replace/>;
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
                <Route path="/console" element={<ProtectedRoute><Home/></ProtectedRoute>}>
                    <Route index element={<ProtectedRoute><DashBoard/></ProtectedRoute>}/>
                    <Route path="dashboard" element={<ProtectedRoute><DashBoard/></ProtectedRoute>}/>
                    <Route path="aircraft/list" element={<ProtectedRoute
                        permission={Permissions.AIRCRAFT_READ.permission_name}><AircraftList/></ProtectedRoute>}/>
                    <Route path="aircraft/type" element={<ProtectedRoute
                        permission={Permissions.AIRCRAFT_TYPE_READ.permission_name}><AircraftType/></ProtectedRoute>}/>
                    <Route path="aircraft/image" element={<ProtectedRoute
                        permission={Permissions.AIRCRAFT_IMAGE_READ.permission_name}><AircraftImageManager/></ProtectedRoute>}/>
                    <Route path="flight" element={<ProtectedRoute
                        permission={Permissions.FLIGHT_READ.permission_name}><Flight/></ProtectedRoute>}/>
                    <Route path="terminal" element={<ProtectedRoute
                        permission={Permissions.TERMINAL_READ.permission_name}><Terminal/></ProtectedRoute>}></Route>
                    <Route path="tasks" element={<ProtectedRoute
                        permission={Permissions.TASK_READ.permission_name}><TaskCenter></TaskCenter></ProtectedRoute>}></Route>
                    <Route path="inspection/records/:task_id" element={<ProtectedRoute
                        permission={Permissions.INSPECTION_READ.permission_name}><InspectionRecordCenter></InspectionRecordCenter></ProtectedRoute>}></Route>
                    <Route path="inspection/hall" element={<ProtectedRoute
                        permission={Permissions.INSPECTION_READ.permission_name}><InspectionRecordHall></InspectionRecordHall></ProtectedRoute>}></Route>
                    <Route path="user/my" element={<ProtectedRoute
                        permission={Permissions.PROFILE_READ.permission_name}><My/></ProtectedRoute>}/>
                    <Route path="user/security" element={<ProtectedRoute
                        permission={Permissions.PROFILE_READ.permission_name}><Security/></ProtectedRoute>}/>
                    <Route path="admin/userlist"
                           element={<ProtectedRoute
                               permission={Permissions.USER_READ_ALL.permission_name}><UserManagement/></ProtectedRoute>}/>
                    <Route path="admin/rolePermission" element={<ProtectedRoute
                        permission={Permissions.PERMISSIONS_MANAGEMENT.permission_name}><RoleManagement></RoleManagement></ProtectedRoute>}></Route>
                    <Route path="admin/log" element={<ProtectedRoute
                        permission={Permissions.LOG_READ.permission_name}><LogManagement/></ProtectedRoute>}></Route>
                </Route>
                <Route path="/permissiondenied" element={<ModernPermissionDenied/>}/>
                <Route path="*" element={<Navigate to="/" replace/>}/>
            </Routes>
        </>
    )
}

export default MyApp
