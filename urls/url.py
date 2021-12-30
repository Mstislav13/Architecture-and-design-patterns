from datetime import date
from views.view import Index, About, Contact

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    }
    
# front controller(Контроллер запросов)
def date_front(request):
    request['date'] = date.today()


def another_front(request):
    request['something'] = 'something'

fronts = [date_front, another_front]
