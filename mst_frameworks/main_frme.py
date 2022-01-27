import quopri
from mst_frameworks.requests import Get, Post


class Page_404:
    def __call__(self, request):
        """        
        :param request: 
        :return: 
        """
        return '404 WHAT', '404 Page not Fоund'


class MainFramework:
    """Класс MainFramework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        """
        :param routes_obj: 
        :param fronts_obj: 
        """
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        """
        :param environ: 
        :param start_response: 
        :return: 
        """
        # Получаем адрес(путь), по которому выполнен переход
        addr = environ['PATH_INFO']

        # Если в строке адреса нет закрывающего слеша,
        # добавляем его
        if not addr.endswith('/'):
            addr = f'{addr}/'

        request = {}
        # Получаем все данные запроса
        data_request = environ['REQUEST_METHOD']
        request['method'] = data_request

        if data_request == 'POST':
            data = Post().req_params(environ)
            request['data'] = MainFramework.decode(data)
            print('Пришел POST-запрос:', MainFramework.decode(data))
            with open('new_file.txt', 'a', encoding='utf-8') as f:
                f.write(f'{MainFramework.decode(data)}'+'\n')
        if data_request == 'GET':
            request_params = Get().req_params(environ)
            request['request_params'] = MainFramework.decode(request_params)
            print('Пришли GET-параметры:', MainFramework.decode(request_params))

        # Отработка паттерна page-controller
        # Находим нужный контроллер(view)
        if addr in self.routes_lst:
            view = self.routes_lst[addr]
        else:
            view = Page_404()

        # Отработка паттерна front-controller
        # Наполняем словарь request элементами
        # Словарь получает все контроллеры(view)
        for front in self.fronts_lst:
            front(request)
        # Запуск контроллера(view) с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode(data):
        """        
        :param data: 
        :return: 
        """
        new_value = {}
        for key, value in data.items():
            item = bytes(value.replace('%', '=').replace('+', ' '), 'utf-8')
            decode_str = quopri.decodestring(item).decode('utf-8')
            new_value[key] = decode_str
        return new_value


# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugApplication(MainFramework):

    def __init__(self, routes_obj, fronts_obj):
        """
        :param routes_obj:
        :param fronts_obj:
        """
        self.application = MainFramework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        """
        :param env:
        :param start_response:
        :return:
        """
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(MainFramework):

    def __init__(self, routes_obj, fronts_obj):
        """
        :param routes_obj:
        :param fronts_obj:
        """
        self.application = MainFramework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        """
        :param env:
        :param start_response:
        :return:
        """
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']