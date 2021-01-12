from django.shortcuts import render,redirect
from django.http import HttpResponse



def homepage(request):
	return render(request,"home.html")

def dashboard(request):
	return render(request,"dashboard.html")

def signup(request):
	return render(request,'signup.html')

def signin(request):
	return render(request,'login.html')


def team(request):
	return render(request,'team.html')

def employee(request):
	return render(request,'employee.html')
