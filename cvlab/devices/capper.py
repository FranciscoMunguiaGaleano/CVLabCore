import time
import logging
from .plc import Plc

logger = logging.getLogger(__name__)


class Capper:
    """
    Controller for the capper subsystem: cap and vial handling.
    Uses a PLC for low-level actuation.
    """

    def __init__(self, name: str, capper_url: str, capper_port: int):
        self._plc = Plc(name=f"{name}_plc", plc_url=capper_url, plc_port=capper_port)

    # ------------------------------------------------------------------
    # Helper to sleep with logging
    # ------------------------------------------------------------------
    @staticmethod
    def _wait(seconds: float):
        time.sleep(seconds)

    # ------------------------------------------------------------------
    # Capper motion sequences
    # ------------------------------------------------------------------
    def home(self):
        """Move capper to home position."""
        logger.info("[%s] Moving capper to home position.", self._plc.name)
        self._plc.capper_cap_release()
        self._wait(0.4)
        self._plc.capper_vial_release()
        self._wait(0.4)
        self._plc.capper_lift_up()
        self._wait(0.4)

    def hold_vial(self):
        """Hold vial in position."""
        logger.info("[%s] Holding vial.", self._plc.name)
        self._plc.capper_vial_hold()
        self._wait(2)

    def release_vial(self):
        """Release vial from capper."""
        logger.info("[%s] Releasing vial.", self._plc.name)
        self._plc.capper_vial_release()
        self._wait(2)

    def uncap(self):
        """Remove the cap from the vial."""
        logger.info("[%s] Uncapping vial.", self._plc.name)
        self._plc.capper_lift_down()
        self._wait(2)
        self._plc.capper_cap_hold()
        self._wait(2)
        self._plc.capper_lift_up()
        self._wait(2)

    def cap(self):
        """Place the cap onto the vial."""
        logger.info("[%s] Capping vial.", self._plc.name)
        self._plc.capper_lift_down()
        self._wait(2)
        self._plc.capper_cap_release()
        self._wait(2)
        self._plc.capper_lift_up()
        self._wait(2)
