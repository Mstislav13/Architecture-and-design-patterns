from time import time


class MyRouter:
    """
    Структурный паттерн - Декоратор
    """
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        :param routes: 
        :param url: 
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        :param cls: 
        :return: 
        """
        self.routes[self.url] = cls()


class Debug:
    """
    Структурный паттерн - Декоратор
    """
    def __init__(self, name):
        """        
        :param name: 
        """
        self.name = name

    def __call__(self, cls):
        """
        Сам декоратор
        :param cls: 
        :return: 
        """
        # Вспомогательная функция которая будет декорировать каждый отдельный
        # метод класса.
        def timeit(method):
            """
            Нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            :param method: 
            :return: 
            """            
            def timed(*args, **kwargs):
                """                
                :param args: 
                :param kwargs: 
                :return: 
                """
                start_time = time()
                result = method(*args, **kwargs)
                finish_time = time()
                delta_time = finish_time - start_time

                print(f'debug: {self.name} выполнялся {delta_time:2.2f} ms')
                return result
            return timed
        return timeit(cls)
        