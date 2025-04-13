import sys
from course.logger.logging import logging

def error_message_details(error, error_details: sys):
    _, _, exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in script: {file_name}, line: {line_number}, error: {str(error)}"
    return error_message

class RecommenderException(Exception):
    def __init__(self, error, error_details: sys):
        super().__init__(str(error))
        self.error_message = error_message_details(error, error_details)
        logging.error(self.error_message)  

    def __str__(self):
        return self.error_message
