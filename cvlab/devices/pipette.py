import logging
from typing import Optional

from .base import Device, RobotClient

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Pipette Main Controller (HTTP-based, inherits RobotClient)
# ----------------------------------------------------------------------
class Pipette(RobotClient):
    """
    High-level pipette controller that uses HTTP for robotic movement
    and a separate auxiliary controller for low-level servo actions.
    """

    def __init__(self, name: str, pipette_url: str, pipette_aux_url: str, pipette_aux_port: int):
        super().__init__(name=name, robot_url=pipette_url)

        # Auxiliary low-level controller (socket)
        self.pipette_aux = PipetteAux(
            name=f"{name}_aux",
            pipette_aux_url=pipette_aux_url,
            pipette_aux_port=pipette_aux_port,
        )


# ----------------------------------------------------------------------
# Pipette AUX Controller (Socket-based)
# ----------------------------------------------------------------------
class PipetteAux(Device):
    """
    Socket-based controller for pipette servos and mechanical actions.
    """

    SPEED_MAP = {
        "fast": "7",
        "medium": "6",
        "slow": "5",
    }

    def __init__(self, name: str, pipette_aux_url: str, pipette_aux_port: int):
        super().__init__(
            name=name,
            base_url=None,
            socket_url=pipette_aux_url,
            port=pipette_aux_port,
        )

    # ------------------------------------------------------------------
    # Core functions
    # ------------------------------------------------------------------

    def preload_pipette(self):
        """
        Preload the pipette before dipping the tip into a sample.
        Command '1' = pre-suction stage.
        """
        logger.info("[%s] Preloading pipette...", self.name)
        return self.send_socket_command("1")

    def load_pipette(self):
        """
        Load sample into pipette.
        Command '4' = main suction stage.
        """
        logger.info("[%s] Loading sample...", self.name)
        return self.send_socket_command("4")

    def unload_pipette(self):
        """
        Unload pipette contents.
        Based on common convention: command '2' (you can adjust if needed).
        """
        logger.info("[%s] Unloading pipette...", self.name)
        return self.send_socket_command("2")

    def eject_tip(self):
        """
        Eject the pipette tip.
        Command '3'.
        """
        logger.info("[%s] Ejecting tip...", self.name)
        return self.send_socket_command("3")

    def homing_servos(self):
        """
        Home servo motors for pipette.
        Command '4'? (Ambiguous in your original code — consider changing)
        """
        logger.info("[%s] Homing servos...", self.name)
        return self.send_socket_command("4")

    def set_speed(self, speed: str = "fast"):
        """
        Set pipette action speed.
        - fast   → '7'
        - medium → '6'
        - slow   → '5'
        """

        speed_key = speed.lower().strip()
        cmd = self.SPEED_MAP.get(speed_key)

        if cmd is None:
            logger.warning(
                "[%s] Invalid speed='%s'. Defaulting to 'slow' (=5).",
                self.name, speed
            )
            cmd = self.SPEED_MAP["slow"]

        logger.info("[%s] Setting pipette speed: %s (%s)", self.name, speed_key, cmd)
        return self.send_socket_command(cmd)
