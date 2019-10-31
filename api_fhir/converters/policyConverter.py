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

        def getPolicyStageFromID(ID):
            with connection.cursor() as cursor:
                 cursor.execute("""SELECT tblPolicy.PolicyStage 
                                    FROM tblInsureePolicy 
                                    FULL OUTER JOIN tblPolicy on tblInsureePolicy.PolicyId = tblPolicy.PolicyID  
                                    WHERE tblInsureePolicy.InsureePolicyId = """+str(ID))
                 row = cursor.fetchone()
            return row

        def getPolicyProductFromID(ID):
            with connection.cursor() as cursor:
                 cursor.execute("""SELECT tblProduct.ProductCode 
                                    FROM tblInsureePolicy 
                                    FULL OUTER JOIN tblPolicy on tblInsureePolicy.PolicyId = tblPolicy.PolicyID 
                                    FULL OUTER JOIN tblProduct on tblPolicy.ProdID = tblProduct.ProdID                 
                                    WHERE tblInsureePolicy.InsureePolicyId = """+str(ID))
                 row = cursor.fetchone()
            return row
        
        # policy status
        def build_extension_PolicyStatus(imis_insuree, fhir_patient): 
             PolicyStatus = getPolicyStatusFromID(fhir_patient.id)
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyStatus"
             extension.valueString = PolicyStatus[0]
             imis_insuree.extension.append(extension)

         # policy stage
        def build_extension_PolicyStage(imis_insuree, fhir_patient): 
             PolicyStage = getPolicyStageFromID(fhir_patient.id)
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyStage/" 
             extension.valueString = PolicyStage[0]
             imis_insuree.extension.append(extension)

          # policy product
        def build_extension_PolicyProduct(imis_insuree, fhir_patient): 
             PolicyProduct = getPolicyProductFromID(fhir_patient.id)
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyProduct/" 
             extension.valueString = PolicyProduct[0]
             imis_insuree.extension.append(extension)
             
        # policy insuree policy id
        def build_extension_InsureePolicyID(imis_insuree, fhir_patient):
             InsureePolicyID = fhir_patient.insuree_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyInsureeID"
             extension.valueString = InsureePolicyID
             imis_insuree.extension.append(extension)

        # policy id
        def build_extension_PolicyID(imis_insuree, fhir_patient): 
             PolicyID = fhir_patient.policy_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientPolicyID"
             extension.valueString = PolicyID
             imis_insuree.extension.append(extension)

        # Enrollment date
        def build_extension_EnrollmentDate(imis_insuree, fhir_patient): 
             EnrollmentDate = fhir_patient.enrollment_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientEnrollmentDate"
             extension.valueString = EnrollmentDate
             imis_insuree.extension.append(extension)

        # start date
        def build_extension_StartDate(imis_insuree, fhir_patient): 
             StartDate = fhir_patient.start_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientStartDate" 
             extension.valueStartDate = StartDate
             imis_insuree.extension.append(extension)

        # effective date
        def build_extension_EffectiveDate(imis_insuree, fhir_patient): 
             EffectiveDate = fhir_patient.effective_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientEffectiveDate" 
             extension.valueString = EffectiveDate
             imis_insuree.extension.append(extension)

        # Expiry date
        def build_extension_ExpiryDate(imis_insuree, fhir_patient): 
             ExpiryDate = fhir_patient.expiry_date
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/PatientExpiryDate"
             extension.valueString = ExpiryDate
             imis_insuree.extension.append(extension)
            
        build_extension_PolicyStatus(imis_insuree, fhir_patient)
        build_extension_PolicyStage(imis_insuree, fhir_patient)
        build_extension_PolicyProduct(imis_insuree, fhir_patient)
        build_extension_InsureePolicyID(imis_insuree, fhir_patient)
        build_extension_PolicyID(imis_insuree, fhir_patient)
        build_extension_EnrollmentDate(imis_insuree, fhir_patient)
        build_extension_StartDate(imis_insuree, fhir_patient)
        build_extension_EffectiveDate(imis_insuree, fhir_patient)
        build_extension_ExpiryDate(imis_insuree, fhir_patient)
