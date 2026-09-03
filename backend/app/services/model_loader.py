import json
from functools import lru_cache
from pathlib import Path

import joblib

from app.core.config import settings


@lru_cache(maxsize=1)
def get_battery_model():
    path = Path(settings.battery_model_path)

    if not path.exists():
        raise RuntimeError(
            f"Battery model not found at: {path}. "
            "Copy the Kaggle artifact into backend/models/battery/."
        )

    return joblib.load(path)


@lru_cache(maxsize=1)
def get_battery_metadata() -> dict:
    path = Path(settings.battery_metadata_path)

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def get_battery_schema() -> list[str]:
    path = Path(settings.battery_schema_path)

    if not path.exists():
        metadata = get_battery_metadata()
        return metadata.get("features", [])

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # Support either {"features": [...]} or a raw list.
    if isinstance(data, dict):
        return data.get("features", [])

    return data


def load_models() -> None:
    """
    Load the current production/research artifacts during application startup.
    """
    get_battery_model()
    get_battery_metadata()
    get_battery_schema()


def get_battery_model_info() -> dict:
    try:
        metadata = get_battery_metadata()
        features = get_battery_schema()

        return {
            "loaded": True,
            "model_type": metadata.get("model"),
            "n_estimators": metadata.get("n_estimators"),
            "feature_count": len(features),
            "features": features,
            "development_batteries": metadata.get(
                "development_batteries", []
            ),
            "untouched_test_batteries": metadata.get(
                "untouched_test_batteries", []
            ),
            "metadata": metadata,
        }
    except Exception:
        return {
            "loaded": False,
            "model_type": None,
            "n_estimators": None,
            "feature_count": None,
            "features": [],
            "development_batteries": [],
            "untouched_test_batteries": [],
            "metadata": {},
        }
