from mst_frameworks.template import open_template


class Index:
    """"""
    def __call__(self, request):
        return '200 - OK', open_template('index.html',
                                         date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 - OK', open_template('about.html',
                                         date=request.get('date', None))


class Contact:
    def __call__(self, request):
        return '200 - OK', open_template('contact.html',
                                         date=request.get('date', None))
