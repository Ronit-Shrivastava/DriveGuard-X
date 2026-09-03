# DriveGuard-X FastAPI Backend

Current stage: **Battery AI integration**

The backend is deliberately modular so that the future IMU model, road model,
multimodal fusion, cause attribution and adaptive protection layers can be
added without rewriting the battery service.

## Current architecture

```text
Client
  |
  | HTTP/JSON
  v
FastAPI
  |
  +--> Battery Service
  |       |
  |       +--> Feature Schema Validation
  |       +--> Random Forest Model
  |
  +--> (future) IMU Service
  +--> (future) Road Service
  +--> (future) Fusion Engine
  +--> (future) Attribution Engine
  +--> (future) Protection Engine
```

## Important limitation

The current Battery AI model is a **cycle-level model** trained on 21
engineered discharge-cycle features. It is not yet a rolling-window
real-time model.

Therefore, the first API accepts the 21 engineered features directly.

Later, `battery_features.py` will convert a raw/windowed ESP32 or
Simulink battery stream into the exact same feature schema.

## Model artifacts

Copy these from the Kaggle notebook output:

```text
driveguard_x_final_battery_rf.joblib
final_model_metadata.json
feature_schema.json
```

into:

```text
backend/models/battery/
```

## Setup on Windows PowerShell

From the repository root:

```powershell
cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run

From `backend/`:

```powershell
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Test

```powershell
pytest
```

Health:

```powershell
curl http://127.0.0.1:8000/api/v1/health
```

Model information:

```powershell
curl http://127.0.0.1:8000/api/v1/battery/model-info
```

## Example prediction

Use Swagger `/docs` or send:

```json
{
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

  "discharge_duration": 3600.0
}
```

The numerical values above are only an API-format example. They are not
claimed to be a validated RC-car input.

## Planned expansion

The backend will grow toward:

```text
/api/v1/battery/predict
/api/v1/imu/predict
/api/v1/road/predict
/api/v1/inference
/api/v1/protection/decision
```

The combined endpoint will be added only after the individual model
interfaces are stable.

## Project rule

Do not mix model training code with API code.

Training notebooks remain under the AI/model-development part of the
repository. The backend should contain deployment/inference code and the
versioned model artifacts.
