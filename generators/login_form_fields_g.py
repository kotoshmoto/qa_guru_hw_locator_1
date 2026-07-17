from typing import List


# ------------ POSITIVE DATA ------------

def g_get_valid_params() -> List[List[str]]:
    return [["qaguru@qa.guru", "qaguru", "Вы успешно вошли"],
            ["QAGURU@QA.GURU", "qaguru", "Вы успешно вошли"]]


# ------------ NEGATIVE DATA ------------

def g_get_invalid_params() -> List[List[str]]:
    return [["qaguru@qa.guru", "wrong_pass", "Неверный пароль"],
            ["unknown@qa.guru", "qaguru", "Такого пользователя не существует"],
            ["", "qaguru", "Заполните поле Email"],
            ["qaguru@qa.guru", "", "Заполните поле Пароль"],
            ["", "", "Заполните поля"],
            ["qaguruqa.guru", "qaguru", "Email должен содержать символ @"],
            ["qaguru@", "qaguru", "Введен некорректный Email"],
            ["@qa.guru", "qaguru", "Введен некорректный Email"],
            ["qaguru' OR '1'='1", "' OR '1'='1", "Некорректные данные"]]
