from django.utils.translation import gettext
from claim.models import Claim
from api_fhir.converters import BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin
from api_fhir.models import Extension
from api_fhir.models.claim import Claim
from django.db import connection

class ClaimDataConverter(BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_insuree):
        fhir_patient = Claim()
        cls.build_fhir_pk(fhir_patient, imis_insuree.id)
        # extension
        cls.build_fhir_extensions(fhir_patient, imis_insuree)
        return fhir_patient

    @classmethod
    def build_fhir_extensions(cls, imis_insuree, fhir_patient):
        imis_insuree.extension = []

        # Insuree ID
        def build_extension_InsureeID(imis_insuree, fhir_patient):
             InsureeID = fhir_patient.insuree_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/InsureeID/"
             extension.valueString = InsureeID
             imis_insuree.extension.append(extension)

        # Claim Code
        def build_extension_ClaimCode(imis_insuree, fhir_patient):
             ClaimCode = fhir_patient.code
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/ClaimCode/"
             extension.valueString = ClaimCode
             imis_insuree.extension.append(extension)

        # Date From
        def build_extension_DateFrom(imis_insuree, fhir_patient):
             DateFrom = fhir_patient.date_from
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/DateFrom/"
             extension.valueString = DateFrom
             imis_insuree.extension.append(extension)

        # Date To
        def build_extension_DateTo(imis_insuree, fhir_patient):
             DateTo = fhir_patient.date_to
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/DateTo/"
             extension.valueString = DateTo
             imis_insuree.extension.append(extension)

        # ICD ID
        def build_extension_ICDID(imis_insuree, fhir_patient):
             ICDID = fhir_patient.icd_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/ICDID/"
             extension.valueString = ICDID
             imis_insuree.extension.append(extension)

        # Claim Status
        def build_extension_ClaimStatus(imis_insuree, fhir_patient):
             ClaimStatus = fhir_patient.status
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/ClaimStatus/"
             extension.valueString = ClaimStatus
             imis_insuree.extension.append(extension)

        # Adjustment
        def build_extension_Adjustment(imis_insuree, fhir_patient):
             Adjustment = fhir_patient.adjustment
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/Adjustment/" 
             extension.valueString = Adjustment
             imis_insuree.extension.append(extension)

        # Claimed
        def build_extension_Claimed(imis_insuree, fhir_patient):
             Claimed = fhir_patient.claimed
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/Claimed/" 
             extension.valueString = Claimed
             imis_insuree.extension.append(extension)

        # Approval Status
        def build_extension_ApprovalStatus(imis_insuree, fhir_patient):
             ApprovalStatus = fhir_patient.approval_status
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/ApprovalStatus/" 
             extension.valueString = ApprovalStatus
             imis_insuree.extension.append(extension)
             
        # ClaimAdminID
        def build_extension_ClaimAdminID(imis_insuree, fhir_patient):
             ClaimAdminID = fhir_patient.admin_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/ClaimAdminID/" 
             extension.valueString = ClaimAdminID
             imis_insuree.extension.append(extension)
             
        # Approved
        def build_extension_Approved(imis_insuree, fhir_patient):
             Approved = fhir_patient.approved
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/ClaimApproved/" 
             extension.valueString = Approved
             imis_insuree.extension.append(extension)
             
        # Date Claimed
        def build_extension_DateClaimed(imis_insuree, fhir_patient):
             DateClaimed = fhir_patient.date_claimed
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/DateClaimed/" 
             extension.valueString = DateClaimed
             imis_insuree.extension.append(extension)
          
        # Date Processed
        def build_extension_DateProcessed(imis_insuree, fhir_patient):
             DateProcessed = fhir_patient.date_processed
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/DateProcessed/" 
             extension.valueString = DateProcessed
             imis_insuree.extension.append(extension)
             
        # FeedbackID
        def build_extension_FeedbackID(imis_insuree, fhir_patient):
             FeedbackID = fhir_patient.feedback_id
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/FeedbackID/" 
             extension.valueString = FeedbackID
             imis_insuree.extension.append(extension)
             
        # Feedback Status
        def build_extension_FeedbackStatus(imis_insuree, fhir_patient):
             FeedbackStatus = fhir_patient.feedback_status
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/FeedbackStatus/" 
             extension.valueString = FeedbackStatus
             imis_insuree.extension.append(extension)
             
        # Explanation
        def build_extension_Explanation(imis_insuree, fhir_patient):
             Explanation = fhir_patient.explanation
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/Explanation/" 
             extension.valueString = Explanation
             imis_insuree.extension.append(extension)
             
        # Rejection Reason
        def build_extension_RejectionReason(imis_insuree, fhir_patient):
             RejectionReason = fhir_patient.rejection_reason
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/RejectionReason/" 
             extension.valueString = RejectionReason
             imis_insuree.extension.append(extension)
             
        def getHFCODEFromHFID(ID):
            with connection.cursor() as cursor:
                 cursor.execute("""SELECT tblHF.HFCode 
                                    FROM tblClaim 
                                    FULL OUTER JOIN tblHF on tblClaim.HFID = tblHF.HfID 
                                    WHERE tblClaim.ClaimID = """+str(ID))
                 row = cursor.fetchone()
            return row

        # health_facility_id
        def build_extension_health_facility_id(imis_insuree, fhir_patient):
             health_facility_id = getHFCODEFromHFID(fhir_patient.id)
             extension = Extension()
             extension.url = "http://hispindia.org/fhir/StructureDefinition/health_facility_id/" 
             extension.valueString = health_facility_id[0]
             imis_insuree.extension.append(extension)
             
        def buildall(component,urlvalue):
             def build_extension_component(imis_insuree, fhir_patient):
                  variable = component
                  extension = Extension()
                  extension.url = "http://hispindia.org/fhir/StructureDefinition/Claim/"+urlvalue
                  extension.valueString = variable
                  imis_insuree.extension.append(extension)
             build_extension_component(imis_insuree, fhir_patient)

        build_extension_InsureeID(imis_insuree, fhir_patient)
        build_extension_ClaimCode(imis_insuree, fhir_patient)
        build_extension_DateFrom(imis_insuree, fhir_patient)
        build_extension_DateTo(imis_insuree, fhir_patient)
        build_extension_ICDID(imis_insuree, fhir_patient)
        build_extension_ClaimStatus(imis_insuree, fhir_patient)
        build_extension_Adjustment(imis_insuree, fhir_patient)
        build_extension_Claimed(imis_insuree, fhir_patient)
        build_extension_ApprovalStatus(imis_insuree, fhir_patient)
        build_extension_ClaimAdminID(imis_insuree, fhir_patient)
        build_extension_Approved(imis_insuree, fhir_patient)
        build_extension_DateClaimed(imis_insuree, fhir_patient)
        build_extension_DateProcessed(imis_insuree, fhir_patient)
        build_extension_FeedbackID(imis_insuree, fhir_patient)
        build_extension_FeedbackStatus(imis_insuree, fhir_patient)
        build_extension_Explanation(imis_insuree, fhir_patient)
        build_extension_RejectionReason(imis_insuree, fhir_patient)
        build_extension_health_facility_id(imis_insuree, fhir_patient)

        buildall(fhir_patient.guarantee_id,"icd_1_id")
        buildall(fhir_patient.guarantee_id,"guarantee_id")
        buildall(fhir_patient.health_facility_id,"health_facility_id")
        buildall(fhir_patient.process_stamp,"process_stamp")
        buildall(fhir_patient.reinsured,"reinsured")
        buildall(fhir_patient.remunerated,"remunerated")
        buildall(fhir_patient.review_status,"review_status")
        buildall(fhir_patient.submit_stamp,"submit_stamp")
        buildall(fhir_patient.valuated,"valuated")
        buildall(fhir_patient.visit_type,"visit_type")