from claim.models import Claim, Feedback, ClaimItem, ClaimService
from medical.models import Item, Service

from api_fhir.configurations import Stu3IdentifierConfig, Stu3ClaimConfig
from api_fhir.converters import ClaimResponseConverter, CommunicationRequestConverter
from api_fhir.models import ClaimResponse, ClaimResponsePayment, Money, ClaimResponseError, ClaimResponseItem, \
    ClaimResponseItemAdjudication, ClaimResponseProcessNote
from api_fhir.tests import GenericTestMixin
from api_fhir.utils import TimeUtils


class ClaimResponseTestMixin(GenericTestMixin):

    _TEST_CODE = 'code'
    _TEST_STATUS = '1'
    _TEST_ADJUSTMENT = "adjustment"
    _TEST_DATE_PROCESSED = "2010-11-16T00:00:00"
    _TEST_APPROVED = 214.25
    _TEST_REJECTION_REASON = '1'
    _TEST_FEEDBACK_ID = 1
    _TEST_ITEM_CODE = "iCode"
    _TEST_ITEM_STATUS = 1
    _TEST_ITEM_QUANTITY_APPROVED = 4
    _TEST_ITEM_JUSTIFICATION = "item justification"
    _TEST_ITEM_REJECTED_REASON = 1
    _TEST_ITEM_LIMITATION_VALUE = 2
    _TEST_SERVICE_CODE = "sCode"
    _TEST_SERVICE_STATUS = 2
    _TEST_SERVICE_QUANTITY_APPROVED = 3
    _TEST_SERVICE_JUSTIFICATION = "service justification"
    _TEST_SERVICE_REJECTED_REASON = 3
    _TEST_SERVICE_LIMITATION_VALUE = 4
    _TEST_ID = 1

    def setUp(self):
        self._TEST_ITEM = self.create_test_claim_item()
        self._TEST_SERVICE = self.create_test_claim_service()

    def create_test_claim_item(self):
        item = ClaimItem()
        item.item = Item()
        item.item.code = self._TEST_ITEM_CODE
        item.status = self._TEST_ITEM_STATUS
        item.qty_approved = self._TEST_ITEM_QUANTITY_APPROVED
        item.justification = self._TEST_ITEM_JUSTIFICATION
        item.rejection_reason = self._TEST_ITEM_REJECTED_REASON
        item.limitation_value = self._TEST_ITEM_LIMITATION_VALUE
        return item

    def create_test_claim_service(self):
        service = ClaimService()
        service.service = Service()
        service.service.code = self._TEST_SERVICE_CODE
        service.status = self._TEST_SERVICE_STATUS
        service.qty_approved = self._TEST_SERVICE_QUANTITY_APPROVED
        service.justification = self._TEST_SERVICE_JUSTIFICATION
        service.rejection_reason = self._TEST_SERVICE_REJECTED_REASON
        service.limitation_value = self._TEST_SERVICE_LIMITATION_VALUE
        return service

    def create_test_imis_instance(self):
        imis_claim = Claim()
        imis_claim.id = self._TEST_ID
        imis_claim.code = self._TEST_CODE
        imis_claim.status = self._TEST_STATUS
        imis_claim.adjustment = self._TEST_ADJUSTMENT
        imis_claim.date_processed = TimeUtils.str_to_date(self._TEST_DATE_PROCESSED)
        imis_claim.approved = self._TEST_APPROVED
        imis_claim.rejection_reason = self._TEST_REJECTION_REASON
        feedback = Feedback()
        feedback.id = self._TEST_FEEDBACK_ID
        imis_claim.feedback = feedback
        return imis_claim

    def create_test_fhir_instance(self):
        fhir_claim_response = ClaimResponse()
        fhir_claim_response.id = self._TEST_CODE
        pk_id = ClaimResponseConverter.build_fhir_identifier(self._TEST_ID,
                                                          Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                          Stu3IdentifierConfig.get_fhir_id_type_code())
        claim_code = ClaimResponseConverter.build_fhir_identifier(self._TEST_CODE,
                                                          Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                          Stu3IdentifierConfig.get_fhir_claim_code_type())
        fhir_claim_response.identifier = [pk_id, claim_code]
        display = Stu3ClaimConfig.get_fhir_claim_status_rejected_code()
        fhir_claim_response.outcome = ClaimResponseConverter.build_codeable_concept(self._TEST_STATUS, system=None,
                                                                                    text=display)
        fhir_payment = ClaimResponsePayment()
        fhir_payment.adjustmentReason = ClaimResponseConverter.build_simple_codeable_concept(self._TEST_ADJUSTMENT)
        fhir_payment.date = self._TEST_DATE_PROCESSED
        fhir_claim_response.payment = fhir_payment
        total_approved = Money()
        total_approved.value = self._TEST_APPROVED
        fhir_claim_response.totalBenefit = total_approved
        fhir_error = ClaimResponseError()
        fhir_error.code = ClaimResponseConverter.build_codeable_concept(self._TEST_REJECTION_REASON)
        fhir_claim_response.error = [fhir_error]
        feedback = Feedback()
        feedback.id = self._TEST_FEEDBACK_ID
        fhir_claim_response.communicationRequest = \
            [CommunicationRequestConverter.build_fhir_resource_reference(feedback)]
        self.build_response_item(fhir_claim_response)
        self.build_response_service(fhir_claim_response)
        return fhir_claim_response

    def build_response_item(self, fhir_claim_response):
        item = ClaimResponseItem()
        item.sequenceLinkId = 1
        item_general_adjudication = ClaimResponseItemAdjudication()
        item_general_adjudication.category = ClaimResponseConverter.build_simple_codeable_concept(
            Stu3ClaimConfig.get_fhir_claim_item_general_adjudication_code())
        item_limitation = Money()
        item_limitation.value = self._TEST_ITEM_LIMITATION_VALUE
        item_general_adjudication.amount = item_limitation
        item_general_adjudication.reason = ClaimResponseConverter \
            .build_codeable_concept(self._TEST_ITEM_STATUS, Stu3ClaimConfig.get_fhir_claim_item_status_passed_code())
        item_general_adjudication.value = self._TEST_ITEM_QUANTITY_APPROVED
        item.adjudication.append(item_general_adjudication)
        item_rejection_adjudication = ClaimResponseItemAdjudication()
        item_rejection_adjudication.category = ClaimResponseConverter.build_simple_codeable_concept(
            Stu3ClaimConfig.get_fhir_claim_item_rejected_reason_adjudication_code())
        item_rejection_adjudication.reason = ClaimResponseConverter.build_codeable_concept(
            self._TEST_ITEM_REJECTED_REASON)
        item.adjudication.append(item_rejection_adjudication)
        item.noteNumber = [1]
        fhir_claim_response.item.append(item)
        item_note = ClaimResponseProcessNote()
        item_note.number = 1
        item_note.text = self._TEST_ITEM_JUSTIFICATION
        fhir_claim_response.processNote.append(item_note)

    def build_response_service(self, fhir_claim_response):
        service = ClaimResponseItem()
        service.sequenceLinkId = 2
        service_general_adjudication = ClaimResponseItemAdjudication()
        service_general_adjudication.category = ClaimResponseConverter.build_simple_codeable_concept(
            Stu3ClaimConfig.get_fhir_claim_item_general_adjudication_code())
        item_limitation = Money()
        item_limitation.value = self._TEST_SERVICE_LIMITATION_VALUE
        service_general_adjudication.amount = item_limitation
        service_general_adjudication.reason = ClaimResponseConverter \
            .build_codeable_concept(self._TEST_SERVICE_STATUS, Stu3ClaimConfig.get_fhir_claim_item_status_rejected_code())
        service_general_adjudication.value = self._TEST_SERVICE_QUANTITY_APPROVED
        service.adjudication.append(service_general_adjudication)
        item_rejection_adjudication = ClaimResponseItemAdjudication()
        item_rejection_adjudication.category = ClaimResponseConverter.build_simple_codeable_concept(
            Stu3ClaimConfig.get_fhir_claim_item_rejected_reason_adjudication_code())
        item_rejection_adjudication.reason = ClaimResponseConverter.build_codeable_concept(
            self._TEST_SERVICE_REJECTED_REASON)
        service.adjudication.append(item_rejection_adjudication)
        service.noteNumber = [2]
        fhir_claim_response.item.append(service)
        item_note = ClaimResponseProcessNote()
        item_note.number = 2
        item_note.text = self._TEST_SERVICE_JUSTIFICATION
        fhir_claim_response.processNote.append(item_note)

    def verify_fhir_instance(self, fhir_obj):
        self.assertEqual(str(self._TEST_CODE), fhir_obj.id)
        for identifier in fhir_obj.identifier:
            if identifier.type.coding[0].code == Stu3IdentifierConfig.get_fhir_id_type_code():
                self.assertEqual(str(self._TEST_ID), identifier.value)
            elif identifier.type.coding[0].code == Stu3IdentifierConfig.get_fhir_claim_code_type():
                self.assertEqual(self._TEST_CODE, identifier.value)
        self.assertEqual(self._TEST_STATUS, fhir_obj.outcome.coding[0].code)
        self.assertEqual(self._TEST_ADJUSTMENT, fhir_obj.payment.adjustmentReason.text)
        self.assertEqual(self._TEST_DATE_PROCESSED, fhir_obj.payment.date)
        self.assertEqual(self._TEST_APPROVED, fhir_obj.totalBenefit.value)
        self.assertEqual(self._TEST_REJECTION_REASON, fhir_obj.error[0].code.coding[0].code)
        self.assertEqual(str(self._TEST_FEEDBACK_ID), CommunicationRequestConverter.get_resource_id_from_reference(
            fhir_obj.communicationRequest[0]))
        self.assertEqual(str(self._TEST_ITEM_STATUS), fhir_obj.item[0].adjudication[0].reason.coding[0].code)
        self.assertEqual(self._TEST_ITEM_QUANTITY_APPROVED, fhir_obj.item[0].adjudication[0].value)
        self.assertEqual(self._TEST_ITEM_JUSTIFICATION, fhir_obj.processNote[0].text)
        self.assertEqual(str(self._TEST_ITEM_REJECTED_REASON), fhir_obj.item[0].adjudication[1].reason.coding[0].code)
        self.assertEqual(self._TEST_ITEM_LIMITATION_VALUE, fhir_obj.item[0].adjudication[0].amount.value)
        self.assertEqual(str(self._TEST_SERVICE_STATUS), fhir_obj.item[1].adjudication[0].reason.coding[0].code)
        self.assertEqual(self._TEST_SERVICE_QUANTITY_APPROVED, fhir_obj.item[1].adjudication[0].value)
        self.assertEqual(self._TEST_SERVICE_JUSTIFICATION, fhir_obj.processNote[1].text)
        self.assertEqual(str(self._TEST_SERVICE_REJECTED_REASON), fhir_obj.item[1].adjudication[1].reason.coding[0].code)
        self.assertEqual(self._TEST_SERVICE_LIMITATION_VALUE, fhir_obj.item[1].adjudication[0].amount.value)
