from uuid import uuid4

from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from api.v1.models.base import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    wallet_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    amount: Mapped[float] = mapped_column(Float)

