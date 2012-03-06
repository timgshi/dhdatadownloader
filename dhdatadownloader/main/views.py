from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django import forms
import csv
import datetime
from Frameworks import ParsePy
import xlwt

now = datetime.datetime.now()

class QueryForm(forms.Form):
    limit = forms.IntegerField()
    startdate = forms.DateField(now, '%m/%d/%y')
    enddate = forms.DateField(now, '%m/%d/%y')

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
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            return downloadFile(request)
    else: 
        form = QueryForm()
        t = loader.get_template('templates/download.html')
        c = RequestContext(request, {
            'form' : form,
        })
        return HttpResponse(t.render(c))

def downloadFile(request):

    response = HttpResponse(mimetype='text/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=dhdata-%s.xls' % now.strftime('%d-%m-%y')

    wb = xlwt.Workbook()
    ws = wb.add_sheet('DH Data')

    f = xlwt.Font()
    f.height = 20*10
    f.name = 'Arial'
    f.bold = False
    f.underline = xlwt.Font().UNDERLINE_SINGLE
    f.colour_index = 4

    h_style = xlwt.XFStyle()
    h_style.font = f
    
    query = ParsePy.ParseQuery("DHPhoto")
    query.order("updatedAt", True).limit(10)
    objects = query.fetch();
    headers = ['description', 'level', 'userID', 'location', 'latitude', 'longitude', 'date', 'photoURL']
    for x in range((len(headers))):
        ws.write(0,x,headers[x])
    row = 1
    for x in objects:
        data = [x.DHDataSixWord, x.DHDataHappinessLevel, x.PFUser._object_id, x.DHDataLocationString, x.geopoint._latitude, x.geopoint._longitude, x._created_at, x.photoData.url]
        for col in range((len(data))):
            if col == len(data) - 1:

                ws.write(row, col, xlwt.Formula("HYPERLINK" + '("%s";"photo")' % data[col]), h_style)
            else:
                ws.write(row, col, data[col])
        row += 1

    wb.save(response)

    return response
