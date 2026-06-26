import logging
from typing import Optional
from .base import Device,RobotClient


logger = logging.getLogger(__name__)


class Camera(Device):
    """
    This controller fetches and image from the camera of the electrochemistry station.
    """
    def __init__(self, name: str, camera_url: str):
        super().__init__(
            name=name,
            base_url=camera_url
        )
    def capture(self):
        logger.info("[%s] Fetching image...", self.name)
        return self.get_binary("/capture")