import atexit
import signal

from src.presentation.application import Application


application = Application()


def _stop_handler(sig=None, frame=None):  # pylint: disable=unused-argument
    """Handles the SIGINT signal."""
    application.stop()


def _start_handler():
    signal.signal(signal.SIGINT, _stop_handler)
    atexit.register(_stop_handler)

    application.run()


if __name__ == "__main__":
    _start_handler()
