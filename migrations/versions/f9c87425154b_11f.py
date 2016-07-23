"""11f

Revision ID: f9c87425154b
Revises: 817f9cae0974
Create Date: 2016-07-23 09:03:43.638233

"""

# revision identifiers, used by Alembic.
revision = 'f9c87425154b'
down_revision = '817f9cae0974'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###