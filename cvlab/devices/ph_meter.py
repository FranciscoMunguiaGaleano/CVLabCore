import json
import logging
from pathlib import Path
from typing import Tuple, Optional
from .base import Device

logger = logging.getLogger(__name__)

class PHMeter(Device):
    """
    Class for pH meter device. Reads pH values from ADC and applies calibration.
    """

    DEFAULT_SLOPE: float = -5.7
    DEFAULT_INTERCEPT: float = 16.34

    def __init__(self, name: str, phmeter_url: str, phmeter_port: int, calibration_conf: str):
        self.config_file: Path = Path(calibration_conf)
        super().__init__(name=name, socket_url=phmeter_url, port=phmeter_port)

    def load_calibration(self) -> Tuple[float, float]:
        """Load calibration slope and intercept from JSON file. Returns defaults if missing/invalid."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    cfg = json.load(f)
                    slope = cfg.get("slope", self.DEFAULT_SLOPE)
                    intercept = cfg.get("intercept", self.DEFAULT_INTERCEPT)
                    logger.info("[%s] Loaded calibration: pH = %.4f * V + %.4f", self.name, slope, intercept)
                    return slope, intercept
            except Exception as e:
                logger.warning("[%s] Error reading calibration file: %s", self.name, e)

        logger.warning("[%s] No calibration file found! Using defaults: slope=%.4f, intercept=%.4f",
                       self.name, self.DEFAULT_SLOPE, self.DEFAULT_INTERCEPT)
        return self.DEFAULT_SLOPE, self.DEFAULT_INTERCEPT

    @staticmethod
    def adc_to_voltage(adc: int) -> float:
        """Convert ADC reading to voltage (0-5V, 10-bit ADC)."""
        return adc * (5.0 / 1023.0)

    def read_status(self) -> str:
        """Read status of the pH meter."""
        logger.info("[%s] Checking pH meter status...", self.name)
        return self.read_value_from_socket("/")

    def read_ph(self) -> Optional[float]:
        """Read pH value, applying calibration."""
        try:
            adc_raw = self.read_value_from_socket("1")
            voltage = self.adc_to_voltage(float(adc_raw))
            slope, intercept = self.load_calibration()
            ph = slope * voltage + intercept
            logger.info("[%s] Measured pH: %.4f", self.name, ph)
            return ph
        except Exception as e:
            logger.error("[%s] Failed to read pH: %s", self.name, e)
            return None
