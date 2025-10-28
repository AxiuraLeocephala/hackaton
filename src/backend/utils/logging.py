import logging
from datetime import datetime

from src.backend.settings import CONFIG_LOGGING

def setup_logging():
    now = datetime.now()
    file_name = CONFIG_LOGGING["basic"]["filename"]
    idx_point = file_name.find(".")
    file_name = file_name[0 : idx_point] + "" \
        f"_{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}" \
        "" + file_name[idx_point :]

    if CONFIG_LOGGING["minor"]["logging_in_file"]:
        logging.basicConfig(
            filename=file_name,
            filemode=CONFIG_LOGGING["basic"]["filemode"],
            format=CONFIG_LOGGING["basic"]["format"],
            level=CONFIG_LOGGING["basic"]["level"],
        )
    else:
        logging.basicConfig(
            format=CONFIG_LOGGING["basic"]["format"],
            level=CONFIG_LOGGING["basic"]["level"],
        )

    logging.info("logging is set up")