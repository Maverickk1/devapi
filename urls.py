from django.urls import path
from . import views
from .views import StudentList,StudentDetail

urlpatterns = [
    path('', StudentList.as_view(), name='home'),
    path('<int:pk>/', StudentDetail.as_view()),
    path('register', views.register, name='register'),
    path('login',views.loginpage,name='login'),
    path('logout',views.logoutuser,name='logout')

]
