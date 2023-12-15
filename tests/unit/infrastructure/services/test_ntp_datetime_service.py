from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock
import pytest

from src.infrastructure.services.ntp_datetime_service import NtpDatetimeService


class TestNtpDatetimeService:
    """Test suite for a datetime service that uses NTP server"""

    @pytest.mark.parametrize(
        "ntp_server",
        [
            "",
            "pool.ntp.org",
            "time.google.com",
            "time.cloudflare.com",
            "time.windows.com",
        ],
    )
    @mock.patch("ntplib.NTPClient", name="ntpclient_mock")
    def test_get_datetime(self, ntpclient_mock: MagicMock, ntp_server: str):
        """Should return current time"""
        ntpclient_mock.request.return_value = MagicMock(tx_time=1614556800.0)
        datetime_service = NtpDatetimeService(ntp_server)

        ntp_datetime = datetime_service.get_datetime()

        assert isinstance(ntp_datetime, datetime)

    @pytest.mark.parametrize(
        "ntp_server",
        [
            "",
            "pool.ntp.org",
            "time.google.com",
            "time.cloudflare.com",
            "time.windows.com",
        ],
    )
    @mock.patch("ntplib.NTPClient", name="ntpclient_mock")
    def test_get_datetime_with_exception(
        self, ntpclient_mock: MagicMock, ntp_server: str
    ):
        """Should return epoch time when exception occurs"""
        ntpclient_mock.request.side_effect = Exception()
        datetime_service = NtpDatetimeService(ntp_server)

        datetime = datetime_service.get_datetime()

        assert datetime.isoformat() == "1970-01-01T00:00:01+00:00"
