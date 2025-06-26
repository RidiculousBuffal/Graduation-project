import type {TaskType} from "@/store/task/types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {currentState} from "@/store/current/currentStore.ts";
import type {MiddlewareTypes} from "@/store/baseType.ts";
import type {InspectionRecordType} from "@/store/inspection/types.ts";

export type CurrentSlice = {
    currentTask: TaskType | null,
    setCurrentTask: (task: TaskType) => void,
    currentInspectionRecord: InspectionRecordType | null
    setCurrentInspectionRecord: (inspectionRecord: InspectionRecordType) => void
}
export const createCurrentSlice: StateCreator<currentState, MiddlewareTypes, [], CurrentSlice> = (setState, getState) => {
    return {
        currentTask: null,
        setCurrentTask: (task) => {
            setState({...getState(), currentTask: task})
        },
        currentInspectionRecord: null,
        setCurrentInspectionRecord: (inspectionRecord) => {
            setState({...getState(), currentInspectionRecord: inspectionRecord})
        }
    }
}