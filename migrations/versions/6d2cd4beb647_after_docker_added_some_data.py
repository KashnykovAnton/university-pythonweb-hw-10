"""After docker added some data

Revision ID: 6d2cd4beb647
Revises: b5f4b3fddedb
Create Date: 2025-04-03 01:33:38.849734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d2cd4beb647'
down_revision: Union[str, None] = 'b5f4b3fddedb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
