import logging

COLORS = {
    'asctime': '\033[94m',  # Blue
    'levelname': {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[1;31m',  # Bold Red
    },
    'reset': '\033[0m'  # Reset color
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        asctime = COLORS['asctime'] + self.formatTime(record, self.datefmt) + COLORS['reset']
        levelname = COLORS['levelname'].get(record.levelname, COLORS['reset']) + record.levelname + COLORS['reset']
        message = record.getMessage()
        formatted_message = f"{asctime} - {levelname} - {message}"
        return formatted_message


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": CustomFormatter,
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}
