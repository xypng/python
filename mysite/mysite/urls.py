from django.conf.urls import url
from views import hello, current_datetime, hours_ahead, custom_info
from django.contrib import admin
from books.views import book_list, search, contact, thanks

urlpatterns = [
    url(r'^hello/$', hello),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^books/$', book_list),
    url(r'^admin/', admin.site.urls),
    url(r'^custominfo/$', custom_info),
    url(r'^search/$', search),
    url(r'^contact/$', contact),
    url(r'^contact/thanks/$', thanks),
]
