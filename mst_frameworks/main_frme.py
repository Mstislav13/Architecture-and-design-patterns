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

        # Отработка паттерна page-controller
        # Находим нужный контроллер(view)
        if addr in self.route_list:
            view = self.route_list[addr]
        else:
            view = Page_404()

        request = {}
        # Отработка паттерна front-controller
        # Наполняем словарь request элементами
        # Словарь получает все контроллеры(view)
        for front in self.front_list:
            front(request)
        # Запуск контроллера(view) с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

class Page_404:
    def __call__(self, request):
        return '404 - Page not found'
