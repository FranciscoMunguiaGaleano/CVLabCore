import json
import logging
from typing import Optional, Dict, List
from .base import Device
from .plc import Plc

logger = logging.getLogger(__name__)


class TopCarousel(Device):
    """
    Base class for a Carousel device. Supports homing, absolute, and incremental movement.
    """

    def __init__(self, name: str, carousel_url: str, carousel_port: int, conf_file: str):
        self.position: float = 0.0
        self.positions: Optional[List[float]] = self.load_positions(conf_file)
        self.step: float = 0.1
        super().__init__(name=name, base_url=None, socket_url=carousel_url, port=carousel_port)

    def load_positions(self, conf_file: str) -> Optional[List[float]]:
        """Load carousel positions from JSON config file."""
        try:
            with open(conf_file) as f:
                return json.load(f)
        except Exception:
            logger.error("[%s] File %s does not exist or is invalid.", self.name, conf_file)
            return None

    def home(self):
        """Home the carousel."""
        logger.info("[%s] Homing Carousel", self.name)
        return self.send_socket_command("home")

    def move_absolute(self, pos: int):
        """Move carousel to an absolute position."""
        self.position = self.positions[str(pos)]
        logger.info("[%s] Moving to absolute position %s at %.2f degrees", self.name, pos, self.position)
        return self.send_socket_command(f"go {self.position}")

    def move_incremental(self):
        """Move carousel by a step increment."""
        self.position += self.step
        logger.info("[%s] Moving incrementally to %.2f degrees", self.name, self.position)
        return self.send_socket_command(f"go {self.position}")


class BottomCarousel(TopCarousel):
    """
    Extended Carousel with pumps and purger control.
    """

    def __init__(
        self,
        name: str,
        carousel_url: str,
        carousel_port: int,
        aux_carousel_pump_url: str,
        aux_carousel_pump_port: int,
        aux_carousel_purger_url: str,
        aux_carousel_purger_port: int,
        conf_file: str,
    ):
        super().__init__(name, carousel_url, carousel_port, conf_file)
        self._pumps = Device(name=f"{name}_aux", socket_url=aux_carousel_pump_url, port=aux_carousel_pump_port)
        self._purger = Plc(name=f"{name}_aux", plc_url=aux_carousel_purger_url, plc_port=aux_carousel_purger_port)

    # Pumps control
    def turn_pumps_on(self):
        logger.info("[%s] Turning pumps on.", self.name)
        return self._pumps.send_socket_command("5")

    def turn_pumps_off(self):
        logger.info("[%s] Turning pumps off.", self.name)
        return self._pumps.send_socket_command("6")

    # Purger control
    def turn_purger_on(self):
        logger.info("[%s] Turning purger on.", self.name)
        return self._purger.purger_stock_on()

    def turn_purger_off(self):
        logger.info("[%s] Turning purger off.", self.name)
        return self._purger.purger_stock_off()
