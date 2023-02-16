import logging
from datetime import datetime

logging.basicConfig(filename='my.log', level=logging.DEBUG)


def add_log(my_text):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    log_text = f'{timestampStr}: {my_text}'
    logging.debug(log_text)