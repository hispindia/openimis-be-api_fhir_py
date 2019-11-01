from claim.models import ClaimAdmin, Claim, Feedback, ClaimItem, ClaimService
from insuree.models import Insuree, InsureePolicy
from location.models import HealthFacility

from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api_fhir.paginations import FhirBundleResultsSetPagination
from api_fhir.permissions import FHIRApiPermissions
from api_fhir.configurations import Stu3EligibilityConfiguration as Config
from api_fhir.serializers import PatientSerializer, LocationSerializer, PractitionerRoleSerializer, \
    PractitionerSerializer, ClaimSerializer, EligibilityRequestSerializer, \
    ClaimResponseSerializer, CommunicationRequestSerializer, PolicySerializer, \
    ClaimDataSerializer, ClaimItemSerializer, ClaimServiceSerializer

datevar = '2019-01-01'

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class BaseFHIRView(APIView):
    pagination_class = FhirBundleResultsSetPagination
    permission_classes = (FHIRApiPermissions,)
    authentication_classes = [CsrfExemptSessionAuthentication] + APIView.settings.DEFAULT_AUTHENTICATION_CLASSES


class InsureeViewSet(BaseFHIRView, viewsets.ModelViewSet):
    insureeid = Claim.objects.all().filter(date_claimed__gte=datevar).values('insuree')
    queryset = Insuree.objects.all().filter(validity_to__exact=None).filter(id__in=insureeid)
    serializer_class = PatientSerializer


class HFViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = HealthFacility.objects.all()
    serializer_class = LocationSerializer


class PractitionerRoleViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerRoleSerializer

    def perform_destroy(self, instance):
        instance.health_facility_id = None
        instance.save()


class PractitionerViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerSerializer


class ClaimViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin, GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    lookup_field = 'code'


class ClaimResponseViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimResponseSerializer
    lookup_field = 'code'


class CommunicationRequestViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = CommunicationRequestSerializer


class EligibilityRequestViewSet(BaseFHIRView, mixins.CreateModelMixin, GenericViewSet):
    queryset = Insuree.objects.none()
    serializer_class = eval(Config.get_serializer())

# policy
class PolicyViewSet(BaseFHIRView, viewsets.ModelViewSet):
    insureeid = Claim.objects.all().filter(date_claimed__gte=datevar).values('insuree')
    queryset = InsureePolicy.objects.all().filter(validity_to__exact=None).filter(id__in=insureeid)
    serializer_class = PolicySerializer

# claim data
class ClaimDataViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = Claim.objects.all().filter(validity_to__exact=None).filter(date_claimed__gte=datevar)
    serializer_class = ClaimDataSerializer

# claim items
class ClaimItemViewSet(BaseFHIRView, viewsets.ModelViewSet):
    claimid = Claim.objects.all().filter(date_claimed__gte=datevar).values('insuree')
    queryset = ClaimItem.objects.all().filter(validity_to__exact=None).filter(claim__in=claimid)
    serializer_class = ClaimItemSerializer

# claim services
class ClaimServiceViewSet(BaseFHIRView, viewsets.ModelViewSet):
    claimid = Claim.objects.all().filter(date_claimed__gte=datevar).values('insuree')
    queryset = ClaimService.objects.all().filter(validity_to__exact=None).filter(claim__in=claimid)
    serializer_class = ClaimServiceSerializer
