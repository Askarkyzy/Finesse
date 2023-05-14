from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('admin/', admin.site.urls),
   path('man/', views.man, name='man'),
   path('woman/', views.woman, name='woman'),
   path('', views.main, name='main'),
   path('loginpage/', views.loginpage, name='loginpage'),
   path('register/', views.register, name='register'),
   path('detail/<int:id>', views.detail, name='detail'),
   path('cabinet/', views.cabinet, name='cabinet'),
   path('edit_profile/', views.EditProfile.as_view(), name='edit_profile'),
   path('logout/', views.Logout, name='logout'),
   path('check_users', views.CheckUsers.as_view(), name='check_users'),

]

