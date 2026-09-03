from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_DIR = BACKEND_DIR / "models" / "battery"


class Settings(BaseSettings):
    app_name: str = "DriveGuard-X AI Backend"
    environment: str = "development"

    battery_model_path: Path = (
        DEFAULT_MODEL_DIR / "driveguard_x_final_battery_rf.joblib"
    )
    battery_metadata_path: Path = (
        DEFAULT_MODEL_DIR / "final_model_metadata.json"
    )
    battery_schema_path: Path = (
        DEFAULT_MODEL_DIR / "feature_schema.json"
    )

    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
