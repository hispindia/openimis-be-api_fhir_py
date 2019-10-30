from django.utils.translation import gettext
from insuree.models import InsureePolicy
from api_fhir.converters import BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin
from api_fhir.models import Extension
from api_fhir.models.policy import Policy
from django.db import connection

class PolicyConverter(BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_insuree):
        fhir_patient = Policy()
        cls.build_fhir_pk(fhir_patient, imis_insuree.id)
        # extension
        cls.build_fhir_extensions(fhir_patient, imis_insuree)
        return fhir_patient

    @classmethod
    def build_fhir_extensions(cls, imis_insuree, fhir_patient):
        imis_insuree.extension = []
        def getPolicyStatusFromID(ID):
            with connection.cursor() as cursor:
                 cursor.execute("""SELECT tblPolicy.PolicyStatus 
                                    FROM tblInsureePolicy 
                                    FULL OUTER JOIN tblPolicy on tblInsureePolicy.PolicyId = tblPolicy.PolicyID  
                                    WHERE tblInsureePolicy.InsureePolicyId = """+str(ID))
                 row = cursor.fetchone()
            return row

        # policy status
        def build_extension_PolicyStatus(imis_insuree, fhir_patient): 
             PolicyStatus = getPolicyStatusFromID(fhir_patient.id)
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyStatus/" + str(PolicyStatus[0])
             extension.valuePolicystatus = PolicyStatus[0]
             imis_insuree.extension.append(extension)

        # policy insuree policy id
        def build_extension_InsureePolicyID(imis_insuree, fhir_patient):
             InsureePolicyID = fhir_patient.insuree_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyInsureeID/"+str(InsureePolicyID)
             extension.valueInsureePolicyID = InsureePolicyID
             imis_insuree.extension.append(extension)

        # policy id
        def build_extension_PolicyID(imis_insuree, fhir_patient): 
             PolicyID = fhir_patient.policy_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyID/" +str(PolicyID)
             extension.valuePolicyID = PolicyID
             imis_insuree.extension.append(extension)

        # Enrollment date
        def build_extension_EnrollmentDate(imis_insuree, fhir_patient): 
             EnrollmentDate = fhir_patient.enrollment_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientEnrollmentDate/" +str(EnrollmentDate)
             extension.valueEnrollmentDate = EnrollmentDate
             imis_insuree.extension.append(extension)

        # start date
        def build_extension_StartDate(imis_insuree, fhir_patient): 
             StartDate = fhir_patient.start_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientStartDate/" +str(StartDate)
             extension.valueStartDate = StartDate
             imis_insuree.extension.append(extension)

        # effective date
        def build_extension_EffectiveDate(imis_insuree, fhir_patient): 
             EffectiveDate = fhir_patient.effective_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientEffectiveDate/" +str(EffectiveDate)
             extension.valueEffectiveDate = EffectiveDate
             imis_insuree.extension.append(extension)

        # Expiry date
        def build_extension_ExpiryDate(imis_insuree, fhir_patient): 
             ExpiryDate = fhir_patient.expiry_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientExpiryDate/" +str(ExpiryDate)
             extension.valueExpiryDate = ExpiryDate
             imis_insuree.extension.append(extension)
            
        build_extension_PolicyStatus(imis_insuree, fhir_patient)
        build_extension_InsureePolicyID(imis_insuree, fhir_patient)
        build_extension_PolicyID(imis_insuree, fhir_patient)
        build_extension_EnrollmentDate(imis_insuree, fhir_patient)
        build_extension_StartDate(imis_insuree, fhir_patient)
        build_extension_EffectiveDate(imis_insuree, fhir_patient)
        build_extension_ExpiryDate(imis_insuree, fhir_patient)