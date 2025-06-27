export type Role = {
    role_id: number,
    role_name: string,
    description: string,
}
export type Permission = {
    permission_id: number,
    permission_name: string,
    description: string,
}
export type RolePermission = {
    role: Role,
    permissions: Permission[]
}

export interface AdminUserDTO {
    user_id: string;
    username: string;
    email?: string;
    phone?: string;
    faceInfo?: string;
    status?: boolean;
    last_login?: Date ;
    created_at?: Date ;
    updated_at?: Date ;
    name?: string;
    gender?: string;
    department?: string;
    work_years?: string;
    contact_info?: string;
}

export interface AdminUserDTOWithRolesAndPermissions extends AdminUserDTO {
    roles: Role[],
    permissions: Permission[]
}