import {z} from 'zod/v4'
import type {aircraftType_} from "../aircraft/types.ts";
import type {terminalType} from "../terminal/types.ts";

export const flight = z.object({
    flight_id: z.uuidv4().or(z.string()).nullable().nullish(),
    aircraft_id: z.uuidv4().nullable().nullish(),
    terminal_id: z.uuidv4().nullable().nullish(),
    estimated_departure: z.string().nullable().nullish(),
    estimated_arrival: z.string().nullable().nullish(),
    flight_status: z.string().nullable().nullish(),
    actual_departure: z.string().nullable().nullish(),
    actual_arrival: z.string().nullable().nullish(),
    health_status: z.string().nullable().nullish(),
    approval_status: z.string().nullable().nullish(),
})

export type flightType = z.infer<typeof flight>
export type flightListType = flightType & Pick<aircraftType_, 'aircraft_name'> & Pick<terminalType, 'terminal_name'>
