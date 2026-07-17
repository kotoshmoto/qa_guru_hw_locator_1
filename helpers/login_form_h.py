from typing import cast

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_result_message(driver, status_message_locator: tuple[str, str], ) -> str:
    try:
        alert = cast(Alert, WebDriverWait(driver, 2).until(EC.alert_is_present()), )
        message = alert.text
        alert.accept()
        return message

    except TimeoutException:
        return WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(status_message_locator)
        ).text
