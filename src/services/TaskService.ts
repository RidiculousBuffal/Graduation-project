import {BaseService} from "./BaseService.ts";
import {
    createTask,
    searchTask,
    deleteTask,
    type createTaskPayload,
    type SearchTaskPayload,
    updateTask,
    type updateTaskPayload, getTaskById
} from "../api/taskapi.ts";
import {useTaskStore} from "../store/task/taskStore.ts";
import {getAllImageInOneFlight} from "@/api/flightapi.ts";
import {useCurrentStore} from "@/store/current/currentStore.ts";

export class TaskService extends BaseService {
    public static async getTaskList(params: SearchTaskPayload) {
        const payload = {
            ...params,
            ...useTaskStore.getState().tasksPagination
        }
        const searchData = await searchTask(payload)
        return this.processResultSync(
            searchData,
            () => {
                useTaskStore.getState().setTasks(
                    searchData?.data!
                );
                useTaskStore.getState().setTasksPagination(
                    searchData?.pagination!
                )
            }
        )
    }

    public static async createTask(task: createTaskPayload) {
        const res = await createTask(task)
        return this.processResultAsync(res,
            async () => {
                await this.getTaskList({})
            }
        )
    }

    public static async updateTask(task: updateTaskPayload) {
        const res = await updateTask(task)
        return this.processResultSync(res,
            () => {
                useTaskStore.getState().updateTask(task)
            }
        )
    }

    public static async deleteTask(taskId: string) {
        const res = await deleteTask(taskId)
        return await this.processResultAsync(res, async () => {
            await this.getTaskList({})
        })
    }

    public static async getTaskById(taskId: string) {
        return await getTaskById(taskId)
    }

    public static async getAircraftImageByTaskId(taskId: string) {
        const task = await getTaskById(taskId)
        if (task) {
            return await getAllImageInOneFlight(task.flight_id!)
        } else {
            return null;
        }
    }

    public static async getCurrentTaskReferenceAircraftImage() {
        const task = useCurrentStore.getState().currentTask
        if (task) {
            return await getAllImageInOneFlight(task.flight_id!)
        } else {
            return null;
        }
    }
}
