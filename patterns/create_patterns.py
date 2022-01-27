import copy
import quopri
from patterns.behavioral_patterns import FileScriber, Person
from patterns.architect_system_pattern import ThingDomain
from sqlite3 import connect


class Human:
    """
    Класс - Потенциальный пользователь
    """
    def __init__(self, name):
        """
        :param name:
        """
        self.name = name


class Coach(Human):
    """
    Класс - Преподаватель
    """
    pass


class Client(Human, ThingDomain):
    """
    Класс - Клиент
    """
    def __init__(self, name):
        """
        :param name:
        """
        self.courses = []
        super().__init__(name)


class HumanFactory:
    """
    Порождающий паттерн - Фабричный метод
    """
    types = {
        'client': Client,
        'coach': Coach
    }
    
    @classmethod
    def create(cls, type_, name):
        """
        :param type_:
        :param name:
        :return:
        """
        return cls.types[type_](name)


# Порождающий паттерн - Прототип
class Prototype:
    """
    Класс - Прототип курсов обучения
    """
    def clone(self):
        return copy.deepcopy(self)


class MiCourse(Prototype, Person):
    """
    Класс - Курс
    """
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.clients = []
        super().__init__()

    def __getitem__(self, item):
        """
        :param item:
        :return:
        """
        return self.clients[item]

    def add_client(self, client: Client):
        self.clients.append(client)
        client.courses.append(self)
        self.notify()


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
    def create_human(type_, name):
        """
        :param type_:
        :param name:
        :return:
        """
        return HumanFactory.create(type_, name)

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

    def get_client(self, name) -> Client:
        """
        :param name:
        :return:
        """
        for item in self.clients:
            if item.name == name:
                return item

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
        """
        :param name:
        :param bases:
        :param attrs:
        :param kwargs:
        """
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
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
    def __init__(self, name, writer=FileScriber()):
        """
        :param name:
        :param writer:
        """
        self.name = name
        self.writer = writer
    
    def log(self, text):
        """
        :param text:
        :return:
        """
        text = f'log: {text}'
        self.writer.write(text)


class ClientMapper:
    """
    Mapper
    """
    def __init__(self, connection):
        """
        :param connection: 
        """
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'client'

    def collection(self):
        """
        :return:
        """
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            client = Client(name)
            client.id = id
            result.append(client)
        return result

    def search_by_id(self, id):
        """
        :param id:
        :return:
        """
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Client(*result)
        else:
            raise EggogNotRecord(f'record with id={id} not found')

    def data_insert(self, obj):
        """
        :param obj:
        :return:
        """
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise EggogCommitDb(e.args)

    def data_update(self, obj):
        """
        :param obj:
        :return:
        """
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise EggogUpdateDb(e.args)

    def data_delete(self, obj):
        """
        :param obj:
        :return:
        """
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise EggogDeleteDb(e.args)

connection = connect('site_bd.sqlite')


# Архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    """
    Класс - Mapper
    """
    mappers = {
        'client': ClientMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        """
        :param obj:
        :return:
        """
        if isinstance(obj, Client):

            return ClientMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        """
        :param name:
        :return:
        """
        return MapperRegistry.mappers[name](connection)


class EggogCommitDb(Exception):
    """
    Класс - Eggog Commit
    """
    def __init__(self, message):
        """
        :param message:
        """
        super().__init__(f'Ошибка фиксации БД: {message}')


class EggogUpdateDb(Exception):
    """
    Класс - Eggog Update
    """
    def __init__(self, message):
        """
        :param message:
        """
        super().__init__(f'Ошибка обновления БД: {message}')


class EggogDeleteDb(Exception):
    """
    Класс - Eggog Delete
    """
    def __init__(self, message):
        """
        :param message:
        """
        super().__init__(f'Ошибка удаления БД: {message}')


class EggogNotRecord(Exception):
    """
    Класс - Eggog Record
    """
    def __init__(self, message):
        """
        :param message:
        """
        super().__init__(f'Запись не найдена: {message}')
