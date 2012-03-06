from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    x = 'hi'
    t = loader.get_template('templates/index.html')
    c = Context({
        'x' : x
    })
    return HttpResponse(t.render(c))
