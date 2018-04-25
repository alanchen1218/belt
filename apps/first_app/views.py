from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Q
import bcrypt
from .models import *

# the index function is called when root is visited
def index(request):
  return render(request, 'first_app/index.html')
  request.session.clear()

def register(request):
  errors = User.objects.nameValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
      request.session['fullname'] = request.POST['fullname']
      request.session['alias'] = request.POST['alias']
      request.session['email'] = request.POST['email']
      return redirect('/')
  else:
    request.session.clear()
    pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(fullname = request.POST['fullname'], email = request.POST['email'], alias = request.POST['alias'], password = pwhash)
    request.session['fullname'] = request.POST['fullname']
    # request.session['id'] = User.objects.get(username=request.POST['username']).id
    request.session['id'] = user.id
    return redirect('/quotes')

def login(request):
  errors = User.objects.loginValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:
    user = User.objects.get(email=request.POST['email'])
    request.session['fullname'] = User.objects.get(email=request.POST['email']).fullname
    # request.session['id'] = User.objects.get(username=request.POST['username']).id
    request.session['id'] = user.id
    print (request.session['id'])
    return redirect('/quotes')
  
def quotes(request):
  currentUser = User.objects.get(id = request.session['id'])
  request.session['id'] = currentUser.id
  quotes = Quote.objects.all()
  context = {
    'quotes': quotes,
    'myquotes' : Quote.objects.all(),
    'notliked' : Quote.objects.filter(~Q(liked_users=currentUser) & ~Q(added_by=currentUser)),
    'liked' : Quote.objects.filter(liked_users  = currentUser),
  }
  return render(request, 'first_app/quotes.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def create(request):
  errors = Quote.objects.QuoteManager(request.POST)
  if (errors):
    for key, value in errors.items():
      messages.error(request, value)
      return redirect('/quotes')
  else:
    Quote.objects.create(message = request.POST['message'], quotedby = request.POST['quotedby'] ,added_by = User.objects.get(id=request.session['id']))
    return redirect('/quotes')
    
def remove(request, number):
  a = User.objects.get(id=request.session['id'])
  b = a.liked_quotes.get(id=number)
  b.delete()
  b.save()
  return redirect('/quotes')

def show(request, number):
  user = User.objects.get(id=number)
  quotes = user.create.all()
  total = len(quotes)
  context = {
    'user' : user,
    'quotes' : quotes,
    'total' : total 
  }
  return render(request, 'first_app/users.html', context)

def add(request, number):
  User.objects.get(id=request.session['id']).liked_quotes.add(Quote.objects.get(id=number))
  return redirect('/quotes')