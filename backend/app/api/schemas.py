from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BatteryFeatureVector(BaseModel):
    """
    Exact 21-feature input expected by the current final Battery AI model.

    Important:
    This model is a cycle-level model. These are engineered discharge-cycle
    features, not instantaneous ESP32 readings.
    """

    model_config = ConfigDict(extra="forbid")

    voltage_initial: float
    voltage_final: float
    voltage_min: float
    voltage_max: float
    voltage_mean: float
    voltage_std: float
    voltage_drop: float

    current_mean: float
    current_min: float
    current_max: float
    current_std: float

    temperature_initial: float
    temperature_final: float
    temperature_max: float
    temperature_mean: float
    temperature_rise: float

    load_current_abs_mean: float
    load_current_abs_max: float
    load_voltage_mean: float
    load_voltage_min: float

    discharge_duration: float


class BatteryPredictionResponse(BaseModel):
    model: str
    soh: float = Field(description="Predicted State of Health on the model's 0-1 scale.")
    soh_percent: float
    input_feature_count: int


class ModelInfoResponse(BaseModel):
    loaded: bool
    model_type: str | None = None
    n_estimators: int | None = None
    feature_count: int | None = None
    features: list[str] = []
    development_batteries: list[str] = []
    untouched_test_batteries: list[str] = []
    metadata: dict[str, Any] = {}
