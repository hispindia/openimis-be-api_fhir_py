from api_fhir.models import Element, Property


class Extension(Element):

    url = Property('url', str)
    # policy status
    valuePolicystatus = Property('valuePolicystatus', str)
    # insuree policy id
    valueInsureePolicyID = Property('valueInsureePolicyID', str)
    # policy id
    valuePolicyID = Property('valuePolicyID', str)
    # Enrollment date
    valueEnrollmentDate = Property('valueEnrollmentDate', str)
    # start date
    valueStartDate = Property('valueStartDate', str)
    # effective date
    valueEffectiveDate = Property('valueEffectiveDate', str)
    # Expiry date
    valueExpiryDate = Property('valueExpiryDate', str)
    # education
    valueEducation = Property('valueEducation', str)
    # profession
    valueProfession = Property('valueProfession', str)
    valueAddress = Property('valueAddress', 'Address')
    valueAge = Property('valueAge', 'Age')
    valueAnnotation = Property('valueAnnotation', 'Annotation')
    valueAttachment = Property('valueAttachment', 'Attachment')
    valueBase64Binary = Property('valueBase64Binary', str)
    valueBoolean = Property('valueBoolean', bool)
    valueCode = Property('valueCode', str)
    valueCodeableConcept = Property('valueCodeableConcept', 'CodeableConcept')
    valueCoding = Property('valueCoding', 'Coding')
    valueContactPoint = Property('valueContactPoint', 'ContactPoint')
    valueCount = Property('valueCount', 'Count')
    valueDate = Property('valueDate', 'FHIRDate')
    valueDateTime = Property('valueDateTime', 'FHIRDate')
    valueDecimal = Property('valueDecimal', float)
    valueDistance = Property('valueDistance', 'Distance')
    valueDuration = Property('valueDuration', 'Duration')
    valueHumanName = Property('valueHumanName', 'HumanName')
    valueId = Property('valueId', str)
    valueIdentifier = Property('valueIdentifier', 'Identifier')
    valueInstant = Property('valueInstant', 'FHIRDate')
    valueInteger = Property('valueInteger', int)
    valueMarkdown = Property('valueMarkdown', str)
    valueMeta = Property('valueMeta', 'Meta')
    valueMoney = Property('valueMoney', 'Money')
    valueOid = Property('valueOid', str)
    valuePeriod = Property('valuePeriod', 'Period')
    valuePositiveInt = Property('valuePositiveInt', int)
    valueQuantity = Property('valueQuantity', 'Quantity')
    valueRange = Property('valueRange', 'Range')
    valueRatio = Property('valueRatio', 'Ratio')
    valueReference = Property('valueReference', 'Reference')
    valueSampledData = Property('valueSampledData', 'SampledData')
    valueSignature = Property('valueSignature', 'Signature')
    valueString = Property('valueString', str)
    valueTime = Property('valueTime', 'FHIRDate')
    valueTiming = Property('valueTiming', 'Timing')
    valueUnsignedInt = Property('valueUnsignedInt', int)
    valueUri = Property('valueUri', str)
