from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from api.models import *
from api.serializers import *
from django.shortcuts import redirect
import hashlib
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

def _createHash(key):
	hash=hashlib.md5(key)
	return hash.hexdigest()[:4]

class OrganisationViewSet(viewsets.ModelViewSet):
	queryset=Organisation.objects.all()
	serializer_class=OrganisationSerializer
	permission_classes=(IsAuthenticated,)

	def create(self,request):
		name=request.data['name']
		about=request.data['about']
		founded=request.data['founded']
		org_size=request.data['org_size']
		
		key = str(name)+str(request.user.username)
		print(key)
		hashed = _createHash(key.encode('utf-8'))
		print(hashed)

		organisation=Organisation.objects.create(name=name,
			owner=request.user,
			about=about,
			founded=founded,
			org_size=org_size,
			org_id=hashed)
		organisation.save()
		request.user.profile.organisation = organisation
		request.user.profile.save()

		org = OrganisationSerializer(organisation)
		return Response(org.data)

	def list(self,request):
		queryset = request.user.profile.organisation
		print(queryset)
		if queryset is not None:
			serializer = OrganisationSerializer(queryset)
			return Response(serializer.data)
		else:
			return Response({"error": "You're not part of any organisation."})

	def update(self,request,pk):
		name=request.data['name']
		owner=int(request.data['owner'])
		about=request.data['about']
		founded=request.data['founded']
		org_size=request.data['org_size']

		org = Organisation.objects.get(pk = pk)
		org.name = name

		org.about=about
		org.founded=founded
		org.org_size=org_size
		org.save()



		return Response("Done")






class TeamViewSet(viewsets.ViewSet):
	queryset=Team.objects.all()
	serializer_class=TeamSerializer
	permission_classes=(IsAuthenticated,)

	def create(self,request):
		print(request.data)
		name=request.data['name']
		size=request.data['size']
		about=request.data['about']

		lead = int(request.data["lead"])
		lead = User.objects.get(pk=lead)
		team_info=Team.objects.create(
			name=name,
			size=size,
			lead=lead,
			about=about,
			organisation=lead.profile.organisation)
		team_info.save()
		lead.profile.is_teamleader = True
		lead.profile.save()

		
		return Response("Done")

	def list(self,request):
		print(request.user.profile.organisation)
		profiles = Profile.objects.filter(organisation=request.user.profile.organisation)
		leads = [profile.user for profile in profiles]
		teams=Team.objects.filter(organisation=request.user.profile.organisation)
		leadsSerialized = UserSerializer(leads, many=True)
		teamsSerialized = TeamSerializer(teams, many=True)

		serializer = {"teams" : teamsSerialized.data,
					  "leads" : leadsSerialized.data}
		return Response(serializer)

	def update(self,request,pk):
		name=request.data['name']
		size=request.data['size']
		about=request.data['about']


		team = Team.objects.get(pk = pk)
		team.name = name

		team.size=size
		team.about=about
		
		team.save()



		return Response("Done")
	

	
class LeaveViewSet(viewsets.ModelViewSet):
	queryset=Leave_request.objects.all()
	serializer_class=Leave_requestSerializer
	permission_classes=(IsAuthenticated,)

	def create(self,request):

		date=request.data['date']
		reason=request.data['reason']
		duration=request.data['duration']
		
		
		leave_info=Leave_request.objects.create(name=request.user,
		date=date,
		reason=reason,
		duration=duration,
		requested_to=request.user.profile.reporting_to)

		leave_info.save()
		
		return Response("Done")		
		
	def list(self,request):
		queryset = Leave_request.objects.filter(requested_to=request.user, status=True)
		serializer = Leave_requestSerializer(queryset, many=True)
		return Response(serializer.data)

	def update(self,request,pk):
		
		date=request.data['date']
		reason=request.data['reason']
		duration=request.data['duration']
		leave_type=request.data['leave_type']

		leave=Leave_request.objects.get(pk=pk)
		leave.date=date
		leave.reason=reason
		leave.duration=duration
		leave.leave_type=leave_type
		leave.save()
		return Response("Updated successfully")
	
	def partial_update(self, request, pk=None):
		state = request.data["state"]
		leave=Leave_request.objects.get(pk = pk)
		print(leave.name.email)
		email = leave.name.email
		msg = "Ërror"
		if state == "Accept":
			leave.is_approved = True
			leave.status = False
			msg = "Request has been Accepted."
		elif state == "Reject":
			leave.is_approved = False
			leave.status = False
			msg = "Request has been Rejected."
		
		leave.save()
		self.sendmail(email, msg)
		return Response(msg)

	def sendmail(self, email, msg):
		msg= EmailMessage("Leave Status", f"Your Leave {msg}. Please login to see status.", to=[email])
		msg.send()







class ProfileViewSet(viewsets.ModelViewSet):
	queryset=Profile.objects.all()
	serializer_class=ProfileSerializer
	permission_classes=(IsAuthenticated,)

	def create(self,request):
		user=int(request.data['user'])		
	
		team=int(request.data['team'])
	
		organisation=int(request.data['organisation'])
		
		
		about=request.data['about']
		designation=request.data['designation']
		reporting_to=int(request.data['reporting_to'])


		profile_info=Profile.objects.create(user=request.user,
			team=Team.objects.get(id=team),organisation=Organisation.objects.get(id=organisation),about=about,designation=designation,reporting_to=User.objects.get(id=reporting_to),
			)
		profile_info.save()

		return Response("done")

	def list(self,request):
		organisation = request.user.profile.organisation
		profiles=Profile.objects.filter(is_teamleader=False,is_owner=False, organisation=organisation)
		employees=[profile.user for profile in profiles]
		serializer = ProfileSerializer(profiles, many=True)
		return Response(serializer.data)

	# def update(self,request,pk):
	# 	about=request.data['request']
	# 	designation=request.data['designation']




class SignupViewSet(viewsets.ModelViewSet):
	queryset=User.objects.all()
	serializer_class=UserSerializer
	permission_classes=(AllowAny,)

	def create(self,request):
		firstname=request.data['first_name']
		lastname=request.data['last_name']
		email=request.data['email']
		username=request.data['username']
		password=request.data['password']
		org_id=request.data['org_id']
		user_exists=User.objects.filter(username=username)
		try:
			org = Organisation.objects.get(org_id=org_id)
		except:
			return Response({'error':'Invalid Organisation ID'})
		if not user_exists:
			user=User.objects.create_user(
				first_name=firstname,
				last_name=lastname,email=email,
				username=username,
				password=password)
			profile = Profile.objects.create(user=user, organisation=org, reporting_to=org.owner)
			return Response({'success':'User has successfully signed up.'})
		else:
			return Response({'error':'User already exists. Please enter a new user'})


class TMemberViewSet(viewsets.ModelViewSet):
	serializer_class = TMemberSerializer
	permission_classes = [AllowAny,]

	def get_queryset(self):
		queryset = TMember.objects.filter(user=self.request.user)
		return queryset

	def list(self, request):
		team = Team.objects.get(pk=request.GET.get('team'))
		tmember = TMember.objects.filter(team=team)
		tserialized = TMemberSerializer(tmember, many=True)
		return Response(tserialized.data)

	def create(self, request):
		user = User.objects.get(pk=request.data['user'])
		team = Team.objects.get(pk=request.data['team'])
		tmember = TMember.objects.create(user=user, team=team, organisation=team.organisation)
		user.profile.reporting_to = team.lead
		user.profile.save()

		tserialized = TMemberSerializer(tmember)
		return Response(tserialized.data)

