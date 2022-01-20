from datetime import date
# from views.views import Index, About, Contacts

# routes = {
#     '/': Index(),
#     '/about/': About(),
#     '/contacts/': Contacts(),
# }

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
