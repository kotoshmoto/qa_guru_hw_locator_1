import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from generators.box_form_fields_g import *

FULLNAME_INPUT = (By.ID, "userName")
EMAIL_INPUT = (By.ID, "userEmail")
CURRENT_ADDRESS_INPUT = (By.ID, "currentAddress")
PERMANENT_ADDRESS_INPUT = (By.ID, "permanentAddress")
SUBMIT_BUTTON = (By.ID, "submit")
RESULT_BOX = (By.ID, "output")


@pytest.fixture
def form_factory():
    def browser(driver, fullname, email, curr_addr, perm_addr):
        # Открытие страницы
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(5)

        # Поиск элементов и заполнение полей
        # Находим поле Full Name по его ID и вводим текст
        full_name_field = driver.find_element(*FULLNAME_INPUT)
        full_name_field.send_keys(fullname)

        # Находим поле Email по его ID и вводим текст
        email_field = driver.find_element(*EMAIL_INPUT)
        email_field.send_keys(email)

        # Находим поле Current Address по его ID и вводим текст
        current_address = driver.find_element(*CURRENT_ADDRESS_INPUT)
        current_address.send_keys(curr_addr)

        # Находим поле Permanent Address по его ID и вводим текст
        permanent_address = driver.find_element(*PERMANENT_ADDRESS_INPUT)
        permanent_address.send_keys(perm_addr)

        # Находим кнопку Submit по ее ID и кликаем
        submit_button = driver.find_element(*SUBMIT_BUTTON)
        submit_button.click()

        # Пауза, чтобы увидеть результат отправки
        time.sleep(5)

        result_box = driver.find_element(*RESULT_BOX)
        return result_box

    return browser


def test_fill_form_fields(form_factory):
    # Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        result_box = form_factory(driver=driver, fullname="Петров Петр Петрович", email="test@example.com",
                                  curr_addr="г. Москва, Пушкина 101", perm_addr="г. Москва, Комсомольский проспект 42")

        # Проверяем, что в блоке результата появился введенный текст
        assert "Петров Петр Петрович" in result_box.text
        print("Тест успешно пройден!")

    finally:
        # Закрытие браузера в любом случае
        driver.quit()


# Тесты валидные значения полей fullname, email, current_address, permanent_address
@pytest.mark.parametrize("params", g_get_valid_fields())
def test_fill_form_fields_with_valid_values(params, form_factory):
    # Запуск браузера Chrome
    driver = webdriver.Chrome()
    fullname, email, cur_addr, per_addr = params

    try:
        result_box = form_factory(driver=driver, fullname=fullname, email=email, curr_addr=cur_addr, perm_addr=per_addr)

        # Проверяем, что в блоке результата появился введенный текст
        assert [fullname, email, cur_addr, per_addr] in result_box.text
        print("Тест успешно пройден!")

    finally:
        # Закрытие браузера в любом случае
        driver.quit()


# Тесты невалидное значение e-mail
@pytest.mark.parametrize("email", g_get_invalid_email_and_injection_values())
def test_fill_form_with_invalid_email(email, form_factory):
    # Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        form_factory(driver=driver, fullname="Захаров Геннадий Павлович", email=email,
                     curr_addr="г. Санкт-Петербург, Ленина 12, 22",
                     perm_addr="г. Санкт-Петербург, Ленина 12, 24")

        validation_message = driver.find_element(*EMAIL_INPUT).get_property("validationMessage")
        assert (f'Адрес электронной почты должен содержать символ "@". В адресе "{email}"'
                f' отсутствует символ "@".') in validation_message

    finally:
        # 5. Закрытие браузера в любом случае
        driver.quit()


# Тесты невалидное значение fullname
@pytest.mark.parametrize("fullname", g_get_invalid_fullname_and_injection_values())
def test_fill_form_with_invalid_fullname(fullname, form_factory):
    # Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        form_factory(driver=driver, fullname=fullname, email="example@example.com",
                     curr_addr="г. Санкт-Петербург, Ленина 12, 22",
                     perm_addr="г. Санкт-Петербург, Ленина 12, 24")

        validation_message = driver.find_element(*FULLNAME_INPUT).get_property("validationMessage")
        assert "Поле Full Name должно содержать символы латиницы или кириллицы" in validation_message

    finally:
        # Закрытие браузера в любом случае
        driver.quit()


# Тесты невалидное значение current address
@pytest.mark.parametrize("curr_addr", g_get_invalid_curr_addr_and_injection_values())
def test_fill_form_with_invalid_curr_addr(curr_addr, form_factory):
    # Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        form_factory(driver=driver, fullname="Иванов Василий Павлович", email="ivanov@example.ru",
                     curr_addr=curr_addr, perm_addr="г. Санкт-Петербург, Ленина 12, 24")

        validation_message = driver.find_element(*CURRENT_ADDRESS_INPUT).get_property("validationMessage")
        assert "Поле Current Address должно содержать символы латиницы, кириллицы и цифры" in validation_message

    finally:
        # Закрытие браузера в любом случае
        driver.quit()


# # Тесты невалидное значение permanent address
@pytest.mark.parametrize("perm_addr", g_get_invalid_perm_addr_and_injection_values())
def test_fill_form_with_invalid_perm_addr(perm_addr, form_factory):
    # Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        form_factory(driver=driver, fullname="Иванов Василий Павлович", email="ivanov@example.ru",
                     curr_addr="г. Санкт-Петербург, Ленина 12, 24", perm_addr=perm_addr)

        validation_message = driver.find_element(*PERMANENT_ADDRESS_INPUT).get_property("validationMessage")
        assert "Поле Permanent Address должно содержать символы латиницы, кириллицы и цифры" in validation_message

    finally:
        # Закрытие браузера в любом случае
        driver.quit()
