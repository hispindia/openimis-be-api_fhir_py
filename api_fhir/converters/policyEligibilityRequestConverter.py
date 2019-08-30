from policy.services import ByInsureeRequest

from api_fhir.configurations import Stu3EligibilityConfiguration as Config, Stu3IdentifierConfig
from api_fhir.converters import BaseFHIRConverter, PatientConverter
from api_fhir.models import EligibilityResponse as FHIREligibilityResponse, InsuranceBenefitBalance, \
    EligibilityResponseInsurance, InsuranceBenefitBalanceFinancial, Money, Contract, Term, Period, \
    Identifier


class PolicyEligibilityRequestConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, eligibility_response):
        fhir_response = FHIREligibilityResponse()
        for item in eligibility_response.items:
            cls.build_fhir_insurance(fhir_response, item)
        return fhir_response

    @classmethod
    def to_imis_obj(cls, fhir_eligibility_request, audit_user_id):
        chfid = cls.build_imis_chfid(fhir_eligibility_request)
        return ByInsureeRequest(chfid)

    @classmethod
    def build_fhir_insurance(cls, fhir_response, response):
        result = EligibilityResponseInsurance()
        cls.build_fhir_insurance_contract(result,                                        
                                          response.product_code,
                                          response.expiry_date.isoformat(),
                                          response.status)
        cls.build_fhir_money_benefit(result, Config.get_fhir_balance_code(),
                                     response.ceiling1,
                                     response.ded1)
        fhir_response.insurance.append(result)

    @classmethod
    def build_fhir_insurance_contract(cls, insurance, product_code, expiry_date, status):
        identifier = cls.build_fhir_identifier(f'{product_code}/{expiry_date}',
                                               Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                               Stu3IdentifierConfig.get_fhir_id_type_code())

        period = Period()
        period.end = expiry_date
        term = Term()
        term.applies = period
        contract = Contract()        
        contract.identifier = [identifier]
        contract.status = Config.get_fhir_status_map().get(status)
        contract.term = term
        insurance.contract = contract

    @classmethod
    def build_fhir_money_benefit(cls, insurance, code, allowed_value, used_value):
        benefit_balance = cls.build_fhir_generic_benefit_balance(code)
        cls.build_fhir_money_benefit_balance_financial(
            benefit_balance, allowed_value, used_value)
        insurance.benefitBalance.append(benefit_balance)

    @classmethod
    def build_fhir_generic_benefit_balance(cls, code):
        benefit_balance = InsuranceBenefitBalance()
        benefit_balance.category = cls.build_simple_codeable_concept(code)
        return benefit_balance

    @classmethod
    def build_fhir_money_benefit_balance_financial(cls, benefit_balance, allowed_value, used_value):
        financial = cls.build_fhir_generic_benefit_balance_financial()
        allowed_money_value = Money()
        allowed_money_value.value = allowed_value or 0
        financial.allowedMoney = allowed_money_value
        used_money_value = Money()
        used_money_value.value = used_value or 0
        financial.usedMoney = used_money_value
        benefit_balance.financial.append(financial)

    @classmethod
    def build_fhir_generic_benefit_balance_financial(cls):
        financial = InsuranceBenefitBalanceFinancial()
        financial.type = cls.build_simple_codeable_concept(
            Config.get_fhir_financial_code())
        return financial

    @classmethod
    def build_imis_chfid(cls, fhir_eligibility_request):
        chfid = None
        patient_reference = fhir_eligibility_request.patient
        if patient_reference:
            chfid = PatientConverter.get_resource_id_from_reference(
                patient_reference)
        return chfid