import logging
import traceback

import click
from selenium.webdriver import Chrome

from auto_grade.auto_grade import main
from auto_grade.config import config


@click.command()
@click.argument("config_file", type=click.Path(exists=True), default="config.yaml")
def cli(config_file: str) -> None:
    """Automatically give feedback in Person ActiveLearn

    Get configururation from CONFIG FILE (default: `config.yaml`).
    """
    config.load_from_file(config_file)

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
