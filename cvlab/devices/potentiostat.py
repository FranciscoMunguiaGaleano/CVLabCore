from typing import Optional, Dict, Any
from decimal import Decimal
from .base import Device  
import logging

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
            "start_potential": str(start_potential),
            "potential_vertex": str(potential_vertex),
            "scan_rate": scan_rate,
            "cycles": cycles,
            "increment": str(increment),
        }

        return self.get_binary(self._endpoint(potentiostat_id, "cyclic_voltemmetry") + "?" + self._to_query(payload))

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
            "start_potential": str(start_potential),
            "end_potential": str(end_potential),
            "scan_rate": scan_rate,
            "increment": str(increment),
        }

        return self.get_binary(self._endpoint(potentiostat_id, "linear_voltemmetry") + "?" + self._to_query(payload))

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

        return self.get_binary(self._endpoint(potentiostat_id, "open_circuit") + "?" + self._to_query(payload))

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
            "potential": str(potential),
            "duration": duration,
            "sampling_period": sampling_period,
        }

        return self.get_binary(self._endpoint(potentiostat_id, "electrolysis") + "?" + self._to_query(payload))

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def _to_query(self, payload: Dict[str, Any]) -> str:
        """Convert dict to query string."""
        return "&".join(f"{k}={v}" for k, v in payload.items())