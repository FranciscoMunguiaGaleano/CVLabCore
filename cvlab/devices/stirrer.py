import logging
from typing import Optional

from .base import Device, RobotClient

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Stirrer Controller (Socket-based)
# ----------------------------------------------------------------------
class Stirrer(Device):
    """
    Socket-based controller for bars stirrer in echem.
    """

    def __init__(self, name: str, stirrer_url: str, stirrer_port: int):
        super().__init__(
            name=name,
            base_url=None,
            socket_url=stirrer_url,
            port=stirrer_port,
        )

    # ------------------------------------------------------------------
    # Core functions
    # ------------------------------------------------------------------

    def stirrers_on(self):
        """
        Turns ALL stirrers on
        Command '1' = stirrer (fans on)).
        """
        logger.info("[%s] Turning stirrers ON...", self.name)
        return self.send_socket_command("1")
    
    def stirrers_off(self):
        """
        Turns ALL stirrers off
        Command '0' = stirrer (fans off)).
        """
        logger.info("[%s] Turning stirrers OFF...", self.name)
        return self.send_socket_command("2")