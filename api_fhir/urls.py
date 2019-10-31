from api_fhir import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Patient', views.InsureeViewSet)
router.register(r'Location', views.HFViewSet)
router.register(r'PractitionerRole', views.PractitionerRoleViewSet)
router.register(r'Practitioner', views.PractitionerViewSet)
router.register(r'Claim', views.ClaimViewSet)
router.register(r'ClaimResponse', views.ClaimResponseViewSet)
router.register(r'CommunicationRequest', views.CommunicationRequestViewSet)
router.register(r'EligibilityRequest', views.EligibilityRequestViewSet, base_name='EligibilityRequest')
# policy
router.register(r'InsureePolicy', views.PolicyViewSet)
# claim data
router.register(r'ClaimData', views.ClaimDataViewSet)
# claim items
router.register(r'ClaimItems', views.ClaimItemViewSet)
# claim services
router.register(r'ClaimServices', views.ClaimServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
