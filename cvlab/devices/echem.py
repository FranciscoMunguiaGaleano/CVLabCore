import logging
from typing import Optional

from .base import Device,RobotClient
from .plc import Plc
from .pipette import Pipette

logger = logging.getLogger(__name__)


class EchemAux(Device):
    """
    Socket-based auxiliary controller for polishing disc, alumina dropper,
    and electrode Z-axis control.
    """

    SPEED_MAP = {
        "fast": "9",
        "medium": "8",
        "slow": "7",
    }

    CMD = {
        "lower_electrodes": "2",
        "raise_electrodes": "1",
        "polisher_on": "3",
        "polisher_off": "4",
        "dropper_on": "5",
        "dropper_off": "6",
    }

    def __init__(self, name: str, echem_aux_url: str, echem_aux_port: int):
        super().__init__(
            name=name,
            base_url=None,
            socket_url=echem_aux_url,
            port=echem_aux_port,
        )

    # ------------------------------------------------------------------
    # Polisher control
    # ------------------------------------------------------------------

    def polisher_on(self):
        logger.info("[%s] Polisher ON", self.name)
        return self.send_socket_command(self.CMD["polisher_on"])

    def polisher_off(self):
        logger.info("[%s] Polisher OFF", self.name)
        return self.send_socket_command(self.CMD["polisher_off"])

    # ------------------------------------------------------------------
    # Alumina dropper
    # ------------------------------------------------------------------

    def polisher_dropper_on(self):
        logger.info("[%s] Dropper ON", self.name)
        return self.send_socket_command(self.CMD["dropper_on"])

    def polisher_dropper_off(self):
        logger.info("[%s] Dropper OFF", self.name)
        return self.send_socket_command(self.CMD["dropper_off"])

    # ------------------------------------------------------------------
    # Electrodes vertical translation
    # ------------------------------------------------------------------

    def raise_electrodes(self):
        logger.info("[%s] Raising electrodes", self.name)
        return self.send_socket_command(self.CMD["raise_electrodes"])

    def lower_electrodes(self):
        logger.info("[%s] Lowering electrodes", self.name)
        return self.send_socket_command(self.CMD["lower_electrodes"])

    # ------------------------------------------------------------------
    # Speed control
    # ------------------------------------------------------------------

    def set_speed(self, speed: str = "slow"):
        speed_key = speed.lower().strip()
        cmd = self.SPEED_MAP.get(speed_key)

        if cmd is None:
            logger.warning(
                "[%s] Invalid speed setting '%s'. Defaulting to 'slow'.",
                self.name, speed
            )
            cmd = self.SPEED_MAP["slow"]

        logger.info("[%s] Setting polisher speed: %s (%s)", self.name, speed_key, cmd)
        return self.send_socket_command(cmd)

class Echem(RobotClient):
    """
    High-level electrochemistry system controller combining:
    - Echem auxiliary (polisher, electrodes)
    - PLC (dryer, nitrogen purge)
    - Pipette (motion + servos)
    """

    def __init__(
        self,
        name: str,
        echem_url: str,
        echem_aux_url: str,
        echem_aux_port: int,
        pipette_url: str,
        pipette_aux_url: str,
        pipette_aux_port: int,
        plc_url: str,
        plc_port: int,
    ):
        super().__init__(name=name, robot_url=echem_url)

        self._echem_aux = EchemAux(
            name=f"{name}_echem_aux",
            echem_aux_url=echem_aux_url,
            echem_aux_port=echem_aux_port
        )

        self._plc = Plc(
            name=f"{name}_plc",
            plc_url=plc_url,
            plc_port=plc_port
        )

        self._pipette = Pipette(
            name=f"{name}_pipette",
            pipette_url=pipette_url,
            pipette_aux_url=pipette_aux_url,
            pipette_aux_port=pipette_aux_port
        )
    # ------------------------------------------------------------------
    # Electrodes
    # ------------------------------------------------------------------
    def raise_electrodes(self): return self._echem_aux.raise_electrodes()
    def lower_electrodes(self): return self._echem_aux.lower_electrodes()

    # ------------------------------------------------------------------
    # Polisher
    # ------------------------------------------------------------------
    def polisher_on(self): return self._echem_aux.polisher_on()
    def polisher_off(self): return self._echem_aux.polisher_off()
    def polisher_dropper_on(self): return self._echem_aux.polisher_dropper_on()
    def polisher_dropper_off(self): return self._echem_aux.polisher_dropper_off()
    def polisher_set_speed(self, speed): return self._echem_aux.set_speed(speed)

    # ------------------------------------------------------------------
    # PLC subsystem (dryer, nitrogen purge)
    # ------------------------------------------------------------------
    def dryer_on(self): return self._plc.dryer_on()
    def dryer_off(self): return self._plc.dryer_off()
    def purger_on(self): return self._plc.purger_main_on()
    def purger_off(self): return self._plc.purger_main_off()

    # ------------------------------------------------------------------
    # Pipette arm motion
    # ------------------------------------------------------------------
    def pipette_arm_home(self): return self._pipette.home()
    def pipette_arm_unlock(self): return self._pipette.unlock()
    def pipette_arm_sleep(self): return self._pipette.sleep()
    def pipette_arm_reset(self): return self._pipette.reset()
    def pipette_arm_send_gcode(self, gcode): return self._pipette.send_gcode(gcode)
    def pipette_arm_execute_routine(self, file): return self._pipette.execute_routine(file)
    def pipette_arm_status(self): return self._pipette.status()
    def pipette_arm_get_X_axis(self): return self._pipette.X_axis
    def pipette_arm_set_X_axis(self, X_axis): self._pipette.X_axis = X_axis 
    def pipette_arm_get_Z_axis(self): return self._pipette.Z_axis
    def pipette_arm_set_Z_axis(self, Z_axis): self._pipette.Z_axis = Z_axis 
    
    # ------------------------------------------------------------------
    # Pipette servo/head
    # ------------------------------------------------------------------
    def pipette_home(self): return self._pipette.pipette_aux.homing_servos()
    def pipette_eject_tip(self): return self._pipette.pipette_aux.eject_tip()
    def pipette_preload(self): return self._pipette.pipette_aux.preload_pipette()
    def pipette_load(self): return self._pipette.pipette_aux.load_pipette()
    def pipette_unload(self): return self._pipette.pipette_aux.unload_pipette()
    def pipette_set_speed(self, speed): return self._pipette.pipette_aux.set_speed(speed)
