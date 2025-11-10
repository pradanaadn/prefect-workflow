from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    nasa_api_key: str = Field(
        default="API_KEY", json_schema_extra={"description": "NASA API Key"}
    )
    nasa_base_url: str = Field(
        default="https://api.nasa.gov",
        json_schema_extra={"description": "NASA Base URL"},
    )
