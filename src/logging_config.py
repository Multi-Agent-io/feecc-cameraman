import logging
import sys

# set up logging configurations
BASE_LOGGING_CONFIG = {
    "colorize": True,
    "backtrace": True,
    "diagnose": True,
    "catch": True,
}

# logging settings for the console logs
CONSOLE_LOGGING_CONFIG = {
    **BASE_LOGGING_CONFIG,  # type: ignore
    "level": "DEBUG",
    "sink": sys.stdout,
}

# logging settings for the log file
FILE_LOGGING_CONFIG = {
    **BASE_LOGGING_CONFIG,  # type: ignore
    "level": "DEBUG",
    "sink": "feecc-cameraman.log",
    "rotation": "10 MB",
    "compression": "zip",
}


# disable Uvicorn's access logs for specified endpoints
class EndpointAccessFilter(logging.Filter):
    excluded_endpoints = {"/docs", "/openapi.json", "/health", "/metrics", "/robots.txt"}

    def filter(self, record: logging.LogRecord) -> bool:
        # complete query string (so parameter and other value included)
        query_string: str = record.args[2]  # type: ignore
        endpoint = query_string.split("?")[0]
        return endpoint not in self.excluded_endpoints


logging.getLogger("uvicorn.access").addFilter(EndpointAccessFilter())
