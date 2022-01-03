from os.path import join
from jinja2 import Template


def open_template(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка с шаблоном
    :param kwargs: параметры
    :return:
    """
    path_to_file = join(folder, template_name)

    with open(path_to_file, encoding='utf-8') as file:
        temp_file = Template(file.read())

    return temp_file.render(**kwargs)
    