from django.http import HttpResponse
from django.template import Context, loader
import csv
from Frameworks import ParsePy

ParsePy.APPLICATION_ID = "53Rdo20D9PA1hiPTN7qPzcPVaNQEmAkMXi3j6tLv"
ParsePy.MASTER_KEY = "FqhBINgpfI1ISF1ao2poRHYzvhbbr6PjJvuij0cq"

def index(request):
    x = 'hi'
    t = loader.get_template('templates/index.html')
    c = Context({
        'x' : x
    })
    return HttpResponse(t.render(c))

def download(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filname=download.csv'

    writer = csv.writer(response)
    query = ParsePy.ParseQuery("DHPhoto")
    query.order("updatedAt").limit(2)
    objects = query.fetch();

    writer.writerow(['', 'description', 'username'])
    for x in objects:
        writer.writerow(['', x.DHDataSixWord, x.DHDataWhoTook])

    return response
