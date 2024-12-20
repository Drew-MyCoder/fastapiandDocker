from typing import Any


class BusinessException(Exception):
    def __init__(self, status_code: int, detail: Any = None):
        self.status_code = status_code,
        self.detail = detail