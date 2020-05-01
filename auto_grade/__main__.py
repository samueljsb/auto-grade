import logging
import traceback

from selenium.webdriver import Chrome

from auto_grade.auto_grade import main
from auto_grade.config import config


config.load_from_file("config.yaml")

logging.basicConfig()
LOG = logging.getLogger("auto_grade")
if config.debug:
    LOG.setLevel(logging.DEBUG)
else:
    LOG.setLevel(logging.INFO)

webdriver = Chrome()
try:
    main(webdriver)
except Exception as err:
    LOG.critical(f"{type(err)}: {err}")
    traceback.print_tb(err.__traceback__)
    if config.debug:
        breakpoint()
finally:
    webdriver.quit()
