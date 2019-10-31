from django.utils.translation import gettext
from claim.models import ClaimItem
from api_fhir.converters import BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin
from api_fhir.models import Extension
from api_fhir.models.claim import ClaimItem
from django.db import connection

class ClaimItemConverter(BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_insuree):
        fhir_patient = ClaimItem()
        cls.build_fhir_pk(fhir_patient, imis_insuree.id)
        # extension
        cls.build_fhir_extensions(fhir_patient, imis_insuree)
        return fhir_patient

    @classmethod
    def build_fhir_extensions(cls, imis_insuree, fhir_patient):
        imis_insuree.extension = []

        # function
        def buildall(component,urlvalue):
             def build_extension_component(imis_insuree, fhir_patient):
                  variable = component
                  extension = Extension()
                  extension.url = "http://hispindia.org/fhir/StructureDefinition/ClaimItem/"+urlvalue
                  extension.valueString = variable
                  imis_insuree.extension.append(extension)
             build_extension_component(imis_insuree, fhir_patient)

        buildall(fhir_patient.availability,"availability")
        buildall(fhir_patient.claim_id,"claim_id")
        buildall(fhir_patient.item_id,"iitem_idd")
        buildall(fhir_patient.legacy_id,"legacy_id")
        buildall(fhir_patient.limitation,"limitation")
        buildall(fhir_patient.limitation_value,"ilimitation_valued")
        buildall(fhir_patient.policy_id,"policy_id")
        buildall(fhir_patient.price_adjusted,"price_adjusted")
        buildall(fhir_patient.price_approved,"price_approved")
        buildall(fhir_patient.price_asked,"price_asked")
        buildall(fhir_patient.price_origin,"price_origin")
        buildall(fhir_patient.price_valuated,"price_valuated")
        buildall(fhir_patient.product_id,"product_id")
        buildall(fhir_patient.qty_approved,"qty_approved")
        buildall(fhir_patient.qty_provided,"qty_provided")
        buildall(fhir_patient.rejection_reason,"rejection_reason")
        buildall(fhir_patient.remunerated_amount,"remunerated_amount")
        buildall(fhir_patient.status,"status")
