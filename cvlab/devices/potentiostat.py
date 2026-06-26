from typing import Optional, Dict, Any
from decimal import Decimal
from .base import Device  
import logging
import requests

logger = logging.getLogger(__name__)


class PotentiostatClient(Device):
    """
    Client for interacting with the FastAPI potentiostat server.
    """

    def __init__(self, name: str = "Potentiostat", base_url: Optional[str] = None):
        super().__init__(name=name, base_url=base_url)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _endpoint(self, potentiostat_id: int, path: str) -> str:
        return f"/{potentiostat_id}/{path}"

    def _post_binary(self, endpoint: str, params=None) -> Optional[bytes]:
        """Local POST method to fetch binary data (CSV)."""
        if not self.base_url:
            logger.error("[%s] Cannot POST: base_url is not set.", self.name)
            return None

        url = self._full_url(endpoint)

        try:
            response = requests.post(
                url,
                params=params,
                timeout=None  # 🔥 no timeout (wait as long as needed)
            )
            response.raise_for_status()
            return response.content

        except requests.RequestException as e:
            logger.error("[%s] POST(binary) %s failed: %s", self.name, url, e)
            return None

    # ------------------------------------------------------------------
    # API Methods
    # ------------------------------------------------------------------

    def status(self, potentiostat_id: int) -> Optional[Dict[str, Any]]:
        logger.info("[%s] Getting status of P%s", self.name, potentiostat_id)
        return self.get(self._endpoint(potentiostat_id, "status"))

    # ------------------- Measurements (return CSV) ---------------------

    def cyclic_voltammetry(
        self,
        potentiostat_id: int,
        i_range: str,
        start_potential: float,
        potential_vertex: float,
        scan_rate: float,
        cycles: int,
        increment: float = 0.01,
    ) -> Optional[bytes]:
        logger.info("[%s] Running cyclic voltammetry on P%s", self.name, potentiostat_id)

        payload = {
            "i_range": i_range,
            "start_potential": start_potential,
            "potential_vertex": potential_vertex,
            "scan_rate": scan_rate,
            "cycles": cycles,
            "increment": increment,
        }

        return self._post_binary(
            self._endpoint(potentiostat_id, "cyclic_voltemmetry"),
            params=payload
        )

    def linear_voltammetry(
        self,
        potentiostat_id: int,
        i_range: str,
        start_potential: float,
        end_potential: float,
        scan_rate: float,
        increment: float = 0.01,
    ) -> Optional[bytes]:
        logger.info("[%s] Running linear voltammetry on P%s", self.name, potentiostat_id)

        payload = {
            "i_range": i_range,
            "start_potential": start_potential,
            "end_potential": end_potential,
            "scan_rate": scan_rate,
            "increment": increment,
        }

        return self._post_binary(
            self._endpoint(potentiostat_id, "linear_voltemmetry"),
            params=payload
        )

    def open_circuit(
        self,
        potentiostat_id: int,
        duration: float,
        sampling_period: float,
    ) -> Optional[bytes]:
        logger.info("[%s] Running open circuit on P%s", self.name, potentiostat_id)

        payload = {
            "duration": duration,
            "sampling_period": sampling_period,
        }

        return self._post_binary(
            self._endpoint(potentiostat_id, "open_circuit"),
            params=payload
        )

    def electrolysis(
        self,
        potentiostat_id: int,
        i_range: str,
        potential: float,
        duration: float,
        sampling_period: float,
    ) -> Optional[bytes]:
        logger.info("[%s] Running electrolysis on P%s", self.name, potentiostat_id)

        payload = {
            "i_range": i_range,
            "potential": potential,
            "duration": duration,
            "sampling_period": sampling_period,
        }

        return self._post_binary(
            self._endpoint(potentiostat_id, "electrolysis"),
            params=payload
        )