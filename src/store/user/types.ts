import {z} from 'zod/v4'
import {fake_ISO} from "../../utils/regex/dateRegex.ts";
import validator from "validator";

export const user = z.object({
    contact_info: z.any(),
    created_at: z.string().regex(fake_ISO),
    department: z.string().optional().nullable(),
    email: z.email().optional().nullable(),
    faceInfo: z.base64().optional().nullable(),
    gender: z.string().optional().nullable(),
    last_login: z.string().regex(fake_ISO),
    name: z.string().optional().nullable(),
    phone: z.string().refine(validator.isMobilePhone).optional().nullable(),
    status: z.boolean(),
    updated_at: z.string().regex(fake_ISO),
    user_id: z.uuidv4(),
    username: z.string().max(20).min(5),
    work_years: z.number().optional().nullable()
})
export type userType = z.infer<typeof user>

export const permission = z.array(z.object({
    description: z.string(),
    permission_id: z.number(),
    permission_name: z.string(),
}))
export type permissionType = z.infer<typeof permission>
export const access_token = z.jwt().nullable()
export type access_tokenType = z.infer<typeof access_token>
export const refresh_token = z.jwt().nullable()
export type refresh_tokenType = z.infer<typeof refresh_token>
export const role = z.array(z.object({
    description: z.string(),
    role_id: z.number(),
    role_name: z.string(),
}))
export type roleType = z.infer<typeof role>