import logging
import os

LOG_DIR = os.path.join(os.getcwd(), "app-logs")
os.makedirs(LOG_DIR, exist_ok=True)


LOG_FILE = "app.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.info("Logging setup successfully!\n\n")
