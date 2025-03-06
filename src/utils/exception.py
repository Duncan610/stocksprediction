# src/utils/exception.py
import sys
from src.utils.logger import logger

def error_message_detail(error: str, error_detail: sys) -> str:
    """Generate detailed error message with file and line number."""
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    return f"Error in [{file_name}] at line [{exc_tb.tb_lineno}]: {str(error)}"

class CustomException(Exception):
    """Base class for custom exceptions."""
    def __init__(self, error_message: str, error_detail: sys):
        self.error_message = error_message_detail(error_message, error_detail)
        super().__init__(self.error_message)
        logger.error(self.error_message)

class DataIngestionError(CustomException):
    """Exception for data ingestion errors."""
    pass

class DataTransformationError(CustomException):
    """Exception for data transformation errors."""
    pass