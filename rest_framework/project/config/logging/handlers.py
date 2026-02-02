import logging

from .log_records import SimpleLogRecord


class JSONFileHandler(logging.Handler):
    """Обробник, який пише логи в JSON файл."""

    def __init__(self, filename: str, level: int | str = 0) -> None:
        super().__init__(level)
        self.filename = filename

    def emit(self, record: SimpleLogRecord) -> None:
        try:
            msg = self.format(record)
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except Exception:
            self.handleError(record)
