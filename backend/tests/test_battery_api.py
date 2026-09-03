from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_battery_schema_rejects_extra_fields():
    payload = {
        "voltage_initial": 4.2,
        "voltage_final": 3.2,
        "voltage_min": 3.2,
        "voltage_max": 4.2,
        "voltage_mean": 3.8,
        "voltage_std": 0.1,
        "voltage_drop": 1.0,
        "current_mean": -2.0,
        "current_min": -2.5,
        "current_max": -1.5,
        "current_std": 0.2,
        "temperature_initial": 25.0,
        "temperature_final": 30.0,
        "temperature_max": 30.5,
        "temperature_mean": 27.5,
        "temperature_rise": 5.0,
        "load_current_abs_mean": 2.0,
        "load_current_abs_max": 2.5,
        "load_voltage_mean": 3.8,
        "load_voltage_min": 3.2,
        "discharge_duration": 3600.0,
        "unexpected": 1.0,
    }

    response = client.post("/api/v1/battery/predict", json=payload)
    assert response.status_code == 422
