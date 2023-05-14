from telnetlib import LOGOUT
from django import views
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect, get_object_or_404
from website.forms import *

from website.models import Clothes, Categories, Filter_Size, Filter_Price, Type
from django.contrib.auth.models import User



def main(request):
   clothes_all = Clothes.objects.all().order_by('size')
   clothes_all2 = Clothes.objects.all().order_by('-size')
   clothes_unique = []
   names_seen = set()
   for cloth in clothes_all:
      if cloth.name not in names_seen:
         clothes_unique.append(cloth)
         names_seen.add(cloth)


   clothes_unique2 = []
   names_seen2 = set()
   for cloth2 in clothes_all2:
      if cloth2.name not in names_seen2:
         clothes_unique2.append(cloth2)
         names_seen2.add(cloth2)

   context = {
      'clothes': clothes_unique,
      'clothes2': clothes_unique2,
   }

   return render(request, 'Main/base.html', context)


def loginpage(request):
   if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
         email = form.cleaned_data['email']
         password = form.cleaned_data['password']

         try:
            user = User.objects.get(email=email, password=password)
            messages.success(request, 'Login successful. Welcome!')
            return redirect('/')  # Replace 'home' with the URL you want to redirect to after successful login
         except User.DoesNotExist:

            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'form': form})
   else:
      form = LoginForm()


   return render(request, 'Main/login.html', {'form': form})



def register(request):
   if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']
         email = form.cleaned_data['email']
         user = User(username=username, password=password, email=email)
         user.save()
         return redirect('/loginpage/')
   else:
      form = RegistrationForm()

   return render(request, 'Main/register.html', {'form': form})





def man(request):
   categories = Categories.objects.all()
   prices = Filter_Price.objects.all()
   sizes = Filter_Size.objects.all()
   type = Type.objects.get(type='Male')
   menswear = Clothes.objects.filter(type=type)

   CATID = request.GET.get('categories')
   PRICEID = request.GET.get('prices')
   SIZEID = request.GET.get('sizes')
   if CATID:
      menswear = Clothes.objects.filter(type=type, categories=CATID)
   elif PRICEID:
      menswear = Clothes.objects.filter(type=type, filter_price=PRICEID)
   elif SIZEID:
      menswear = Clothes.objects.filter(type=type, size=SIZEID)

   men_unique = []
   names_seen = set()
   for cloth in menswear:
      if cloth.name not in names_seen:
         men_unique.append(cloth)
         names_seen.add(cloth.name)
   context = {
      'men_unique':men_unique,
      'categories': categories,
      'prices':prices,
      'sizes':sizes,
   }
   return render(request, 'man.html', context=context)


def woman(request):
   categories = Categories.objects.all()
   prices = Filter_Price.objects.all()
   sizes = Filter_Size.objects.all()
   type = Type.objects.get(type='Female')
   womenswear = Clothes.objects.filter(type=type)

   CATID = request.GET.get('categories')
   PRICEID = request.GET.get('prices')
   SIZEID = request.GET.get('sizes')
   if CATID:
      womenswear = Clothes.objects.filter(type=type, categories=CATID)
   elif PRICEID:
      womenswear = Clothes.objects.filter(type=type, filter_price=PRICEID)
   elif SIZEID:
      womenswear = Clothes.objects.filter(type=type, size=SIZEID)

   women_unique = []
   names_seen = set()
   for cloth in womenswear:
      if cloth.name not in names_seen:
         women_unique.append(cloth)
         names_seen.add(cloth.name)
   context = {
         'women_unique': women_unique,
         'categories': categories,
         'prices': prices,
         'sizes': sizes,
   }
   return render(request, 'woman.html', context)


def detail(request, id):
   get_clothes = Clothes.objects.get(id=id)
   context = {
      'get_clothes': get_clothes,

   }
   return render(request, 'Main/detail.html', context)


def cabinet(request):

   context = {

   }

   return render(request, 'Main/cabinet.html', context)


def Logout(request):
   LOGOUT(request)
   return redirect('/')


class EditProfile(views.View):
   def get(self, request):
      return render(request, 'Main/edit-profile.html')

   def post(self, request, *args, **kwargs):
      username = request.POST['username']
      email = request.POST['email']

      User.objects.filter(id=request.user.id).update(
         username=username,
         email=email
      )

      return redirect('cabinet')


class CheckUsers(views.View):
   def get(self, request):
      if request.user.is_superuser:
         all_users = User.objects.all().exclude(id=request.user.id)

         context = {
               'all_users': all_users
         }

         return render(request, 'Main/check_users.html', context)

         return HttpResponse('', status=404)

   def post(self, request, *args, **kwargs):
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']

      if User.objects.filter(username=username).exists():
         messages.info(request, 'Пользователь уже создан!')
         return redirect('check_users')
      if User.objects.filter(email=email).exists():
         messages.info(request, 'Пользователь с этим адресом электронной почты уже создан!')
         return redirect('check_users')

      user = User.objects.create(username=username, email=email)
      user.set_password(password)
      user.save()

      return redirect('check_users')

