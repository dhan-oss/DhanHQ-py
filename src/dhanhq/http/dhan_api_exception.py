from dataclasses import dataclass


@dataclass
class DhanAPIException(Exception):

    def __init__(self, code: str, message: str):
        self.error_code = code
        self.error_message = message
        super().__init__(f"{code}: {message}")