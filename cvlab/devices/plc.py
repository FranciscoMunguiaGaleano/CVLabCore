import logging
from typing import Optional, Union

from .base import Device  # adjust import path to your project

logger = logging.getLogger(__name__)


class Plc(Device):
    """
    PLC controller using socket commands.
    Provides high-level semantic controls for actuators connected to the PLC.
    """

    def __init__(self, name: str, plc_url: str, plc_port: int):
        super().__init__(name=name, base_url=None, socket_url=plc_url, port=plc_port)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _main_on(self, n: int):
        return self.send_socket_command(f"/main{n}")

    def _main_off(self, n: int):
        return self.send_socket_command(f"/mainoff{n}")

    def _ext_on(self, n: int):
        return self.send_socket_command(f"/ext{n}")

    def _ext_off(self, n: int):
        return self.send_socket_command(f"/offext{n}")

    # ------------------------------------------------------------------
    # High-level actuators
    # ------------------------------------------------------------------

    # --- Purger Main ---
    def purger_main_on(self):
        logger.info("[%s][Purger Main] ON", self.name)
        return self._main_on(1)

    def purger_main_off(self):
        logger.info("[%s][Purger Main] OFF", self.name)
        return self._main_off(1)

    # --- Dryer ---
    def dryer_on(self):
        logger.info("[%s][Dryer] ON", self.name)
        return self._main_on(2)

    def dryer_off(self):
        logger.info("[%s][Dryer] OFF", self.name)
        return self._main_off(2)

    # --- Purger Stock ---
    def purger_stock_on(self):
        logger.info("[%s][Purger Stock] ON", self.name)
        return self._main_on(3)

    def purger_stock_off(self):
        logger.info("[%s][Purger Stock] OFF", self.name)
        return self._main_off(3)

    # --- Gripper ---
    def gripper_open(self):
        logger.info("[%s][Gripper] Opening...", self.name)
        return self._main_off(4)

    def gripper_close(self):
        logger.info("[%s][Gripper] Closing...", self.name)
        return self._main_on(4)

    # --- Cartridge Holder Rotation ---
    def cartridge_turn_cw(self):
        logger.info("[%s][Cartridge Holder] Turning clockwise...", self.name)
        return self._ext_off(3)

    def cartridge_turn_ccw(self):
        logger.info("[%s][Cartridge Holder] Turning anticlockwise...", self.name)
        return self._ext_on(3)

    # --- Capper: Cap Holder ---
    def capper_cap_hold(self):
        logger.info("[%s][Capper Cap Holder] Holding cap...", self.name)
        return self._ext_on(4)

    def capper_cap_release(self):
        logger.info("[%s][Capper Cap Holder] Releasing cap...", self.name)
        return self._ext_off(4)

    # --- Capper: Vial Holder ---
    def capper_vial_hold(self):
        logger.info("[%s][Capper Vial Holder] Holding vial...", self.name)
        return self._ext_on(5)

    def capper_vial_release(self):
        logger.info("[%s][Capper Vial Holder] Releasing vial...", self.name)
        return self._ext_off(5)

    # --- Cap Lift ---
    def capper_lift_up(self):
        logger.info("[%s][Capper Lift] Lifting cap...", self.name)
        return self._ext_off(6)

    def capper_lift_down(self):
        logger.info("[%s][Capper Lift] Lowering cap...", self.name)
        return self._ext_on(6)

    # --- Dispensing Piston ---
    def dispensing_position(self):
        logger.info("[%s][Dispensing] Moving piston to dispensing position...", self.name)
        return self._ext_on(7)

    def dispensing_home(self):
        logger.info("[%s][Dispensing] Returning piston to home...", self.name)
        return self._ext_off(7)

    # --- Ultrasound Bath ---
    def ultrasound_bath_on(self):
        logger.info("[%s][Ultrasound Bath] ON", self.name)
        return self._ext_on(1)

    def ultrasound_bath_off(self):
        logger.info("[%s][Ultrasound Bath] OFF", self.name)
        return self._ext_off(1)
