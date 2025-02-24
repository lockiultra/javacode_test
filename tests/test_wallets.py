import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from api.v1.models import wallet  
from api.v1.models.base import Base
from api.v1.core.db import get_db
from api.v1.main import app
from api.v1.schemas.wallet import WalletOperation


DATABASE_URL = "sqlite+aiosqlite:///:memory:?cache=shared"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False, "uri": True},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    async def do_prepare():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(do_prepare())
    yield
    async def do_drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(do_drop())



async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_wallet():
    response = client.post("/api/v1/wallets/create")
    assert response.status_code == 200
    data = response.json()
    assert "wallet_uuid" in data
    assert data["message"] == "Wallet succesfully created"


def test_get_wallet():
    create_resp = client.post("/api/v1/wallets/create")
    wallet_uuid = create_resp.json()["wallet_uuid"]
    get_resp = client.get(f"/api/v1/wallets/{wallet_uuid}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["wallet_uuid"] == wallet_uuid
    assert data["amount"] == 0.0


def test_wallet_deposit():
    create_resp = client.post("/api/v1/wallets/create")
    wallet_uuid = create_resp.json()["wallet_uuid"]
    deposit_payload = {"operation": "DEPOSIT", "amount": 50.0}
    deposit_resp = client.post(f"/api/v1/wallets/{wallet_uuid}/operation", json=deposit_payload)
    assert deposit_resp.status_code == 200
    data = deposit_resp.json()
    assert data["message"] == "Deposit was succesfull"
    assert data["amount"] == 50.0


def test_wallet_withdraw():
    create_resp = client.post("/api/v1/wallets/create")
    wallet_uuid = create_resp.json()["wallet_uuid"]
    deposit_payload = {"operation": "DEPOSIT", "amount": 100.0}
    client.post(f"/api/v1/wallets/{wallet_uuid}/operation", json=deposit_payload)
    withdraw_payload = {"operation": "WITHDRAW", "amount": 30.0}
    withdraw_resp = client.post(f"/api/v1/wallets/{wallet_uuid}/operation", json=withdraw_payload)
    assert withdraw_resp.status_code == 200
    data = withdraw_resp.json()
    assert data["message"] == "Withdraw was succesfull"
    assert data["amount"] == 70.0


def test_wallet_withdraw_insufficient_funds():
    create_resp = client.post("/api/v1/wallets/create")
    wallet_uuid = create_resp.json()["wallet_uuid"]
    withdraw_payload = {"operation": "WITHDRAW", "amount": 10.0}
    withdraw_resp = client.post(f"/api/v1/wallets/{wallet_uuid}/operation", json=withdraw_payload)
    assert withdraw_resp.status_code == 400
    data = withdraw_resp.json()
    assert data["detail"] == "Not enough money"


def test_get_nonexistent_wallet():
    non_existent_uuid = "00000000-0000-0000-0000-000000000000"
    get_resp = client.get(f"/api/v1/wallets/{non_existent_uuid}")
    assert get_resp.status_code == 404
    data = get_resp.json()
    assert data["detail"] == "Wallet doesn't exist"
