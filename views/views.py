from mst_frameworks.template import open_template


class Index:
    def __call__(self, request):
        return '200 OK', open_template('index.html',
                                data=request.get('data', None))


class About:
    def __call__(self, request):
        return '200 OK', open_template('about.html',
                                data=request.get('data', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', open_template('contacts.html',
                                data=request.get('data', None))