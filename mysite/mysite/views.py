from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.shortcuts import render_to_response
import datetime
import MySQLdb

def hello(request):
    return HttpResponse("hello world")

def current_datetime(request):
    current_datetime = str(datetime.datetime.now())
    # t = Template("<html><body>current time is {{ now }}</body></html>")
    # c = Context({'now': str(now)})
    # return HttpResponse(t.render(c))
    title = 'current_datetime'
    return render_to_response('current_datetime.html', locals())

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    now = datetime.datetime.now()
    dt = now + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s</body></html>" % (offset, dt)
    return HttpResponse(html)

# def book_list(request):
#     db = MySQLdb.connect(user='xypng', db='mydb', passwd='123456', host='localhost')
#     cursor = db.cursor()
#     cursor.execute('SELECT name FROM books ORDER BY name')
#     names = [row[0] for row in cursor.fetchall()]
#     db.close()
#     return render_to_response('booklist.html', {'names': names})

def custom_info(request):
    values = request.META.items()
    values.sort()
    return render_to_response('custom_info.html', {'values': values, 'request': request})