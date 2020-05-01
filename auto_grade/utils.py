import time
from typing import List

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def click_link(webdriver: WebElement, link_text: str, max_timeout: float = 4) -> None:
    """Click on a link.

    Will timeout if the link cannot be found before max_timeout seconds have passed.
    """
    start_time = time.time()
    wait_for_element(webdriver, link_text, By.LINK_TEXT, max_timeout)
    time.sleep(0.2)
    while time.time() - start_time < max_timeout:
        # Try to find the link.
        try:
            link = webdriver.find_element_by_link_text(link_text)
        except NoSuchElementException:
            # If we can't find the link, keep trying...
            continue

        # Click the link.
        try:
            link.click()
        except ElementClickInterceptedException:
            continue
        time.sleep(0.1)
        return
    else:
        # If we ran out of time, blow up.
        raise TimeoutError(f"Cannot find link with the text '{link_text}'")


def click_button(webdriver: WebElement, button_text: str) -> None:
    """Click a button."""
    button = webdriver.find_element_by_xpath(f"//button[text() = '{button_text}']")
    button.click()


def wait_for_element(
    webdriver: WebElement, locator: str, method: str = By.ID, max_timeout: float = 4,
) -> WebElement:
    """Wait for an element to be present.

    Raises TimeoutError if max_timeout is exceeded.
    """
    start_time = time.time()
    while time.time() - start_time < max_timeout:
        # Try to find the element.
        try:
            return webdriver.find_element(by=method, value=locator)
        except NoSuchElementException:
            # If we can't find the link, keep trying...
            continue
    else:
        # If we ran out of time, blow up.
        raise TimeoutError(
            f"Cannot find element by {method} with the locator '{locator}'"
        )


def wait_for_elements(
    webdriver: WebElement, locator: str, method: str = By.ID, max_timeout: float = 4,
) -> List[WebElement]:
    """Wait for elements to be present.

    Raises TimeoutError if max_timeout is exceeded.
    """
    start_time = time.time()
    while time.time() - start_time < max_timeout:
        # Try to find the elements.
        elements = webdriver.find_elements(by=method, value=locator)
        if elements:
            return elements
    else:
        # If we ran out of time, blow up.
        raise TimeoutError(
            f"Cannot find elements by {method} with the locator '{locator}'"
        )


def wait_for_element_text_to_equal(
    webdriver: WebElement,
    locator: str,
    text_value: str,
    method: str = By.ID,
    max_timeout: float = 4,
) -> None:
    """Wait for an element to be present and for its text to equal some value.

    Raises TimeoutError if max_timeout is exceeded.
    """
    start_time = time.time()
    while time.time() - start_time < max_timeout:
        try:
            # Try to find the element.
            element = webdriver.find_element(by=method, value=locator)
            if element.text == text_value:
                return
        except StaleElementReferenceException:
            continue
    else:
        # If we ran out of time, blow up.
        raise TimeoutError(
            f"Cannot find elements by {method} with the locator '{locator}' and text '{text_value}'"
        )


def populate_text_box(text_box: WebElement, input_text: str) -> None:
    """Populate a textbox with some text."""
    while text_box.text != input_text:
        text_box.clear()
        text_box.send_keys(input_text)
    return


def populate_form(form: WebElement, form_data: dict) -> None:
    for name, value in form_data.items():
        form.find_element_by_name(name).send_keys(value)
