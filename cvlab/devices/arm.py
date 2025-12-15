import logging
from .base import RobotClient
from .plc import Plc

logger = logging.getLogger(__name__)


class Arm(RobotClient):
    """
    High-level controller for robotic arm, using a RobotClient
    for HTTP commands and a PLC for gripper control.
    """

    def __init__(self, name: str, arm_url: str, arm_aux_url: str, arm_aux_port: int):
        super().__init__(name=name, robot_url=arm_url)
        self._plc = Plc(name=f"{name}_plc_aux", plc_url=arm_aux_url, plc_port=arm_aux_port)

    # ------------------------------------------------------------------
    # Gripper control
    # ------------------------------------------------------------------
    def open_gripper(self):
        """Open the robotic gripper using PLC."""
        logger.info("[%s] Opening gripper...", self.name)
        return self._plc.gripper_open()

    def close_gripper(self):
        """Close the robotic gripper using PLC."""
        logger.info("[%s] Closing gripper...", self.name)
        return self._plc.gripper_close()
