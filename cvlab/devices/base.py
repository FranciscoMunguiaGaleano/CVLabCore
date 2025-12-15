import json
import logging
import socket
from typing import Any, Dict, Optional
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class Device:
    """
    Base class for any network-controlled device (HTTP or raw socket).

    Parameters
    ----------
    name : str
        Human-readable device name (used in logs).
    base_url : str, optional
        URL for HTTP commands (GET/POST). If None, HTTP is disabled.
    socket_url : str, optional
        IP address/hostname for socket communication. If None, socket is disabled.
    port : int
        Port for the socket device.
    timeout : int
        Network timeout (seconds) for HTTP and socket operations.
    """

    def __init__(
        self,
        name: str = "",
        base_url: Optional[str] = None,
        socket_url: Optional[str] = None,
        port: int = 5000,
        timeout: int = 5,
    ) -> None:
        self.name = name
        self.base_url = base_url.rstrip("/") if base_url else None
        self.socket_url = socket_url
        self.port = port
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _full_url(self, endpoint: str) -> str:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url}{endpoint}"

    # ------------------------------------------------------------------
    # HTTP API
    # ------------------------------------------------------------------

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Send a POST request to the device."""
        if not self.base_url:
            logger.error("[%s] Cannot POST: base_url is not set.", self.name)
            return None

        url = self._full_url(endpoint)

        try:
            response = requests.post(url, json=data or {}, timeout=self.timeout)
            response.raise_for_status()  # catch HTTP errors

            try:
                json_data = response.json()
                logger.info("[POST][%s] %s -> %s", self.name, endpoint, json_data)
                return json_data
            except json.JSONDecodeError:
                logger.error("[%s] POST %s returned non-JSON: %s", self.name, endpoint, response.text)
                return None

        except requests.RequestException as e:
            logger.error("[%s] POST %s failed: %s", self.name, url, e)
            return None

    def get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Send a GET request to the device."""
        if not self.base_url:
            logger.error("[%s] Cannot GET: base_url is not set.", self.name)
            return None

        url = self._full_url(endpoint)

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            json_data = response.json()
            logger.info("[GET][%s] %s -> %s", self.name, endpoint, json_data)
            return json_data

        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.error("[%s] GET %s failed: %s", self.name, url, e)
            return None

    # ------------------------------------------------------------------
    # Socket API
    # ------------------------------------------------------------------

    def _open_socket(self) -> Optional[socket.socket]:
        if not self.socket_url:
            logger.error("[%s] Cannot open socket: socket_url is not set.", self.name)
            return None

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((self.socket_url, self.port))
            return s
        except OSError as e:
            logger.error("[%s] Socket connection failed: %s", self.name, e)
            return None

    def send_socket_command(self, cmd: str) -> bool:
        """Send a raw command via TCP socket."""
        s = self._open_socket()
        if not s:
            return False

        try:
            s.sendall((cmd + "\n").encode("utf-8"))
            logger.info("[%s] Sent socket command: %s", self.name, cmd)
            return True
        except OSError as e:
            logger.error("[%s] Socket send failed: %s", self.name, e)
            return False
        finally:
            s.close()

    def read_value_from_socket(self, cmd: str) -> Optional[str]:
        """Send a command and read the first line of response."""
        s = self._open_socket()
        if not s:
            return None

        try:
            s.sendall((cmd + "\n").encode("utf-8"))
            data = s.recv(1024).decode("utf-8").strip()
            logger.info("[%s] Received: %s", self.name, data)
            return data
        except OSError as e:
            logger.error("[%s] Socket read failed: %s", self.name, e)
            return None
        finally:
            s.close()

class RobotClient(Device):
    """
    Client for controlling a CNC/robot through an HTTP API.
    """

    def __init__(self, name: str = "CNC driver", robot_url: Optional[str] = None):
        super().__init__(name=name, base_url=robot_url)
        self.speed = 100

    # ------------------------------------------------------------------
    # Simple API wrappers
    # ------------------------------------------------------------------

    def send_gcode(self, gcode: str) -> Optional[Dict[str, Any]]:
        logger.info("[%s] Executing G-code: %s", self.name, gcode)
        return self.post("/send_gcode", {"gcode": gcode})

    def unlock(self):
        logger.info("[%s] Unlocking joints...", self.name)
        return self.post("/unlock")

    def home(self):
        logger.info("[%s] Homing...", self.name)
        return self.post("/home")

    def settings(self):
        logger.info("[%s] Fetching settings...", self.name)
        return self.get("/settings")

    def sleep(self):
        logger.info("[%s] Sleeping...", self.name)
        return self.post("/sleep")

    def get_position(self):
        logger.info("[%s] Getting current position...", self.name)
        return self.get("/position")

    def status(self):
        logger.info("[%s] Getting status...", self.name)
        return self.get("/status")

    def reset(self):
        logger.info("[%s] Resetting system...", self.name)
        return self.post("/reset")

    def wait_until_idle(self):
        logger.info("[%s] Waiting until robot is idle...", self.name)
        return self.get("/wait_until_idle")

    # ------------------------------------------------------------------
    # Routine Executor
    # ------------------------------------------------------------------

    def execute_routine(self, file: str) -> str:
        """
        Execute a JSON routine file containing a list of G-codes.
        
        Expected format:
        {
            "GCODES": ["G1 X0 Y0", "G1 X10"]
        }
        """
        file_path = Path(file)
        result = {
            "Instruction": "G-Code Executor",
            "success": False,
            "error": None
        }

        if not file_path.exists():
            error = f"Routine file not found: {file}"
            logger.error("[%s] %s", self.name, error)
            result["error"] = error
            return json.dumps(result)

        try:
            with file_path.open() as f:
                routines = json.load(f)

            gcodes: List[str] = routines.get("GCODES", [])
            if not gcodes:
                result["error"] = "Empty GCODES list"
                logger.error("[%s] Routine file contains no G-codes.", self.name)
                return json.dumps(result)

            logger.info("[%s] Loaded %d G-codes from: %s", self.name, len(gcodes), file)

            # Execute
            self.unlock()
            for g in gcodes:
                logger.info("[%s] Executing GCODE: %s", self.name, g)
                self.send_gcode(g)
                self.wait_until_idle()

            self.sleep()

            result["success"] = True
            return json.dumps(result)

        except Exception as e:
            logger.exception("[%s] Failed executing G-code routine: %s", self.name, e)
            result["error"] = str(e)
            return json.dumps(result)
