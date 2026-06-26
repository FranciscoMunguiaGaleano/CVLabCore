import logging
from .base import Device
import time

logger = logging.getLogger(__name__)

class ToledoPhMeter(Device):
    """
    Class for Toledo Ph meter. Reads Ph VAlues from the probre, temperature, date and controls READ Button.
    """

    def __init__(self, name: str, toledophmeter_url: str, servo_url: str, servo_port: str):
        super().__init__(name=name, base_url= toledophmeter_url)
        self.servo=Device(name="ToledoPhmeter_aux",socket_url=servo_url,port=servo_port)
        #TODO home servo

    # ------------------------------------------------------------------
    # Button control (servo)
    # ------------------------------------------------------------------
    
    def press_read_button(self):
        logger.info("[%s] Pressing Read Button...", self.name)
        self.servo.send_socket_command('1');time.sleep(0.7)
        self.servo.send_socket_command('1');time.sleep(3)
        return {"message": "[Info] Button Pressed"}
    
    # ------------------------------------------------------------------
    # Ph Reading 
    # ------------------------------------------------------------------
    
    def read_ph(self):
        logger.info("[%s] Reading pH...", self.name)
        return self.get("/read_ph")
    
    def status(self):
        logger.info("[%s] Reading status...", self.name)
        return self.get("/status")