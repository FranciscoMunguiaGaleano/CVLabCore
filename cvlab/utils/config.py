from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    AI_URL: str
    POTENTIOSTASTS_URL: str
    ARM_URL: str
    ECHEM_URL: str
    PIPETTE_URL: str
    LIQUIDS_URL: str
    SOLIDS_URL: str
    TOLEDO_PH_METER_URL:str
    CAMERA_URL: str
    PLC_URL: str
    PLC_PORT: int
    ECHEM_AUX_URL: str
    ECHEM_AUX_PORT: int
    PIPETTE_AUX_URL: str
    PIPETTE_AUX_PORT: int
    TOP_CAROUSEL_URL: str
    TOP_CAROUSEL_PORT: int
    BOTTOM_CAROUSEL_URL: str
    BOTTOM_CAROUSEL_PORT: int
    PH_PROBE_URL: str
    PH_PROBE_PORT: int
    PUMPS_URL: str
    PUMPS_PORT: int
    SERVO_URL: str
    SERVO_PORT: int
    STIRRER_URL: str
    STIRRER_PORT: int


def load_config(conf_file: str = "conf.json") -> Optional[Config]:
    """
    Load the system configuration from a JSON file.

    Parameters
    ----------
    conf_file : str
        Path to the JSON configuration file.

    Returns
    -------
    Config or None
        Parsed configuration, or None if loading failed.
    """
    path = Path(conf_file)

    if not path.exists():
        logger.error("Config file not found: %s", conf_file)
        return None

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        logger.error("Failed to read/parse config '%s': %s", conf_file, e)
        return None

    try:
        cfg = Config(**data)
        logger.info("Configuration loaded successfully from %s", conf_file)
        return cfg
    except TypeError as e:
        logger.error("Invalid config fields in '%s': %s", conf_file, e)
        return None
