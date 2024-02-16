#1
import os
from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        # Открываем файл для записи
        with open('main.log', 'a') as log_file:
            # Получаем текущую дату и время
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Записываем информацию о вызове функции
            log_file.write(f'{timestamp} - {old_function.__name__} - args: {args}, kwargs: {kwargs}\n')
            # Вызываем исходную функцию
            result = old_function(*args, **kwargs)
            # Записываем информацию о возвращаемом значении
            log_file.write(f'{timestamp} - {old_function.__name__} - return: {result}\n')
            # Возвращаем результат выполнения функции
            return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


#2
import os
import datetime


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            # Открываем файл для записи в режиме добавления
            with open(path, 'a') as log_file:
                # Записываем дату и время вызова функции
                log_file.write(f'[{datetime.datetime.now()}] ')
                # Записываем имя функции
                log_file.write(f'{old_function.__name__} ')
                # Записываем аргументы, с которыми вызвалась функция
                log_file.write(f'args={args} kwargs={kwargs} ')
                # Вызываем декорированную функцию
                result = old_function(*args, **kwargs)
                # Записываем возвращаемое значение функции
                log_file.write(f'result={result}\n')
                return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()

#3
import types
import os
import datetime


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            # Получаем текущую дату и время
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Открываем файл в режиме добавления
            with open(path, 'a') as log_file:
                # Записываем информацию о вызове функции
                log_file.write(f"Дата и время вызова: {current_time}\n")
                log_file.write(f"Имя функции: {old_function.__name__}\n")
                log_file.write(f"Аргументы: {args}, {kwargs}\n")

                # Вызываем исходную функцию
                result = old_function(*args, **kwargs)

                # Записываем информацию о возвращаемом значении
                log_file.write(f"Возвращаемое значение: {result}\n")

            return result

        return new_function

    return __logger


@logger('log.txt')
def flat_generator(list_of_lists):
    for sublist in list_of_lists:
        for item in sublist:
            yield item


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
