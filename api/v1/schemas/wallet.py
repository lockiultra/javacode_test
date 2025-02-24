from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class OperaionTypeEnum(str, Enum):
    deposit: str = 'DEPOSIT'
    withdraw: str = 'WITHDRAW'


class Wallet(BaseModel):
    wallet_uuid: UUID
    amount: float = Field(..., ge=0.0)

    model_config = {'from_attributes': True}


class WalletOperation(BaseModel):
    operation: OperaionTypeEnum = Field(...)
    amount: float = Field(..., ge=0.0)


