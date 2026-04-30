import logging
from .base import Device
from .plc import Plc

logger = logging.getLogger(__name__)


class Mixer:
    """
    Controller for the Mixer subsystem.
    Includes ultrasound bath (PLC controlled) and lift (socket controlled).
    """

    def __init__(
        self,
        name: str,
        mixer_url: str,
        mixer_port: int,
        mixer_aux_url: str,
        mixer_aux_port: int,
    ):
        self.name = name
        self._bath = Plc(name=f"{name}_bath", plc_url=mixer_url, plc_port=mixer_port)
        self._lift = Device(name=f"{name}_lift", socket_url=mixer_aux_url, port=mixer_aux_port)

    # ------------------------------------------------------------------
    # Lift control
    # ------------------------------------------------------------------
    def raise_lift(self):
        """Raise the lift using socket commands."""
        logger.info("[%s] Raising lift.", self.name)
        return self._lift.send_socket_command("1")

    def lower_lift(self):
        """Lower the lift using socket commands."""
        logger.info("[%s] Lowering lift.", self.name)
        return self._lift.send_socket_command("2")

    # ------------------------------------------------------------------
    # Ultrasound bath control
    # ------------------------------------------------------------------
    def turn_ultrasound_bath_on(self):
        """Turn the ultrasound bath ON."""
        logger.info("[%s] Turning ultrasound bath ON.", self.name)
        return self._bath.ultrasound_bath_on()

    def turn_ultrasound_bath_off(self):
        """Turn the ultrasound bath OFF."""
        logger.info("[%s] Turning ultrasound bath OFF.", self.name)
        return self._bath.ultrasound_bath_off()
