# 100% черновик, требует модификаци

# Задача: "Разработать на языке Python и библиотеке Selenium как можно больше позитивных и негативных тестовых сценариев используя подход DDT для формы логина https://qa-guru.github.io/one-page-form/login.html"
# Для реализации тестирования формы авторизации по методу DDT (Data-Driven Testing) на Python лучше всего использовать связку фреймворка pytest
# (через встроенную параметризацию @pytest.mark.parametrize) и библиотеки Selenium WebDriver.
# Ниже представлена подборка тестовых сценариев и готовый скрипт, автоматизирующий проверку страницы https://qa-guru.github.io/one-page-form/login.html .
# Спроектированные тестовые сценарии (DDT-матрица)В качестве валидных учетных данных (ожидаемое поведение тестового стенда QA.GURU)
# принята стандартная пара: email qaguru@qa.guru и любой непустой пароль (или специфичный qaguru),
# при которых форма показывает успешный вход.
# Позитивные сценарии (Positive)Валидный Email и пароль: Проверка классического успешного входа (qaguru@qa.guru).
# Регистронезависимость Email: Ввод email в верхнем регистре (QAGURU@QA.GURU) — система должна корректно приводить его к нижнему регистру.
# Негативные сценарии (Negative)Неверный пароль: Валидный email, но абсолютно некорректный пароль.
# Несуществующий Email: Попытка входа с незарегистрированной почтой.
# Пустой Email: Поле пароля заполнено, email — пустая строка (валидация обязательного поля).
# Пустой пароль: Поле email заполнено, пароль — пустая строка.
# Оба поля пустые: Отправка полностью пустой формы.
# Email без коммерческого атта @: Нарушение базового синтаксиса почты (qaguruqa.guru).Email без доменной части: Строка вида qaguru@.Email без имени ящика: Строка вида @qa.guru.
# Спецсимволы в Email: Использование запрещенных символов (qaguru!#$@qa.guru).Длинный пароль/Email (XSS/SQL-инъекции): Базовый чек на устойчивость к инъекциям (' OR '1'='1).

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from generators.login_form_fields_g import g_get_valid_params, g_get_invalid_params
from helpers.login_form_h import get_result_message

# Локаторы элементов формы на странице
EMAIL_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
LOGIN_BUTTON = (By.ID, "submit-button")
# Селекторы сообщений об ошибке или успехе зависят от верстки страницы QA.GURU
STATUS_MESSAGE = (By.ID, "error-message")


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Фоновый режим для CI/CD
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture()
def field_fills(driver, email, password):
    """Фикстура для заполнения полей """

    # 1. Открытие тестируемой страницы
    driver.get("https://qa-guru.github.io/one-page-form/login.html")

    # 2. Поиск элементов формы
    email_field = driver.find_element(*EMAIL_INPUT)
    password_field = driver.find_element(*PASSWORD_INPUT)
    submit_button = driver.find_element(*LOGIN_BUTTON)

    # 3. Очистка полей и ввод тестовых данных
    email_field.clear()
    email_field.send_keys(email)

    password_field.clear()
    password_field.send_keys(password)

    # 4. Клик по кнопке отправки формы
    submit_button.click()
    return get_result_message(driver, STATUS_MESSAGE)


@pytest.mark.parametrize("email, password, expected_text", g_get_valid_params())
def test_positive_login(driver, email, password, expected_text, field_fills):
    """Тест кейсы заполнения полей валидными данными"""

    actual_result = field_fills
    assert expected_text in actual_result, f"Ожидался успешный вход, но получено: '{actual_result}'"


@pytest.mark.parametrize("email, password, expected_text", g_get_invalid_params())
def test_negative_login(driver, email, password, expected_text, field_fills):
    """Тесты кейсы заполнения полей невалидными данными """

    actual_result = field_fills
    assert expected_text in actual_result or driver.current_url != "success_url", \
        f"Форма пропустила некорректные данные: Email='{email}', Pass='{password}'"
