import random
from typing import List

from faker import Faker


# Валидные поля fullname, email, current address, permanent address
def g_get_valid_fields() -> List[List]:
    fake = Faker()
    lst = []

    for i in range(5):
        lst.append([fake.name(), fake.email(), fake.address(), fake.secondary_address()])

    return lst


# Невалидные значения поля fullname
def g_get_invalid_fullname():
    lst = [
        "",
        "   ",
        "123456",
        "Ivan@Petrov",
    ]
    return lst


# Невалидное поле email
def g_get_invalid_email():
    allowed_chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    longer_email = f'{"".join(random.choice(allowed_chars) for _ in range(1000))}example.com'

    spec_symbol = ",!#$%^&"
    spec_symbol_lst = []

    for i in spec_symbol:
        spec_symbol_lst.append(f"example{i}gmail.com")

    lst = ["test_example.com", "Пустое поле нет ошибки", longer_email, random.choice(spec_symbol_lst)]
    return lst


# sql, json инъекции
def g_get_injection_values():
    lst = ["<script>alert('xss')</script>", "1' OR '1'='1", ":):):):))))::;)", "<div>HTML injection</div>"]

    return lst


# Невалидные значения поля current address
def g_get_invalid_current_address():
    lst = [
        "",
        "   ",
        "123456",
        "Ivan@Petrov",
    ]
    return lst


# Невалидные значения поля current address
def g_get_invalid_permanent_address():
    lst = [
        "",
        "   ",
        "123456",
        "Ivan@Petrov",
    ]
    return lst


def g_get_invalid_fullname_and_injection_values():
    return g_get_invalid_fullname() + g_get_injection_values()


def g_get_invalid_email_and_injection_values():
    return g_get_invalid_email() + g_get_injection_values()


def g_get_invalid_curr_addr_and_injection_values():
    return g_get_invalid_current_address() + g_get_injection_values()


def g_get_invalid_perm_addr_and_injection_values():
    return g_get_invalid_permanent_address() + g_get_injection_values()
