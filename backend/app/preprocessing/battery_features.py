"""
Battery feature engineering placeholder.

The current final Random Forest expects 21 cycle-level engineered features.
The feature extraction logic used during training should eventually be
reimplemented here so that raw ESP32/Simulink windows can be transformed
into exactly the same 21-feature schema.

Do NOT invent a different preprocessing pipeline at inference time.
Training and inference feature definitions must remain identical.
"""

FINAL_BATTERY_FEATURES = [
    "voltage_initial",
    "voltage_final",
    "voltage_min",
    "voltage_max",
    "voltage_mean",
    "voltage_std",
    "voltage_drop",
    "current_mean",
    "current_min",
    "current_max",
    "current_std",
    "temperature_initial",
    "temperature_final",
    "temperature_max",
    "temperature_mean",
    "temperature_rise",
    "load_current_abs_mean",
    "load_current_abs_max",
    "load_voltage_mean",
    "load_voltage_min",
    "discharge_duration",
]
