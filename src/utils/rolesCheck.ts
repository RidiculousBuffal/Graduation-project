import type {roleType} from "../store/user/types.ts";
import {Roles} from "../consts/roles.ts";

export const rolesCheck = (roles: roleType) => {
    for (let i = 0; i < roles.length; i++) {
        if (roles[i].role_name === Roles.ADMIN) {
            return Roles.ADMIN
        } else if (roles[i].role_name === Roles.ENGINEER) {
            return Roles.ENGINEER
        } else if (roles[i].role_name === Roles.USER) {
            return Roles.USER
        }
    }
    return Roles.USER
}