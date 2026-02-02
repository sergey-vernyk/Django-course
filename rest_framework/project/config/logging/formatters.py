import json
import logging

from log_records import SimpleLogRecord


class FileJSONFormatter(logging.Formatter):
    def format(self, record: SimpleLogRecord) -> str:
        log_data = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "user_id": getattr(record, "user_id", None),
            "request_id": getattr(record, "request_id", None),
            "exception": self.formatException(record.exc_info).splitlines()
            if record.exc_info is not None
            else None,
        }

        return json.dumps(log_data)
