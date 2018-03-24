from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index), # index redirects to main
	url(r'^main$',views.main), # shows register and login if not logged in, otherwise redirects to localhost/quotes
	url(r'^users$',views.user), # redirects to users/< request.session["id"] >
	url(r'^users/(?P<id>[0-9])$',views.users),
	url(r'^register$',views.register),
	url(r'^success$',views.success),
	url(r'^login$',views.login),
	url(r'^logout$',views.logout),
	]