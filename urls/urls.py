from datetime import date
from views.views import Index, About, Contact

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
}


# front controller(Контроллер запросов)
def date_front(request):
    """    
    :param request: 
    :return: 
    """
    request['date'] = date.today()


def another_front(request):
    """    
    :param request: 
    :return: 
    """
    request['something'] = 'something'


fronts = [date_front, another_front]
