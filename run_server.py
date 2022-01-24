from wsgiref.simple_server import make_server
from mst_frameworks.main_frme import MainFramework
from urls.urls import fronts
from views.views import routes

app = MainFramework(routes, fronts)

with make_server('', 8000, app) as httpd:
    print('Запуск сервера через порт 8000')    
    httpd.serve_forever()
