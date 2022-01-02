from quopri import decodestring # Декодирует содержимое файла input.
                                # Принимает источник bytes и возвращает 
                                # соответствующий декодированный bytes.
from mst_frameworks.requests import Get, Post


class MainFramework:
    """
    Класс MainFramework база для фреймворка
    """

    def __init__(self, route_obj, front_obj):
        self.route_list = route_obj
        self.front_list = front_obj

    def __call__(self, environ, start_response):
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
            data = Post().request_params(environ)
            request['data'] = MainFramework.decode(data)
            print(f'Пришел POST-запрос: {MainFramework.decode(data)}')
            with open('new_file.txt', 'w', encoding='utf-8') as f:
                f.write(f'{MainFramework.decode(data)}')
        if data_request == 'GET':
            request_params = Get().request_params(environ)
            request['request_params'] = MainFramework.decode(request_params)
            print(f'Пришли GET-параметры:'
                  f' {MainFramework.decode(request_params)}')

        # Отработка паттерна page-controller
        # Находим нужный контроллер(view)
        if addr in self.route_list:
            view = self.route_list[addr]
        else:
            view = Page_404()
        
        # Отработка паттерна front-controller
        # Наполняем словарь request элементами
        # Словарь получает все контроллеры(view)
        for front in self.front_list:
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
            item = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            decode_str = decodestring(item).decode('UTF-8')
            new_value[key] = decode_str
        return new_value


class Page_404:
    def __call__(self, request):
        return '404 - Page not found'
