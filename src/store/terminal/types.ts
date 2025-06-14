import {z} from 'zod/v4'
export const terminal = z.object({
    terminal_name:z.string(),
    terminal_id:z.uuidv4(),
    description:z.string().nullable(),
})
export type terminalType = z.infer<typeof terminal>
