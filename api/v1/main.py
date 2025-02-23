from fastapi import FastAPI, APIRouter

from api.v1.routes.wallets import wallet_router


app = FastAPI()
router = APIRouter(prefix='/api/v1')


@router.get('/')
async def root():
    return {'message': 'Wallets API is started'}


router.include_router(wallet_router)
app.include_router(router)
