from api_fhir import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Patient', views.InsureeViewSet, basename="Patient")
router.register(r'Location', views.HFViewSet)
router.register(r'PractitionerRole', views.PractitionerRoleViewSet, basename="PractitionerRole")
router.register(r'Practitioner', views.PractitionerViewSet)
router.register(r'Claim', views.ClaimViewSet)
router.register(r'ClaimResponse', views.ClaimResponseViewSet, basename="ClaimResponse")
router.register(r'CommunicationRequest', views.CommunicationRequestViewSet)
router.register(r'EligibilityRequest', views.EligibilityRequestViewSet, basename="EligibilityRequest")
router.register(r'Coverage', views.CoverageRequestQuerySet)
router.register(r'Organisation', views.OrganisationViewSet)

urlpatterns = [
    path('', include(router.urls))
    ]
