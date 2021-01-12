from rest_framework import serializers
from api.models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model= User
		fields=('id', 'username', 'first_name','last_name','email')

	

class OrganisationSerializer(serializers.ModelSerializer):
	owner=UserSerializer()
	class Meta:
		model=Organisation
		fields=('id','name','owner','about','logo','founded','org_size', 'org_id')
		depth=1

class TeamSerializer(serializers.ModelSerializer):
	lead=UserSerializer()
	organisation=OrganisationSerializer()
	class Meta:
		model=Team
		fields=('id','name','size','lead','about','organisation')
		depth=1

class ProfileSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	reporting_to=UserSerializer()
	team=TeamSerializer()
	organisation=OrganisationSerializer()

	class Meta:
		model=Profile
		fields=('id','user','is_owner','is_teamleader','about','designation','reporting_to','team','organisation')
		depth=1

class Leave_requestSerializer(serializers.ModelSerializer):
	name=UserSerializer()
	requested_to=UserSerializer()

	class Meta:
		model= Leave_request
		fields=('id', 'name','date','duration','leave_type','reason','requested_to','is_approved','status')
		depth=1

class TMemberSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	team = TeamSerializer()
	organisation = OrganisationSerializer()

	class Meta:
		model = TMember
		fields = ('user', 'team', 'organisation')