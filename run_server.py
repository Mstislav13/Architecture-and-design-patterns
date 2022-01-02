from wsgiref.simple_server import make_server
from urls.urls import routes, fronts
from mst_frameworks.main_frme import MainFramework

apps = MainFramework(routes, fronts)

with make_server('', 8000, apps) as httpd:
    print('Запуск сервера через порт 8000')
    httpd.serve_forever()
