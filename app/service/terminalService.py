from typing import Optional

from sqlalchemy.exc import IntegrityError

from app.DTO.terminals import TerminalCreateDTO, TerminalUpdateDTO, TerminalDTO
from app.consts.Terminals import TerminalConsts
from app.mapper.terminal.terminalMapper import TerminalMapper
from app.models.response import ResponseModel


class TerminalService:
    @staticmethod
    def create_terminal(terminal_data: TerminalCreateDTO) -> ResponseModel:
        """创建航站楼记录"""
        # 参数校验
        if not terminal_data.terminal_name:
            return ResponseModel.fail(
                msg=TerminalConsts.INVALID_TERMINAL_DATA,
                data={"error": "航站楼名称不能为空"}
            )

        try:
            # 检查航站楼名称是否已存在
            existing_terminal = TerminalMapper.search(terminal_name=terminal_data.terminal_name)
            if len(existing_terminal.data) > 0:
                return ResponseModel.fail(
                    msg=TerminalConsts.TERMINAL_ALREADY_EXISTS
                )
            result = TerminalMapper.create(terminal_data)
            return ResponseModel.success(
                msg=TerminalConsts.ADD_TERMINAL_SUCCESS,
                data=result.model_dump()
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=TerminalConsts.ADD_TERMINAL_ERROR,
                data={"error": str(e)}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=TerminalConsts.ADD_TERMINAL_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def get_terminal_by_id(terminal_id: str) -> ResponseModel:
        """根据ID获取航站楼记录"""
        if not terminal_id:
            return ResponseModel.fail(
                msg=TerminalConsts.INVALID_TERMINAL_DATA,
                data={"error": "航站楼ID不能为空"}
            )

        result: Optional[TerminalDTO] = TerminalMapper.get_by_id(terminal_id)
        if result:
            return ResponseModel.success(
                msg=TerminalConsts.GET_TERMINAL_SUCCESS,
                data=result.model_dump()
            )
        return ResponseModel.fail(
            msg=TerminalConsts.GET_TERMINAL_NOT_FOUND,
            data={"error": f"未找到ID为{terminal_id}的航站楼"}
        )

    @staticmethod
    def update_terminal(terminal_id: str, update_data: TerminalUpdateDTO) -> ResponseModel:
        """更新航站楼记录"""
        if not terminal_id:
            return ResponseModel.fail(
                msg=TerminalConsts.INVALID_TERMINAL_DATA,
                data={"error": "航站楼ID不能为空"}
            )

        try:
            # 检查更新后的名称是否已存在
            if update_data.terminal_name:
                existing_terminal = TerminalMapper.search(terminal_name=update_data.terminal_name)
                if len(existing_terminal.data) > 0 and existing_terminal.data[0].terminal_id != terminal_id:
                    return ResponseModel.fail(
                        msg=TerminalConsts.TERMINAL_ALREADY_EXISTS
                    )
            result: Optional[TerminalDTO] = TerminalMapper.update(terminal_id, update_data)
            if result:
                return ResponseModel.success(
                    msg=TerminalConsts.UPDATE_TERMINAL_SUCCESS,
                    data=result.model_dump()
                )
            return ResponseModel.fail(
                msg=TerminalConsts.UPDATE_TERMINAL_ERROR,
                data={"error": f"未找到ID为{terminal_id}的航站楼或更新失败"}
            )
        except IntegrityError as e:
            return ResponseModel.fail(
                msg=TerminalConsts.UPDATE_TERMINAL_ERROR,
                data={"error": str(e)}
            )
        except Exception as e:
            return ResponseModel.fail(
                msg=TerminalConsts.UPDATE_TERMINAL_ERROR,
                data={"error": str(e)}
            )

    @staticmethod
    def delete_terminal(terminal_id: str) -> ResponseModel:
        """删除航站楼记录"""
        if not terminal_id:
            return ResponseModel.fail(
                msg=TerminalConsts.INVALID_TERMINAL_DATA,
                data={"error": "航站楼ID不能为空"}
            )

        success = TerminalMapper.delete(terminal_id)
        if success:
            return ResponseModel.success(
                msg=TerminalConsts.DELETE_TERMINAL_SUCCESS,
                data=None
            )
        return ResponseModel.fail(
            msg=TerminalConsts.DELETE_TERMINAL_ERROR,
            data={"error": f"未找到ID为{terminal_id}的航站楼或删除失败"}
        )

    @staticmethod
    def search_terminal(
            terminal_name: Optional[str] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> ResponseModel:
        """分页查询航站楼记录"""
        if page_num < 1 or page_size < 1:
            return ResponseModel.fail(
                msg=TerminalConsts.INVALID_TERMINAL_DATA,
                data={"error": "页码和每页大小必须大于0"}
            )

        result = TerminalMapper.search(
            terminal_name=terminal_name,
            pageNum=page_num,
            pageSize=page_size
        )
        return ResponseModel.success(
            msg=TerminalConsts.SEARCH_TERMINAL_SUCCESS,
            data=result.model_dump()
        )
