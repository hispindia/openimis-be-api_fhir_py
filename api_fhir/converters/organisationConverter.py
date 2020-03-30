from django.utils.translation import gettext
from api_fhir.configurations import GeneralConfiguration, Stu3IdentifierConfig, Stu3LocationConfig
from api_fhir.converters import BaseFHIRConverter
from api_fhir.models import Location, ContactPointSystem, ContactPointUse, Extension
from api_fhir.utils import TimeUtils, DbManagerUtils
from location.models import Location as Organisation

class OrganisationConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_organisation):
        fhir_location = Location()
        cls.build_organisation_identifier(fhir_location, imis_organisation)
        cls.build_organisation_extension(fhir_location, imis_organisation)
        fhir_location.name = imis_organisation.name
        return fhir_location

    @classmethod
    def build_organisation_identifier(cls, fhir_location, imis_organisation):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_organisation)
        cls.build_fhir_code_identifier(identifiers, imis_organisation)
        fhir_location.identifier = identifiers
        return fhir_location

    @classmethod
    def build_fhir_code_identifier(cls, identifiers, imis_organisation):
        if imis_organisation is not None:
            identifier = cls.build_fhir_identifier(imis_organisation.code,
                                                   Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                   Stu3IdentifierConfig.get_fhir_facility_id_type())
            identifiers.append(identifier)

    @classmethod
    def build_organisation_extension(cls, fhir_location, imis_organisation):
        extension = Extension()
        extension.url = "Parent"
        valueString = ""
        queryset = Organisation.objects.filter(validity_to__isnull=True).filter(id=imis_organisation.parent_id)
        for organisation in queryset:
            valueString = valueString + organisation.uuid
        extension.valueString = valueString
        fhir_location.extension.append(extension)
