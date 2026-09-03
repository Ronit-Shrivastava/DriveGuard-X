from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    BatteryFeatureVector,
    BatteryPredictionResponse,
    ModelInfoResponse,
)
from app.services.battery_service import predict_battery_soh
from app.services.model_loader import get_battery_model_info


router = APIRouter()


@router.get("/health", tags=["system"])
def health():
    info = get_battery_model_info()
    return {
        "status": "ok",
        "battery_model_loaded": info["loaded"],
    }


@router.get(
    "/battery/model-info",
    response_model=ModelInfoResponse,
    tags=["battery"],
)
def battery_model_info():
    return get_battery_model_info()


@router.post(
    "/battery/predict",
    response_model=BatteryPredictionResponse,
    tags=["battery"],
)
def battery_predict(features: BatteryFeatureVector):
    try:
        return predict_battery_soh(features)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
