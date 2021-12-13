from django.conf.urls import url
from . import views
from django.views import View

urlpatterns = [
	url(r'^submit',views.zabMonitoring.as_view(), name='zabMonitoring'),
]