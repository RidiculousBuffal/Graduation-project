export interface InspectionRecordType {
    inspection_id: string,
    inspection_name: string,
    task_id: string,
    executor_id: string,
    progress: number,
    start_time: string,
    end_time: string,
    inspection_status: string,
    reference_image_id: string,
    created_at: string,
    updated_at: string,
}

export interface InspectionRecordListType extends InspectionRecordType {
    aircraft_id?: string,
    aircraft_name?: string,
    executor_name?: string,
    flight_id: string
    reference_image_name: string
    status_name: string,
}