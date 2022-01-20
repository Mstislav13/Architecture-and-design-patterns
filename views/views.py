from datetime import date
from mst_frameworks.template import open_template
from patterns.create_patterns import Engine, Logger
from patterns.structur_patterns import MyRouter, Debug

site_page = Engine()
logger = Logger('main')

routes = {}


@MyRouter(routes=routes, url='/')
class Index:
    """
    Контроллер - главная страница
    """
    @Debug(name='Index')
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        return '200 OK', open_template('index.html', 
                                    objects_list=site_page.categories)


@MyRouter(routes=routes, url='/about/')
class About:
    """
    Контроллер "О проекте"
    """
    @Debug(name='About')
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        return '200 OK', open_template('about.html', date=date.today())


@MyRouter(routes=routes, url='/contacts/')
class Contacts:
    """
    Контроллер "Контакты"
    """
    @Debug(name='Contacts')
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        return '200 OK', open_template('contacts.html')


class NotFound:
    """
    Контроллер "Eggog - 404"
    """
    @Debug(name='NotFound')
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        return '404 WHAT', '404 PAGE Not Found'


@MyRouter(routes=routes, url='/create_my_course/')
class CreateMyCourse:
    """
    Контроллер 'Создание курса'
    """
    cat_id = -1

    def __call__(self, request):
        """
        :param request:
        :return:
        """
        if request['method'] == 'POST':
            # Метод 'POST'
            data = request['data']
            name = data['name']
            name = site_page.decode_value(name)

            category = None
            if self.cat_id != -1:
                category = site_page.find_category_id(int(self.cat_id))
                course = site_page.create_my_course('record', name, category)
                site_page.courses.append(course)
            return '200 OK', open_template('course_list.html',
                                            objects_list=category.courses,
                                            name=category.name,
                                            id=category.id)
        else:
            try:
                self.cat_id = int(request['request_params']['id'])
                category = site_page.find_category_id(int(self.cat_id))
                return '200 OK', open_template('create_course.html',
                                                name=category.name,
                                                id=category.id)
            except KeyError:
                return '200 OK', 'Категории еще не добавлены'


@MyRouter(routes=routes, url='/category_create/')
class CategoryCreator:
    """
    Контроллер 'Создание категории'
    """
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        if request['method'] == 'POST':
            # Метод 'POST'
            data = request['data']
            name = data['name']
            name = site_page.decode_value(name)

            cat_id = data.get('category_id')

            category = None
            if cat_id:
                category = site_page.find_category_id(int(cat_id))
            next_category = site_page.create_category(name, category)
            site_page.categories.append(next_category)
            return '200 OK', open_template('index.html', 
                                            objects_list=site_page.categories)
        else:
            categories = site_page.categories
            return '200 OK', open_template('create_category.html',
                                            categories=categories)


@MyRouter(routes=routes, url='/my_course_list/')
class MyCourseList:
    """
    Контроллер 'Список курсов'
    """
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        logger.log('Список курсов')
        try:
            item = site_page.find_category_id(
                int(request['request_params']['id']))
            return '200 OK', open_template('course_list.html',
                                            objects_list=item.courses,
                                            name=item.name, 
                                            id=item.id)
        except KeyError:
            return '200 OK', 'Курсы еще не добавлены'


@MyRouter(routes=routes, url='/my_category_list/')
class MyCategoryList:
    """
    Контроллер 'Список категорий'
    """
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        logger.log('Список категорий')
        return '200 OK', open_template('category_list.html',
                                        objects_list=site_page.categories)


@MyRouter(routes=routes, url='/course_copy/')
class CourseCopy:
    """
    Контроллер 'Копирование курса'
    """
    def __call__(self, request):
        """
        :param request:
        :return:
        """
        req_params = request['request_params']

        try:
            name = req_params['name']
            elder_course = site_page.get_my_course(name)
            if elder_course:
                next_name = f'copy_{name}'
                next_course = elder_course.clone()
                next_course.name = next_name
                site_page.courses.append(next_course)

            return '200 OK', open_template('course_list.html',
                                    objects_list=site_page.courses,
                                    name=next_course.category.name)
        except KeyError:
            return '200 OK', 'Курсы еще не добавлены'
