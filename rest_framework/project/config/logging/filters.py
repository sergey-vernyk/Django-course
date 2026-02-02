import logging

from core.middlewares import request_id_var

from .log_records import SimpleLogRecord


class RequestFilter(logging.Filter):
    """Фільтр для додавання ID запиту у логи."""

    def filter(self, record: SimpleLogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True
