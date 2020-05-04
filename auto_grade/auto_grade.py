import logging
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .config import config
from .feedback import get_feedback_comment
from .utils import (
    click_button,
    click_link,
    populate_form,
    populate_text_box,
    wait_for_element,
    wait_for_element_text_to_equal,
    wait_for_elements,
)


LOG = logging.getLogger(__name__)

BASE_URL = "https://pearsonactivelearn.com/"


def task_needs_feedback(row: WebElement, completed_tasks: List[str]) -> bool:
    """Checks a row from the Tasks summary page to see if the task needs feedback."""
    cells = wait_for_elements(row, "td", By.TAG_NAME)
    task_name = cells[1].text
    return task_name not in completed_tasks


def student_needs_feedback(row: WebElement) -> bool:
    """Checks a row from the Task Reports page to see if the pupil needs feedback."""
    cells = wait_for_elements(row, "td", By.TAG_NAME)
    status = cells[3].text
    teacher_feedback = cells[-2].get_attribute("tick")

    return status in ("Completed", "Incomplete") and teacher_feedback == "false"


def give_feedback_for_group(webdriver: WebDriver, group_name: str) -> None:
    """Give feedback for all completed tasks by members of a group.

    Assumptions:
      - You are logged in.

    """
    LOG.info(f"Completing feedback for the group '{group_name}'")

    # Give feedback for tasks that need it.
    completed_tasks: List[str] = []
    while True:
        # Go to 'Tasks'.
        click_link(webdriver, "Tasks")
        # Go to 'Submitted'.
        click_link(webdriver, "Submitted")
        click_link(webdriver, "Submitted")  # hack
        # Select the group.
        dropdown = wait_for_element(webdriver, "criteria-list", By.CLASS_NAME)
        dropdown.click()
        menu_item = wait_for_element(
            webdriver, f"//label/span[text() = '{group_name}']", By.XPATH
        )
        menu_item.click()

        rows = wait_for_elements(webdriver, "//tbody/tr", By.XPATH)
        try:
            next_row = next(
                row for row in rows if task_needs_feedback(row, completed_tasks)
            )
        except StopIteration:
            return

        task_link = wait_for_element(next_row, "td/a", By.XPATH)
        task_name = task_link.text
        task_link.click()
        give_feedback_for_task(webdriver)
        completed_tasks.append(task_name)


def give_feedback_for_task(webdriver: WebDriver) -> None:
    """Give feedback for all completed assignments in a task.

    Assumptions:
      - The current page is the task report page.

    """
    task_name = wait_for_element(
        webdriver, "//div[@class = 'panel-heading']/div/span", By.XPATH
    ).text
    LOG.info(f"Completing feedback for the task '{task_name}'")
    # Give feedback to all pupils who need it.
    while True:
        rows = wait_for_elements(webdriver, "//tbody/tr", By.XPATH)
        # Click on the first row that needs feedback.
        try:
            next_row = next(row for row in rows if student_needs_feedback(row))
        except StopIteration:
            return

        click_link(next_row, "Review Results")
        give_pupil_feedback(webdriver)
        # Check we're on the right page (again).
        #  NOTE: This is a bit hacky.
        wait_for_element_text_to_equal(
            webdriver, "panel-heading", "Task report", By.CLASS_NAME
        )


def give_pupil_feedback(webdriver: WebDriver) -> None:
    """Give a pupil feedback on a task.

    Assumptions:
      - The current page is the task feedback report page for a student.

    """
    # Get pupil name.
    pupil_name = wait_for_element(webdriver, "headerText", By.CLASS_NAME).text

    # Get the score.
    data_center = wait_for_element(webdriver, "data-center", By.CLASS_NAME)
    try:
        score = int(data_center.text.strip("%"))
    except ValueError:
        # Some tasks don't have a score, so we have to infer one from the color.
        span = data_center.find_element_by_class_name("result-ragg")
        classes = span.get_attribute("class").split()
        if "raggGreen" in classes or "raggGold" in classes:
            score = 100
        elif "raggAmber" in classes:
            score = 60
        elif "raggRed" in classes:
            score = 0
        else:
            raise ValueError(f"Unexpected result color classes: {classes}")

    # Select a message.
    feedback_message = get_feedback_comment(score)
    LOG.info(f"Giving feedback to {pupil_name} ({score}%): '{feedback_message}'")

    # Enter the message.
    text_box = wait_for_element(webdriver, "feedback-textrea", By.CLASS_NAME)
    populate_text_box(text_box, feedback_message)

    # Submit feedback.
    if config.debug:
        selection = input("Submit feedback? [y/N]: ") or "n"
        if selection == "y":
            click_button(webdriver, "Send feedback and return to previous screen")
    else:
        click_button(webdriver, "Send feedback and return to previous screen")


def login(webdriver: WebDriver, username: str, password: str) -> None:
    webdriver.get(BASE_URL + "app/login")

    # Log in.
    form = wait_for_element(webdriver, "mainForm")
    populate_form(form, {"username": username, "password": password})
    click_button(form, "Sign in")


def main(webdriver: WebDriver) -> None:
    login(webdriver, config.username, config.password)

    time.sleep(1)  # Takes ages to load after login.

    for group_name in config.groups:
        give_feedback_for_group(webdriver, group_name)
