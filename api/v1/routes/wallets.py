from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.repository.wallet import WalletRepository
from api.v1.core.db import get_db
from api.v1.schemas.wallet import WalletOperation


wallet_router = APIRouter(prefix='/wallets')


@wallet_router.post('/create')
async def create_wallet(db: AsyncSession = Depends(get_db)):
    return await WalletRepository.create_wallet(db=db)


@wallet_router.post('/{wallet_uuid}/operation')
async def wallet_operation(wallet_uuid: UUID, w_operation: WalletOperation = Depends(), db: AsyncSession = Depends(get_db)):
    return await WalletRepository.wallet_operation(db=db, wallet_uuid=wallet_uuid, operation=w_operation.operation, amount=w_operation.amount)


@wallet_router.get('/{wallet_uuid}')
async def get_wallet(wallet_uuid: UUID, db: AsyncSession = Depends(get_db)):
    return await WalletRepository.get_wallet(db=db, wallet_uuid=wallet_uuid)
