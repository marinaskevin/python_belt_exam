from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from ..main.models import User
from models import *

# GET REQUESTS

# GET list of quotes and display them
def index(request):

	if 'id' not in request.session:
		request.session['id'] = 0
	
	user = User.objects.filter(id = request.session['id']).first()

	context = {
		'user': user,
		'quotes': Quote.objects.exclude(favr_id = request.session['id']),
		'favs': user.favorites.all()
	}

	return render(request,'quotes/index.html',context)

def add_fav(request,id):

	if 'id' not in request.session:
		request.session['id'] = 0
		return redirect('/main')

	quote = Quote.objects.get(id=id)
	user = User.objects.get(id=request.session['id'])
	quote.favr_id.add(user)
	return redirect('/quotes')

def remove_fav(request,id):

	if 'id' not in request.session:
		request.session['id'] = 0
		return redirect('/main')

	quote = Quote.objects.get(id=id)
	user = User.objects.get(id=request.session['id'])
	quote.favr_id.remove(user)
	return redirect('/quotes')

# POST REQUESTS

def add_quote(request):

	# if 'id' not in request.session:
	# 	request.session['id'] = 0
	# 	return redirect('/main')

	if request.method != 'POST':
		return redirect('/quotes')

	response = Quote.objects.validateQuote(request.POST)
	if response['status']:
		messages.success(request,'Quote Added!')
	if response['errors']:
		for error in response['errors']:
			messages.error(request,error)
	return redirect('/quotes')