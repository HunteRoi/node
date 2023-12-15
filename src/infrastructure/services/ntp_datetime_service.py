from datetime import datetime, timezone
import ntplib

from src.application.interfaces.idatetime_service import IDatetimeService


class NtpDatetimeService(IDatetimeService):
    """Datetime service that uses NTP server"""

    def __init__(self, ntp_server: str = "pool.ntp.org"):
        self.ntp_server = ntp_server
        self.client = ntplib.NTPClient()

    def get_datetime(self) -> datetime:
        try:
            response = self.client.request(self.ntp_server)
            return datetime.utcfromtimestamp(response.tx_time).replace(
                tzinfo=timezone.utc
            )
        except Exception:
            return datetime.fromisoformat("1970-01-01T00:00:01+00:00")
