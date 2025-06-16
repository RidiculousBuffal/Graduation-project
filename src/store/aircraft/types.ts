import {z} from 'zod/v4'

export const aircraftType = z.object({
    typeid: z.uuidv4(),
    type_name: z.string(),
    description: z.string()
})
export type aircraftTypeType = z.infer<typeof aircraftType>
export const aircraft = z.object({
        aircraft_id: z.uuidv4(),
        aircraft_name: z.string(),
        age: z.int(),
        typeid: z.uuidv4()
    }
)
export type aircraftType_ = z.infer<typeof aircraft> //防止和aircraftType冲突
export type AircraftArrayType = Array<aircraftTypeType & aircraftType_>