from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from api.v1.models.wallet import Wallet


class WalletRepository:
    @classmethod
    async def create_wallet(cls, db: AsyncSession):
        new_wallet = Wallet(amount=0.0)
        db.add(new_wallet)
        await db.commit()
        await db.refresh(new_wallet)
        return {
            'message': 'Wallet succesfully created',
            'wallet_uuid': new_wallet.wallet_uuid
        }
    
    @classmethod
    async def wallet_operation(cls, db: AsyncSession, wallet_uuid: UUID, operation: str, amount: float):
        wallet = await db.execute(select(Wallet).where(Wallet.wallet_uuid == wallet_uuid).with_for_update())
        wallet = wallet.scalars().first()
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wallet doesn\'t exist')
        if operation == 'DEPOSIT':
            wallet.amount += amount
            await db.commit()
            await db.refresh(wallet)
            return {
                'message': 'Deposit was succesfull',
                'wallet_uuid': wallet_uuid,
                'amount': wallet.amount
            }
        elif operation == 'WITHDRAW':
            if wallet.amount < amount:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough money')
            wallet.amount -= amount
            await db.commit()
            await db.refresh(wallet)
            return {
                'message': 'Withdraw was succesfull',
                'wallet_uuid': wallet_uuid,
                'amount': wallet.amount
            }
        else:
            raise HTTPException(status_code=400, detail='Unknown operation')
        
    @classmethod
    async def get_wallet(cls, db: AsyncSession, wallet_uuid: UUID):
        wallet = await db.execute(select(Wallet).where(Wallet.wallet_uuid == wallet_uuid).with_for_update())
        wallet = wallet.scalars().first()
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wallet doesn\'t exist')
        return {
            'wallet_uuid': wallet.wallet_uuid,
            'amount': wallet.amount
        }
