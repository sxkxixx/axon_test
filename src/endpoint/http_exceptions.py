from typing import Any, Dict

from fastapi import HTTPException


class BadRequestException(HTTPException):
    STATUS_CODE = 404

    def __init__(self, detail: Any = None, headers: Dict[str, str] = None) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=detail, headers=headers)
