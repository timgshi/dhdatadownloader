from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.contrib import sessions
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms, shortcuts
import csv
import datetime
from Frameworks import ParsePy
import xlwt
from bootstrap.forms import BootstrapForm, Fieldset
from models import DHPhoto, DHUserProfile
from django.db.models import Max

now = datetime.datetime.now()

class QueryForm(forms.Form):
    limit = forms.IntegerField()
    startdate = forms.DateField(now, '%m/%d/%y')
    enddate = forms.DateField(now, '%m/%d/%y')

class LoginForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please Login", "username", "username", "password"),
        )
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    username = forms.CharField(max_length=100)
    

ParsePy.APPLICATION_ID = "53Rdo20D9PA1hiPTN7qPzcPVaNQEmAkMXi3j6tLv"
ParsePy.MASTER_KEY = "FqhBINgpfI1ISF1ao2poRHYzvhbbr6PjJvuij0cq"



def index(request):
    loggedIn = False
    if 'session_id' in request.session:
        loggedIn = True
    x = 'hi'
    t = loader.get_template('templates/index.html')
    c = Context({
        'x' : x,
        'loggedIn' : loggedIn
    })
    return HttpResponse(t.render(c))

def download(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            return downloadFile(request)
    else: 
        bform = LoginForm()
        print bform
        t = loader.get_template('templates/download.html')
        c = RequestContext(request, {
            'form' : bform,
        })
        return HttpResponse(t.render(c))

def login(request):
    login_failed = False
    if 'session_id' in request.session:
        print "Logged In"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username =request.POST['username']
        password = request.POST['password']

        parseUser = ParsePy.ParseUser()
        parseUser.login(username, password)

        if parseUser.session_token:
            print parseUser.session_token
            # try:
            #     user = User.objects.get(username=username)
            #     print 'USER FOUND'
            # except User.DoesNotExist:
            #     print 'BEFORE USER'
            #     # user = User.objects.create_user(username=username, email=parseUser.email, password=password)
            #     user = User.objects.create_user('timshi', 'timgshi@gmail.com', 'a071170')
            #     # print 'USER: ' + user
            #     print 'BEFORE SAVE'
            #     user.save()
            #     print 'after save'
            #     # dhUserProfile = DHUserProfile()
            #     # dhUserProfile.user = user
            #     # dhUserProfile.parseToken = parseUser.session_token
            #     # dhUserProfile.save()

            # print 'BEFORE AUTHENTICATE'
            # user = authenticate(username=username, password=password)
            # print 'AFTER AUTHENTICATE'
            # print user
            # auth_login(request, user)
            # print 'AFTER LOGIN'
            request.session['session_id'] = parseUser.session_token
            request.session['user_id'] = parseUser._object_id
            return HttpResponseRedirect('/')
        else:
            login_failed = True
            print "LOGIN FAILED"

    t = loader.get_template('templates/login.html')
    bform = LoginForm()
    c = RequestContext(request, {
        'form' : bform,
        'login_failed' : login_failed
    })
    return HttpResponse(t.render(c))

def logout(request):
    try:
        del request.session['session_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def downloadFile(request):

    response = HttpResponse(mimetype='text/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=dhdata-%s.xls' % now.strftime('%d-%m-%y')

    if 'session_id' in request.session:
        updateDB()
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
        # limit = int(request.GET.get('limit'))
        # if limit > 1000 or limit < 0:
        #     limit = 20
        # print limit
        # query = ParsePy.ParseQuery("DHPhoto").limit(limit)
        # query.order("updatedAt", True)
        # objects = query.fetch();
        # headers = ['description', 'level', 'userID', 'location', 'latitude', 'longitude', 'date', 'photoURL']
        # for x in range((len(headers))):
        #     ws.write(0,x,headers[x])
        # row = 1
        # for x in objects:
        #     try:
        #         data = [x.DHDataSixWord, x.DHDataHappinessLevel, x.PFUser._object_id, x.DHDataLocationString, x.geopoint._latitude, x.geopoint._longitude, x._created_at, x.photoData.url]
        #         for col in range((len(data))):
        #             if col == len(data) - 1:
        #                 ws.write(row, col, xlwt.Formula("HYPERLINK" + '("%s";"photo")' % data[col]), h_style)
        #             else:
        #                 ws.write(row, col, data[col])
        #         row += 1
        #     except AttributeError:
        #         print("att error")

        # wb.save(response)
        objects = []
        personal = request.GET.get('personal')
        if personal == 'true':
            objects = DHPhoto.objects.filter(userID__iexact=request.session['user_id']).order_by('-timestamp')
        else:
            objects = DHPhoto.objects.order_by('-timestamp')
        # headers = ['description', 'level', 'userID', 'location', 'latitude', 'longitude', 'date', 'photoURL', 'objectID']
        # for x in range((len(headers))):
        #     ws.write(0,x,headers[x])
        # row = 1
        # for photo in objects:
        #     data = [photo.description, photo.level, photo.userID, photo.location, photo.latitude, photo.longitude, photo.timestamp.strftime("%Y-%m-%d %H:%M:%S"), photo.photoURL, photo.objectID]
        #     for col in range((len(data))):
        #         if col == len(data) - 2:
        #             ws.write(row, col, xlwt.Formula("HYPERLINK" + '("%s";"photo")' % data[col]), h_style)
        #         else:
        #             ws.write(row, col, data[col])
        #     row += 1
        headers = []
        row = 1
        for photo in objects:
            for x in photo.params:
                if x not in 'DHDataWhoTook' and x not in 'ACL':
                    col = 0
                    try:
                        col = headers.index(x)
                    except ValueError:
                        headers.append(x)
                        col = headers.index(x)
                    ws.write(row, col, "%s" % photo.params.get(x))
            row += 1
        for header in headers:
            ws.write(0, headers.index(header), header)

        wb.save(response)
    else:
        wb = xlwt.Workbook()
        ws = wb.add_sheet('DH Data')
        ws.write(0,0,'NOT LOGGED IN')
        WS.WRITE(1,0, 'TRY LOGGING OUT AND BACK IN')
        ws.save(response)

    return response

def updateDB():
    print "updateDB"
    try:
        latestPhoto = DHPhoto.objects.latest('timestamp')
        # latestPhoto = DHPhoto.objects.order_by('-timestamp')[:1][0]
        total = 0
        while True:
            query = ParsePy.ParseQuery("DHPhoto")
            combined = '{"__type":"Date","iso":"' + latestPhoto.timestamp.strftime('%Y-%m-%dT%H:%M:%S') + '"}'
            query.gte('updatedAt', combined)
            query.order("updatedAt", False)
            query.limit(100).skip(total)
            print "Fetching..."
            objects = query.fetch()
            print "...done"
            count = 0
            for x in objects:
                print "\n===NEW PHOTO====\n"
                print x.__dict__
                try:
                    try:
                       
                        existingPhoto = DHPhoto.objects.get(objectID=x.objectId())
                        existingPhoto.delete()
                        photo = DHPhoto(description=x.DHDataSixWord, level=x.DHDataHappinessLevel, userID=x.PFUser._object_id, location=x.DHDataLocationString, latitude=x.geopoint._latitude, longitude=x.geopoint._longitude, timestamp=x.createdAt(), photoURL=x.photoData.url, objectID=x.objectId(), params=x.__dict__)
                        photo.save()
                        print 'photo updated'
                    except DHPhoto.DoesNotExist:
                        print "before create"
                        photo = DHPhoto(description=x.DHDataSixWord, level=x.DHDataHappinessLevel, userID=x.PFUser._object_id, location=x.DHDataLocationString, latitude=x.geopoint._latitude, longitude=x.geopoint._longitude, timestamp=x.createdAt(), photoURL=x.photoData.url, objectID=x.objectId(), params=x.__dict__)
                        print "before save"
                        print photo
                        photo.save()
                except AttributeError:
                    print "ATT ERROR"
                    pass
                count += 1
                print count
            total += count
            print total
            if count == 0:
                break
            
    except (DHPhoto.DoesNotExist):
        print "does not exist"
        total = 0
        while True:
            print "new loop"
            query = ParsePy.ParseQuery("DHPhoto").limit(100).skip(total)
            query.order("updatedAt", True)
            print "Fetching......."
            objects = query.fetch();
            print "....done"
            count = 0
            for x in objects:
                try:
                    try:
                        existingPhoto = DHPhoto.objects.get(objectID=x.objectId())
                    except DHPhoto.DoesNotExist:
                        photo = DHPhoto(description=x.DHDataSixWord, level=x.DHDataHappinessLevel, userID=x.PFUser._object_id, location=x.DHDataLocationString, latitude=x.geopoint._latitude, longitude=x.geopoint._longitude, timestamp=x.createdAt(), photoURL=x.photoData.url, objectID=x.objectId(), params=x.__dict__)
                        photo.save()
                except AttributeError:
                    pass
                count += 1
                print count
            total += count
            print total
            if count == 0:
                break

