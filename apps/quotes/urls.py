from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^add$',views.add_quote),
	url(r'^(?P<id>[0-9])/fav',views.add_fav),
	url(r'^(?P<id>[0-9])/unfav',views.remove_fav)
	]
