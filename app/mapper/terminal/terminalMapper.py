from typing import Optional

from sqlalchemy import select

from app.DTO.pagination import PaginationDTO
from app.DTO.terminals import TerminalCreateDTO, TerminalDTO, TerminalUpdateDTO, TerminalPagedResponseDTO
from app.ext.extensions import db
from app.models.terminal import Terminal


class TerminalMapper:
    @staticmethod
    def create(terminal_data: TerminalCreateDTO):
        """创建 Terminal 记录"""
        terminal = Terminal(
            terminal_name=terminal_data.terminal_name,
            description=terminal_data.description
        )
        db.session.add(terminal)
        db.session.commit()
        return TerminalDTO(
            terminal_id=terminal.terminal_id,
            terminal_name=terminal.terminal_name,
            description=terminal.description
        )

    @staticmethod
    def get_by_id(terminal_id: str):
        """根据 ID 查询 Terminal 记录"""
        terminal = db.session.get(Terminal, terminal_id)
        if terminal:
            return TerminalDTO(
                terminal_id=terminal.terminal_id,
                terminal_name=terminal.terminal_name,
                description=terminal.description
            )
        return None

    @staticmethod
    def update(terminal_id: str, update_data: TerminalUpdateDTO):
        """更新 Terminal 记录"""
        terminal = db.session.get(Terminal, terminal_id)
        if not terminal:
            return None

        if update_data.terminal_name is not None:
            terminal.terminal_name = update_data.terminal_name
        if update_data.description is not None:
            terminal.description = update_data.description

        db.session.commit()
        return TerminalDTO(
            terminal_id=terminal.terminal_id,
            terminal_name=terminal.terminal_name,
            description=terminal.description
        )

    @staticmethod
    def delete(terminal_id: str) -> bool:
        """删除 Terminal 记录"""
        terminal = db.session.get(Terminal, terminal_id)
        if not terminal:
            return False
        db.session.delete(terminal)
        db.session.commit()
        return True

    @staticmethod
    def search(
            terminal_name: str = None,
            terminal_description: Optional[str] = None,
            pageNum: int = 1,
            pageSize: int = 10,
            fuzzySearch: Optional[bool] = False,
    ):
        """分页查询 Terminal 记录"""
        query = select(Terminal)
        if terminal_name:
            query = query.where(Terminal.terminal_name.ilike(
                f'%{terminal_name}%') if fuzzySearch else Terminal.terminal_name == terminal_name)
        if terminal_description:
            query = query.where(Terminal.description.ilike(f'%{terminal_description}%'))
        query = query.order_by(Terminal.terminal_name)
        pagination = db.paginate(
            select=query,
            page=pageNum,
            per_page=pageSize,
            max_per_page=100,
            error_out=False,
            count=True
        )

        terminals_data = []
        for terminal in pagination.items:
            terminals_data.append(TerminalDTO(
                terminal_id=terminal.terminal_id,
                terminal_name=terminal.terminal_name,
                description=terminal.description
            ))

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = TerminalPagedResponseDTO(
            data=terminals_data,
            pagination=pagination_dto
        )
        return response
