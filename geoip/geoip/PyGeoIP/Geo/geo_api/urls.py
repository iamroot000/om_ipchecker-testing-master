from django.conf.urls import url
from . import views
from django.views import View

urlpatterns = [
	url(r'^$',views.showInfo.as_view(), name='showInfo'),
	url(r'^submit',views.getInfo.as_view(), name='getInfo'),
]
