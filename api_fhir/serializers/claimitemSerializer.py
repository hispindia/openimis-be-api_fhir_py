import copy

from claim.models import ClaimItem

from api_fhir.converters import ClaimItemConverter
from api_fhir.exceptions import FHIRException
from api_fhir.serializers import BaseFHIRSerializer


class ClaimItemSerializer(BaseFHIRSerializer):
    fhirConverter = ClaimItemConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return ClaimItem.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance