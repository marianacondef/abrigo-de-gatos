"""Adiciona coluna imagem na tabela Gato

Revision ID: a47e5f12cdb3
Revises: 
Create Date: 2025-04-15 11:27:21.813862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a47e5f12cdb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gato', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagem', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gato', schema=None) as batch_op:
        batch_op.drop_column('imagem')

    # ### end Alembic commands ###
