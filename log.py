import logging
import logging.handlers
from sys import stdout

from settings import settings

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
my_handler = logging.handlers.RotatingFileHandler('registration.log', mode='a', maxBytes=1_073_741_824, # 1GB
                                 backupCount=0, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(stdout)
if settings.get('Debug') == True:
    console_handler.setLevel(logging.DEBUG)
else:
    console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)

logger = logging.getLogger('RegistrationBot')
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)
logger.addHandler(console_handler)