import copy

from claim.models import ClaimService

from api_fhir.converters import ClaimServiceConverter
from api_fhir.exceptions import FHIRException
from api_fhir.serializers import BaseFHIRSerializer


class ClaimServiceSerializer(BaseFHIRSerializer):
    fhirConverter = ClaimServiceConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return ClaimService.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance