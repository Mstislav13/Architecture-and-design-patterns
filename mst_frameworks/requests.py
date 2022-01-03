# get request
class Get:
    """
    get-запрос
    """
    @staticmethod
    def get_input(data: str):
        """
        Разбор входных данных
        :param data:
        :return:
        """
        dict_input = {}
        if data:
            # Делим параметры через '&'
            input_data = data.split('&')
            for item in input_data:
                # Делим ключ и значение через '='
                key, value = item.split('=')
                dict_input[key] = value
        return dict_input

    @staticmethod
    def req_params(env):
        """
        Получаем параметры запроса
        :param env:
        :return:
        """
        query_string = env['QUERY_STRING']
        # Превращаем параметры в словарь
        request_dict = Get.get_input(query_string)
        return request_dict


# post request
class Post:
    """
    post-запрос
    """
    @staticmethod
    def post_input(data: str):
        """
        Разбор входных данных
        :param data:
        :return:
        """
        dict_input = {}
        if data:
            # Делим параметры через '&'
            input_data = data.split('&')
            for item in input_data:
                # Делим ключ и значение через '='
                key, value = item.split('=')
                dict_input[key] = value
        return dict_input

    @staticmethod
    def wsgi_get_input_data(env) -> bytes:
        """
        :param env:
        :return:
        """
        # Получаем длину тела
        length_content = env.get('CONTENT_LENGTH')
        # Приводим к int
        content_length = int(length_content) if length_content else 0
        print('content_length:', content_length)
        # Считываем данные, если они есть
        # env['wsgi.input'] -> <class '_io.BufferedReader'>
        # запускаем режим чтения
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def wsgi_parse_input_data(self, data: bytes) -> dict:
        """
        :param data:
        :return:
        """
        data_dict = {}
        if data:
            # Декодируем данные
            string = data.decode(encoding='utf-8')
            print('Строка после декодирования:', string)
            # Собираем данные в словарь
            data_dict = self.post_input(string)
        return data_dict

    def req_params(self, environ):
        """
        :param environ:
        :return:
        """
        # Получаем данные
        data = self.wsgi_get_input_data(environ)
        # Превращаем данные в словарь
        data = self.wsgi_parse_input_data(data)
        return data
        