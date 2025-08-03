# src/main/config/__init__.py
"""
Initialize application configs and environment variables (secrets).
- INI base config:    src/main/config/ap_info.ini
- Environment select: APP_ENV (development|staging|production...)
- Secret example:     SECRET_VARIABLE (required in production)
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation

from pydantic import Field, ValidationError, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


# -------------------------
# Paths and INI preparation
# -------------------------
_CONFIG_DIR = Path(__file__).resolve().parent
INI_PATH = _CONFIG_DIR / "ap_info.ini"

# Which environment profile to merge (matches [development], [staging], [production] in INI)
APP_ENV = os.getenv("APP_ENV", "development").strip()

# -------------------------
# Load INI with interpolation
# -------------------------
_parser = ConfigParser(interpolation=ExtendedInterpolation())
read_files = _parser.read(INI_PATH.as_posix())
if not read_files:
    raise FileNotFoundError(f"Config file not found: {INI_PATH}")

# Component sections (create as needed)
ComponentA_cfg = _parser["ComponentA"] if _parser.has_section("ComponentA") else {}

# Optional env-profile overrides: section named exactly like APP_ENV
# Supports dotted-keys (e.g., Database.host) by splitting and applying to sub-sections.
def _apply_profile_overrides(parser: ConfigParser, profile_name: str) -> None:
    if not parser.has_section(profile_name):
        return
    profile = parser[profile_name]
    for key, value in profile.items():
        if "." in key:
            section, opt = key.split(".", 1)
            if not parser.has_section(section):
                parser.add_section(section)
            parser.set(section, opt, value)
        else:
            # Falls back to DEFAULT for top-level keys
            parser["DEFAULT"][key] = value

_apply_profile_overrides(_parser, APP_ENV)

# Rebind after overrides so lookups include merged values
ComponentA_cfg = _parser["ComponentA"] if _parser.has_section("ComponentA") else {}

# -------------------------
# Secrets / env variables
# -------------------------
SECRET_VARIABLE = os.getenv("SECRET_VARIABLE")
if APP_ENV == "production" and not SECRET_VARIABLE:
    raise RuntimeError("SECRET_VARIABLE must be set in production.")


# -------------------------
# Pydantic settings (v2)
# -------------------------
class ApConfig(BaseSettings):
    """
    Settings for ComponentA (extend with more components/modules as needed).
    Env precedence: environment > INI > defaults.
    """

    # Example field sourced from INI by default, override via env COMP_A_VARIABLE or COMPA_VARIABLE
    compA_variable: str = Field(
        default=ComponentA_cfg.get("compA_variable", ""),
        description="ComponentA configurable variable.",
        validation_alias=AliasChoices("COMP_A_VARIABLE", "COMPA_VARIABLE"),
    )

    # pydantic-settings v2 config
    model_config = SettingsConfigDict(
        env_prefix="",              # keep empty; we use explicit validation_alias above
        extra="ignore",
        env_file=".env",            # optional: auto-load .env
        env_file_encoding="utf-8",
    )


class Settings(BaseSettings):
    """
    Top-level application settings.
    Add more sections/fields here and seed their defaults from INI.
    """
    app_env: str = Field(
        APP_ENV,
        description="Active environment profile.",
        validation_alias=AliasChoices("APP_ENV"),
    )
    secret_variable: str | None = Field(
        SECRET_VARIABLE,
        description="Example secret.",
        validation_alias=AliasChoices("SECRET_VARIABLE"),
    )

    # Nest module configs
    componentA: ApConfig = ApConfig()

    model_config = SettingsConfigDict(
        env_prefix="",      # no global prefix
        extra="ignore",
        env_file=".env",    # optional: auto-load .env
        env_file_encoding="utf-8",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Cached accessor for settings.
    Usage:
        from src.main.config import get_settings
        settings = get_settings()
        print(settings.componentA.compA_variable)
    """
    try:
        return Settings()
    except ValidationError as ve:
        raise RuntimeError(f"Configuration validation failed: {ve}") from ve

# Optionally materialize at import (kept lazy via function by default)
# settings = get_settings()
