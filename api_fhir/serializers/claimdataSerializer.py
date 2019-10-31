import copy

from claim.models import Claim

from api_fhir.converters.claimdataConverter import ClaimDataConverter
from api_fhir.exceptions import FHIRException
from api_fhir.serializers import BaseFHIRSerializer


class ClaimDataSerializer(BaseFHIRSerializer):
    fhirConverter = ClaimDataConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return Claim.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance