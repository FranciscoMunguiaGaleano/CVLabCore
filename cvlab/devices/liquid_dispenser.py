import logging
from typing import Dict
from .base import Device
from .plc import Plc

logger = logging.getLogger(__name__)


class SyringePump(Device):
    """
    Controller for a syringe pump, including piston, valve, and waste port control.
    """

    def __init__(
        self,
        name: str,
        syringe_pump_url: str,
        syringe_pump_aux_url: str,
        syringe_pump_aux_port: int,
    ):
        super().__init__(name=name, base_url=syringe_pump_url)
        self._piston = Plc(
            name=f"{name}_aux",
            plc_url=syringe_pump_aux_url,
            plc_port=syringe_pump_aux_port,
        )

    # ------------------------------------------------------------------
    # Piston control
    # ------------------------------------------------------------------
    def piston_to_dispense_position(self):
        """Move piston to dispensing position."""
        return self._piston.dispensing_position()

    def piston_to_home_position(self):
        """Return piston to home position."""
        return self._piston.dispensing_home()

    # ------------------------------------------------------------------
    # Status and valve
    # ------------------------------------------------------------------
    def status(self):
        logger.info("[%s] Reading status", self.name)
        return self.get(endpoint="/status")

    def get_valve_pos(self):
        logger.info("[%s] Getting valve position", self.name)
        return self.get(endpoint="/get_valve_pos")

    # ------------------------------------------------------------------
    # Dispensing
    # ------------------------------------------------------------------
    def dispense(self, data: Dict):
        logger.info(
            "[%s] Dispensing %s ml of liquid %s",
            self.name,
            data.get("volume"),
            data.get("liquid_id"),
        )
        return self.post(endpoint="/dispense", data=data)

    def move_home(self):
        """Move the syringe pump to home position."""
        logger.info("[%s] Moving to home position", self.name)
        return self.post(endpoint="/move_home")

    def set_waste_port(self, data: Dict):
        """Set the waste port."""
        logger.info("[%s] Setting waste port to: %s", self.name, data.get("waste_port"))
        return self.post(endpoint="/set_waste_port", data=data)
