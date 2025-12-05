import pytest
from fastapi.testclient import TestClient
from main import app
from database import DB_PATH, init_db

client = TestClient(app)

# ---------------- Test DB Setup ----------------
@pytest.fixture(autouse=True)
def setup_and_teardown():
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
    yield
    if DB_PATH.exists():
        DB_PATH.unlink()

# ---------------- Tests ----------------
def test_create_and_get_vehicle():
    payload = {
        "vin": "a1b2c3",
        "manufacturer": "TestAuto",
        "description": "A test car",
        "horse_power": 120,
        "model_name": "T-Car",
        "model_year": 2020,
        "purchase_price": 15000.0,
        "fuel_type": "Gas"
    }
    r = client.post("/vehicle", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["vin"] == "A1B2C3"

    r2 = client.get("/vehicle")
    assert r2.status_code == 200
    assert any(v["vin"] == "A1B2C3" for v in r2.json())

def test_vin_case_insensitive_uniqueness():
    payload = {
        "vin": "uniqueVIN",
        "manufacturer": "X",
        "description": "",
        "horse_power": 100,
        "model_name": "M",
        "model_year": 2019,
        "purchase_price": 10000,
        "fuel_type": "Electric"
    }
    r = client.post("/vehicle", json=payload)
    assert r.status_code == 201

    payload["vin"] = "UNIQUEvin"
    r2 = client.post("/vehicle", json=payload)
    assert r2.status_code == 422

def test_update_and_delete():
    payload = {
        "vin": "delVIN",
        "manufacturer": "D",
        "description": "to delete",
        "horse_power": 90,
        "model_name": "Del",
        "model_year": 2018,
        "purchase_price": 8000,
        "fuel_type": "Gas"
    }
    r = client.post("/vehicle", json=payload)
    assert r.status_code == 201

    upd = {"manufacturer": "D-up"}
    r2 = client.put(f"/vehicle/{payload['vin']}", json=upd)
    assert r2.status_code == 200
    assert r2.json()["manufacturer"] == "D-up"

    r3 = client.delete(f"/vehicle/{payload['vin']}")
    assert r3.status_code == 204

    r4 = client.get(f"/vehicle/{payload['vin']}")
    assert r4.status_code == 404
