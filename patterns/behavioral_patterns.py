from jsonpickle import dumps, loads
from mst_frameworks.template import open_template


# Курс
class BigBrother:
    """
    Поведенческий паттерн - Наблюдатель
    """
    def update(self, person):
        """
        :param person:
        :return:
        """
        pass


class Person:
    """
    Объект наблюдения
    """
    def __init__(self):
        self.observers = []

    def notify(self):
        """
        :return:
        """
        for item in self.observers:
            item.update(self)


class SmsNotifier(BigBrother):
    """
    Уведомление по-Sms
    """
    def update(self, person):
        """
        :param person:
        :return:
        """
        print('SMS: ', 'к нам присоединился - ', person.clients[-1].name)


class EmailNotifier(BigBrother):
    """
    Уведомление по-Email
    """
    def update(self, person):
        """
        :param person:
        :return:
        """
        print(('EMAIL: ', 'к нам присоединился - ', person.clients[-1].name))


class PrimarySerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        """
        :return:
        """
        return dumps(self.obj)

    @staticmethod
    def load(data):
        """
        :param data:
        :return:
        """
        return loads(data)


# Поведенческий паттерн - Шаблонный метод
class SampleView:
    template_name = 'template.html'

    def get_context_data(self):
        """
        :return:
        """
        return {}

    def get_template(self):
        """
        :return:
        """
        return self.template_name

    def render_template_with_context(self):
        """
        :return:
        """
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', open_template(template_name, **context)

    def __call__(self, request):
        """
        :param request:
        :return:
        """
        return self.render_template_with_context()


class ScrollView(SampleView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        """
        :return:
        """
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        """
        :return:
        """
        return self.context_object_name

    def get_context_data(self):
        """
        :return:
        """
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class BuildView(SampleView):
    """
    Создание шаблона
    """
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        """
        :param request:
        :return:
        """
        return request['data']

    def create_obj(self, data):
        """
        :param data:
        :return:
        """
        pass

    def __call__(self, request):
        """
        :param request:
        :return:
        """
        if request['method'] == 'POST':
            # Метод - 'POST'
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


# Поведенческий паттерн - Стратегия
class ConsoleScriber:
    """
    Вывод в консоль
    """
    def write(self, text):
        """
        :param text:
        :return:
        """
        print(text)


class FileScriber:
    """
    Вывод в файл
    """
    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        """
        :param text:
        :return:
        """
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
