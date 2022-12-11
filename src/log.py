import logging
import os
from datetime import datetime


def init_logger():
    LOG_FILENAME = r'C:\Users\Pentex\PycharmProjects\tg-nyx-news\logs\log-' + f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.out"
    if not os.path.exists(LOG_FILENAME):
        open(LOG_FILENAME, "w")
    logging.basicConfig(
        format="%(asctime)s -  %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s()]: %(message)s ",
        level=logging.INFO, filename=LOG_FILENAME
    )
