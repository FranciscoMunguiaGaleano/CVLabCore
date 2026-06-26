import logging
from typing import Dict
from .base import Device
from .plc import Plc

logger = logging.getLogger(__name__)


class SolidDispenser(Device):
    """
    Controller for the solid dispenser hardware, including cartridge tower,
    doors, dosing head, and sample dispensing.
    """

    def __init__(
        self,
        name: str,
        solid_dispenser_url: str,
        solid_dispenser_aux_url: str,
        solid_dispenser_aux_port: int,
    ):
        super().__init__(name=name, base_url=solid_dispenser_url)
        self._cartridges_tower = Plc(
            name=f"{name}_aux", plc_url=solid_dispenser_aux_url, plc_port=solid_dispenser_aux_port
        )

    # ------------------------------------------------------------------
    # Cartridge tower control
    # ------------------------------------------------------------------
    def set_cartridge_tower_position(self, pos: int = 1):
        """Move cartridge tower to a specified position (1 or 2)."""
        if pos == 1:
            logger.info("[%s] Moving cartridges tower to position 1", self.name)
            return self._cartridges_tower.cartridge_turn_cw()
        elif pos == 2:
            logger.info("[%s] Moving cartridges tower to position 2", self.name)
            return self._cartridges_tower.cartridge_turn_ccw()
        else:
            logger.error("[%s] Invalid position: %s, defaulting to position 1", self.name, pos)
            return self._cartridges_tower.cartridge_turn_cw()

    # ------------------------------------------------------------------
    # Door control
    # ------------------------------------------------------------------
    def open_front_door(self):
        logger.info("[%s] Opening front door", self.name)
        return self.post(endpoint="/open_front_door")

    def close_front_door(self):
        logger.info("[%s] Closing front door", self.name)
        return self.post(endpoint="/close_front_door")

    def open_side_doors(self):
        logger.info("[%s] Opening side doors", self.name)
        return self.post(endpoint="/open_side_door")

    def close_side_doors(self):
        logger.info("[%s] Closing side doors", self.name)
        return self.post(endpoint="/close_side_door")

    # ------------------------------------------------------------------
    # Dosing head control
    # ------------------------------------------------------------------
    def unlock_dosing_head(self):
        logger.info("[%s] Unlocking dosing head", self.name)
        return self.post(endpoint="/unlock_dosing_head")

    def lock_dosing_head(self):
        logger.info("[%s] Locking dosing head", self.name)
        return self.post(endpoint="/lock_dosing_head")

    # ------------------------------------------------------------------
    # Sample data and balance
    # ------------------------------------------------------------------
    def get_sample_data(self):
        logger.info("[%s] Getting sample data", self.name)
        return self.get(endpoint="/get_sample_data")

    def tare_balance(self):
        logger.info("[%s] Taring balance", self.name)
        return self.post(endpoint="/tare_balance")

    def set_target_mass(self, mass: Dict):
        logger.info("[%s] Setting target mass to: %s", self.name, mass.get("mass"))
        return self.post(endpoint="/set_target_mass", data=mass)

    def dispense(self, data: Dict):
        logger.info(
            "[%s] Dispensing %s mg of sample %s", self.name, data.get("mass"), data.get("sample_id")
        )
        return self.post(endpoint="/dispense", data=data)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------
    def status(self):
        logger.info("[%s] Reading status", self.name)
        return self.get(endpoint="/status")
