import threading


class LiveTickBuffer:
    """
    Thread-safe holder for the latest tick.

    A background thread (streaming from Deriv) writes to this on
    every tick. The main Streamlit thread reads from it on its own
    fast fragment timer. A lock guards both sides so reads/writes
    never interleave badly.
    """

    def __init__(self):

        self._lock = threading.Lock()
        self._quote = None
        self._digit = None
        self._connected = False
        self._error = None

    def set_tick(self, quote, digit):

        with self._lock:
            self._quote = quote
            self._digit = digit
            self._connected = True
            self._error = None

    def set_error(self, message):

        with self._lock:
            self._connected = False
            self._error = message

    def get(self):

        with self._lock:
            return {
                "quote": self._quote,
                "digit": self._digit,
                "connected": self._connected,
                "error": self._error,
            }


class AutoTradeToggle:
    """
    Thread-safe on/off switch. The sidebar checkbox (main thread)
    calls .set() whenever the user toggles it; the background tick
    stream thread calls .get() before placing any trade. Defaults to
    OFF so nothing fires automatically until explicitly enabled.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._enabled = False

    def set(self, enabled):
        with self._lock:
            self._enabled = enabled

    def get(self):
        with self._lock:
            return self._enabled
