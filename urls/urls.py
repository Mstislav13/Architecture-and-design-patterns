from datetime import date
from views.views import Index, About, Contacts, MyCourseList, \
    CreateMyCourse, CategoryCreator, MyCategoryList, CourseCopy

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/create_my_course/': CreateMyCourse(),
    '/category_create/': CategoryCreator(),
    '/my_course_list/': MyCourseList(),
    '/my_category_list/': MyCategoryList(),
    '/course_copy/': CourseCopy(),    
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
