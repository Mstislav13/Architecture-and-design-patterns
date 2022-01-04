from jinja2 import FileSystemLoader
from jinja2.environment import Environment

def open_template(template_name, folder='templates', **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param folder: папка с шаблоном
    :param kwargs: параметры
    :return:
    """
    # Создаем объект окружения
    env = Environment()

    # Указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)

    # Находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)
    