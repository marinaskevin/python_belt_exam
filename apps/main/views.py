from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from ..quotes.models import *
from models import *

def index(request):
	return redirect ('/main')

# GET REQUESTS

def main(request):
	if 'id' not in request.session:
		request.session['id'] = 0
	context = {
		'user': User.objects.filter(id = request.session['id']).first()
	}
	return render(request,'main/index.html',context)

def user(request):
	if 'id' not in request.session:
		request.session['id'] = 0
		return redirect('/main')
	return redirect('/users/'+str(request.session['id']))

def users(request,id):
	try:
		user = User.objects.get(id = id)
		context = {
			'user': user,
			'quotes': user.submissions.all(),
			'count': user.submissions.count()
		}
		print context
		return render(request,'main/user.html',context)	
	except Exception as e:
		raise
	else:
		return redirect('/main')

def logout(request):
	request.session.clear()
	return redirect('/main')

# POST REQUESTS

def register(request):
	if request.method != 'POST':
		return redirect('/main')
	response = User.objects.validateRegistration(request.POST)
	if response['status']:
		messages.success(request,'Registration Successful!')
		request.session.clear()
		request.session["id"] = response['user_id']
		return redirect('/success')
	if response['errors']:
		for error in response['errors']:
			messages.error(request,error)
		for key in response['feedback']:
			request.session[key] = response['feedback'][key]
		return redirect('/main')

def login(request):
	if request.method != 'POST':
		return redirect('/main')

	email = request.POST['email']

	if len(User.objects.filter(email=email)) > 0:
		if bcrypt.checkpw(request.POST['password'].encode(), User.objects.filter(email=email).first().pw_hash.encode()):
			print "Password MATCHES"
			user = User.objects.filter(email=email).first()
			request.session["id"] = user.id
			messages.success(request, 'Successfully logged in!')
			return redirect('/success')
		else:
			print "Password is incorrect!"
			messages.error(request, 'Password is incorrect.')
	else:
		print "User does not exist!"
		messages.error(request, 'User does not exist.')	
	return redirect('/main')

# OUTCOME REDIRECTS

def success(request):
	no_messages = True
	messages = get_messages(request)
	for message in messages:
		no_messages = False
		break
	if 'id' not in request.session or no_messages:
		return redirect('/main')
	context = {
		'user': User.objects.filter(id = request.session['id']).first()
	}
	return redirect('/quotes')