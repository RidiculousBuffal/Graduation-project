export interface TaskType {
    task_id: string,
    flight_id?: string,
    estimated_start?: string,
    estimated_end?: string,
    actual_start?: string,
    actual_end?: string,
    admin_id?: string,
    task_status?: string
    created_at?: string,
    updated_at?: string,
}

export interface TaskListType extends TaskType {
    aircraft_id?: string,
    aircraft_name?: string,
    admin_name?: string,
}