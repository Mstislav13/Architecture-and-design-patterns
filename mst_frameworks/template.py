from jinja2 import Template
from os.path import join


def open_template(template_name, folder='templates', **kwargs):
    """
    Функция рендера шаблона.
    :param template_name: имя шаблона
    :param folder: папка в которой находится шаблон
    :param kwargs: параметры
    :return:
    """
    path_to_file = join(folder, template_name)
    # Открытие файла-шаблона
    with open(path_to_file, encoding='utf-8') as file:
        # Чтение файла-шаблона
        temp_file = Template(file.read())
    # Рендер файла-шаблона с параметрами
    return temp_file.render(**kwargs)
