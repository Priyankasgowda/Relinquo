from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
import time

LEAVE_TYPE=(
			(1,("Sick leave")),
			(2,("Causal leave")),
			)





class Organisation(models.Model):
	name=models.CharField(max_length=100)
	owner=models.ForeignKey(User,on_delete=models.CASCADE)
	about=models.TextField(default=True)
	logo=models.ImageField(blank=True,null=True)
	founded=models.DateField(default=timezone.now)
	org_size=models.CharField(max_length=10)
	org_id=models.CharField(max_length=4,null=True,blank=True,unique=True)

	def __str__(self):
		return f"{self.name}"


class Team(models.Model):
	name=models.CharField(max_length=100)
	size=models.IntegerField()
	lead=models.ForeignKey(User,on_delete=models.CASCADE)
	about=models.TextField()
	organisation=models.ForeignKey(Organisation,on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return f"{self.name}"

class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	is_owner=models.BooleanField(default=False)
	is_teamleader=models.BooleanField(default=False)
	about=models.TextField(default=True)
	designation=models.CharField(max_length=10)
	reporting_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+',blank=True,null=True)
	team=models.ForeignKey(Team,on_delete=models.CASCADE,blank=True,null=True)
	organisation=models.ForeignKey(Organisation,on_delete=models.CASCADE, null=True)
	

	def __str__(self):
		return f"{self.user}"


class Leave_request(models.Model):
	name=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateField(default=timezone.now)
	duration = models.IntegerField(default=1)
	leave_type = models.IntegerField(choices = LEAVE_TYPE, default=1)
	reason=models.TextField()
	is_approved=models.BooleanField(default=False)
	requested_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
	status=models.BooleanField(default=True)

	def __str__(self):
		return f"{self.name}"


class TMember(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	team=models.ForeignKey(Team,on_delete=models.CASCADE)
	organisation=models.ForeignKey(Organisation,on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user}"