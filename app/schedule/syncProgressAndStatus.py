"""
1. 分页拉inspection -> 找到 records -> 更新progress 【process 计算方法: 拿到aircraftImageId对应的point 已经Pass的item/总point】 全部完成,即process 为100% 要更新inspection_status 和 end_time
inspection_status :
	未通过: 出现一个point对应的result 是没有passed
	已经通过 progress为100% 且全部passed
	进行中: 全部passed 但是没有满足全部的点位
2. 分页拉tasks 找到 tasks 对应的inspections 出现failed 则 failed  出现 pending 则pending 全部成功则成功

3. 分页拉flights 根据tasks 如果全部通过就是healthy 如果出现failed 则是fault

"""


from app import celery
from app.DTO.flights import FlightUpdateDTO
from app.DTO.inspections import InspectionRecordUpdateDTO
from app.DTO.tasks import TaskUpdateDTO
from app.consts.Dict import DictionaryData
from app.mapper.aircraft.aircraftReferenceImageMapper import AircraftReferenceImageMapper
from app.mapper.flight.flightMapper import FlightMapper
from app.mapper.tasks.inspectionItemMapper import InspectionItemMapper
from app.mapper.tasks.inspectionRecordMapper import InspectionRecordMapper

import datetime

from app.mapper.tasks.taskMapper import TaskMapper


# @celery.task
def sync_inspectionProgressAndStatus():
    # 1. 初始化分页
    page_num = 1
    page_size = 100

    while True:
        # 获取一页检查记录
        res = InspectionRecordMapper.search(page_num=page_num, page_size=page_size)

        # 如果当前页没有数据，说明已经处理完所有页，退出循环
        if not res.data:
            break

        for record in res.data:
            inspection_id = record.inspection_id

            # 如果没有关联的参考图，则跳过此记录，避免错误
            if not record.reference_image_id:
                continue

            image = AircraftReferenceImageMapper.get_by_id(record.reference_image_id)
            # 如果参考图不存在或没有点位信息，也跳过
            if not image or not image.image_json or not image.image_json.pointInfo:
                continue

            all_points_count = len(image.image_json.pointInfo)

            # 获取该检查任务下的所有检查项
            # 使用一个足够大的 page_size 来获取全部 item，避免分页问题
            record_items_response = InspectionItemMapper.list_by_inspection_id(inspection_id, page_size=100000)

            is_overall_passed = True
            inspected_points_count = len(record_items_response.data)  # 已检查的点 = item 的数量

            for item in record_items_response.data:
                # 如果 item 中没有任何 result，则它不可能通过
                if not item.result:
                    is_overall_passed = False
                    continue

                # 2. 修正排序逻辑：应根据 version 排序获取最新结果
                latest_result = sorted(item.result, key=lambda x: x.version, reverse=True)[0]

                # 如果最新的结果明确是未通过，则整个检查记录记为未通过
                if latest_result.isPassed is False:
                    is_overall_passed = False

            # 计算最终进度
            final_progress = int(inspected_points_count / all_points_count * 100) if all_points_count > 0 else 0

            # 准备更新的数据
            new_status = record.inspection_status
            new_end_time = record.end_time

            if final_progress >= 100:
                if is_overall_passed:
                    new_status = 'inspection_passed'
                else:
                    new_status = 'inspection_failed'
                # 3. 修正 end_time 更新逻辑：无论通过还是失败，完成时都应更新结束时间
                new_end_time = datetime.datetime.now()
            elif not is_overall_passed:
                # 只要出现了失败项，即使没完成，状态也应是 failed
                new_status = 'inspection_failed'
                new_end_time = datetime.datetime.now()
            else:
                # 进度未满100%且没有失败项，则为进行中
                new_status = 'inspection_in_progress'

            # 只有在进度或状态有变化时才执行更新，减少不必要的数据库写入
            if record.progress != final_progress or record.inspection_status != new_status:
                update_dto = InspectionRecordUpdateDTO(
                    progress=final_progress,
                    inspection_status=new_status,
                    end_time=new_end_time
                )
                InspectionRecordMapper.update(record.inspection_id, update_dto)

        # 4. 修正分页逻辑：处理完当前页后，页码加一
        page_num += 1


# @celery.task
def sync_task_status_from_inspections():
    """
    分页遍历所有Task，并根据其下所有InspectionRecord的状态来更新Task的状态。
    规则:
    - 任何一个Inspection是failed -> Task是failed
    - 没有failed但有未完成的Inspection -> Task是in_progress
    - 所有Inspection都passed -> Task是completed
    """
    print("开始同步任务状态...")
    page_num = 1
    page_size = 100

    while True:
        task_res = TaskMapper.search(page_num=page_num, page_size=page_size)
        if not task_res.data:
            break

        for task in task_res.data:
            # 获取该任务下的所有检查记录
            inspection_res = InspectionRecordMapper.search(task_id=task.task_id, page_size=10000)

            if not inspection_res.data:
                # 如果没有检查记录，则任务状态应为 '待处理'
                new_task_status = DictionaryData.TASK_PENDING['dict_key']
            else:
                has_failed = False
                completed_count = 0
                total_inspections = len(inspection_res.data)

                for inspection in inspection_res.data:
                    if inspection.inspection_status == DictionaryData.INSPECTION_FAILED['dict_key']:
                        has_failed = True
                        break  # 发现失败项，直接跳出
                    elif inspection.inspection_status == DictionaryData.INSPECTION_PASSED['dict_key']:
                        completed_count += 1

                # 根据检查结果判断任务状态
                if has_failed:
                    new_task_status = DictionaryData.TASK_FAILED['dict_key']
                elif completed_count == total_inspections:
                    new_task_status = DictionaryData.TASK_COMPLETED['dict_key']
                else:
                    new_task_status = DictionaryData.TASK_IN_PROGRESS['dict_key']

            # 如果状态有变化，则更新数据库
            if task.task_status != new_task_status:
                print(f"任务 [ID: {task.task_id}] 状态从 '{task.task_status}' 更新为 '{new_task_status}'")
                update_dto = TaskUpdateDTO(task_status=new_task_status)
                TaskMapper.update(task.task_id, update_dto)

        page_num += 1
    print("任务状态同步完成。")
    return True  # 表示成功


# @celery.task
def sync_flight_health_status_from_tasks():
    """
    分页遍历所有Flight，并根据其下所有Task的状态来更新Flight的健康状态。
    此任务应在 `sync_task_status_from_inspections` 之后执行。
    规则:
    - 任何一个Task是failed -> Flight是fault
    - 所有Task都completed -> Flight是healthy
    - 其他情况 -> Flight是pending_check
    """
    print("开始同步航班健康状态...")
    page_num = 1
    page_size = 100

    while True:
        flight_res = FlightMapper.search(pageNum=page_num, pageSize=page_size)
        if not flight_res.data:
            break

        for flight in flight_res.data:
            # 获取该航班下的所有任务
            task_res = TaskMapper.search(flight_id=flight.flight_id, page_size=1000)

            if not task_res.data:
                # 如果没有关联任务，默认是 '待检查'
                new_health_status = DictionaryData.PENDING_CHECK['dict_key']
            else:
                has_failed_task = False
                all_tasks_completed = True

                for task in task_res.data:
                    if task.task_status == DictionaryData.TASK_FAILED['dict_key']:
                        has_failed_task = True
                        break  # 发现失败任务，直接跳出

                    if task.task_status != DictionaryData.TASK_COMPLETED['dict_key']:
                        all_tasks_completed = False

                # 根据任务状态判断航班健康状态
                if has_failed_task:
                    new_health_status = DictionaryData.FAULT['dict_key']
                elif all_tasks_completed:
                    new_health_status = DictionaryData.HEALTHY['dict_key']
                else:
                    new_health_status = DictionaryData.PENDING_CHECK['dict_key']

            # 如果状态有变化，则更新数据库
            if flight.health_status != new_health_status:
                print(f"航班 [ID: {flight.flight_id}] 健康状态从 '{flight.health_status}' 更新为 '{new_health_status}'")
                update_dto = FlightUpdateDTO(health_status=new_health_status)
                FlightMapper.update(flight.flight_id, update_dto)

        page_num += 1
    print("航班健康状态同步完成。")
    return True  # 表示成功