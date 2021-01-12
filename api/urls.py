from django.urls import path,include

from rest_framework.routers import DefaultRouter
from api.viewsets import *


router=DefaultRouter()
router.register(r'profile',ProfileViewSet)
router.register(r'organisation',OrganisationViewSet)
router.register(r'team',TeamViewSet)
router.register(r'leave',LeaveViewSet)
router.register(r'getstarted',SignupViewSet)
router.register(r'teammember', TMemberViewSet, base_name="teammember")



urlpatterns=[
	
	path('',include(router.urls))
]