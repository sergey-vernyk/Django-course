import logging


class SimpleLogRecord(logging.LogRecord):
    """Додає не стандартні поля до запису логу."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_id: int | None = None
        self.request_id: str | None = None


logging.setLogRecordFactory(SimpleLogRecord)
