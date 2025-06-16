import {z} from 'zod/v4'

export const aircraftType = z.object({
    typeid: z.uuidv4(),
    type_name: z.string(),
    description: z.string()
})
export type aircraftTypeType = z.infer<typeof aircraftType>
