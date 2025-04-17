"""change image_id to str uuid

Revision ID: 10f9c48a1821
Revises: 77ac3d43706c
Create Date: 2025-04-17 19:27:32.816457
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '10f9c48a1821'
down_revision = '77ac3d43706c'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands to handle foreign key constraints and column type change ###
    # 1. 删除外键约束
    with op.batch_alter_table('inspection_records', schema=None) as batch_op:
        batch_op.drop_constraint('inspection_records_ibfk_5', type_='foreignkey')

    # 2. 修改 aircraft_reference_image 表的 image_id 类型
    with op.batch_alter_table('aircraft_reference_image', schema=None) as batch_op:
        batch_op.alter_column('image_id',
                              existing_type=mysql.BIGINT(display_width=20),
                              type_=sa.String(length=50),
                              existing_comment='图片ID',
                              existing_nullable=False)

    # 3. 修改 inspection_records 表的 reference_image_id 类型
    with op.batch_alter_table('inspection_records', schema=None) as batch_op:
        batch_op.alter_column('reference_image_id',
                              existing_type=mysql.BIGINT(display_width=20),
                              type_=sa.String(length=50),
                              existing_nullable=True)

    # 4. 重新添加外键约束
    with op.batch_alter_table('inspection_records', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'inspection_records_ibfk_5',  # 外键名称，与原来一致
            'aircraft_reference_image',   # 引用的表
            ['reference_image_id'],       # 本表字段
            ['image_id']                  # 引用表字段
        )
    # ### end Alembic commands ###

def downgrade():
    # ### commands to revert changes ###
    # 1. 删除外键约束
    with op.batch_alter_table('inspection_records', schema=None) as batch_op:
        batch_op.drop_constraint('inspection_records_ibfk_5', type_='foreignkey')

    # 2. 恢复 inspection_records 表的 reference_image_id 类型
    with op.batch_alter_table('inspection_records', schema=None) as batch_op:
        batch_op.alter_column('reference_image_id',
                              existing_type=sa.String(length=50),
                              type_=mysql.BIGINT(display_width=20),
                              existing_nullable=True)

    with op.batch_alter_table('aircraft_reference_image', schema=None) as batch_op:
        batch_op.alter_column('image_id',
                              existing_type=sa.String(length=50),
                              type_=mysql.BIGINT(display_width=20),
                              existing_comment='图片ID',
                              existing_nullable=False)
    with op.batch_alter_table('inspection_records', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'inspection_records_ibfk_5',
            'aircraft_reference_image',
            ['reference_image_id'],
            ['image_id']
        )
    # ### end Alembic commands ###