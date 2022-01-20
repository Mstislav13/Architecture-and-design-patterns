import copy
import quopri


class Human:
    """
    Класс - Потенциальный пользователь
    """
    pass


class Coach(Human):
    """
    Класс - Преподаватель
    """
    pass


class Client(Human):
    """
    Класс - Клиент
    """
    pass


class HumanFactory:
    """
    Порождающий паттерн - Фабричный метод
    """
    types = {
        'client': Client,
        'coach': Coach
    }
    
    @classmethod
    def create(cls, type_):
        """
        :param type_:
        :return:
        """
        return cls.types[type_]()


# Порождающий паттерн - Прототип
class Prototype:
    """
    Класс - Прототип курсов обучения
    """
    def clone(self):
        return copy.deepcopy(self)


class MiCourse(Prototype):
    """
    Класс - Курс
    """
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class IntMiCourse(MiCourse):
    """
    Курс - Интерактивный курс
    """
    pass


class RecMiCourse(MiCourse):
    """
    Класс - Запись курсов
    """
    pass


class MiCourseFactory:
    """
    Класс - Фабрика курсов
    """
    types = {
        'interactive': IntMiCourse,
        'record': RecMiCourse
    }

    # Порождающий паттерн - Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        """
        :param type_:
        :param name:
        :param category:
        :return:
        """
        return cls.types[type_](name, category)


class Category:
    """
    Класс - Категория
    """
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        """
        :return:
        """
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    """
    Класс - Основной интерфейс проекта
    """
    def __init__(self):
        self.coachs = []
        self.clients = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_human(type_):
        """
        :param type_:
        :return:
        """
        return HumanFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        """
        :param name:
        :param category:
        :return:
        """
        return Category(name, category)

    def find_category_id(self, id):
        """
        :param id:
        :return:
        """
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_my_course(type_, name, category):
        """
        :param type_:
        :param name:
        :param category:
        :return:
        """
        return MiCourseFactory.create(type_, name, category)

    def get_my_course(self, name):
        """
        :param name:
        :return:
        """
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        """
        :param val:
        :return:
        """
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """
    Класс - Порождающий паттерн Синглтон
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    """
    Класс - Логгер
    """
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        """
        :param text:
        :return:
        """
        print('log ==>', text)
