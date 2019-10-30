import copy

from insuree.models import InsureePolicy

from api_fhir.converters import PolicyConverter
from api_fhir.exceptions import FHIRException
from api_fhir.serializers import BaseFHIRSerializer


class PolicySerializer(BaseFHIRSerializer):
    fhirConverter = PolicyConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return InsureePolicy.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance
