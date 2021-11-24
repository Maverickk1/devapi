from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from restapiapp.models import Student
from .serializers import *
from rest_framework import serializers


from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import create_student, get_students, get_student_object,update_student
from rest_framework import generics

from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



class StudentList(APIView):
    class StudentSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=50)
        father_name = serializers.CharField(max_length=50)
        standard = serializers.IntegerField()


    def get(self, request):
        students = Student.objects.filter(name='student8')
        serializer = self.StudentSerializer(students,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = create_student(**serializer.validated_data)
        serializer = self.StudentSerializer(student)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentDetail(APIView):
    class StudentSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=50)
        father_name = serializers.CharField(max_length=50)
        standard = serializers.IntegerField()


    def get(self, request, pk):
        student_obj = get_student_object(pk=pk)
        serializer = self.StudentSerializer(student_obj)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, id=pk)
        serializer = self.StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['name']= serializer.validated_data.pop('name')
        serializer.validated_data['father_name'] = serializer.validated_data.pop('father_name')
        serializer.validated_data['standard'] = serializer.validated_data.pop('standard')
        student = update_student(student=student, **serializer.validated_data)

        print("request.data = ", request.data)
        return Response(serializer.data)


    def delete(self, request, pk):
        student_obj = get_student_object(pk=pk)
        student_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'account is created for '+ user)
            return redirect('login')

    context={"form": form}
    return render(request, 'restapiapp/register.html',  context)

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect!')

    context={}
    return render(request,'restapiapp/login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

