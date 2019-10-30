from api_fhir.models import DomainResource, Property

class Policy(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    active = Property('active', bool)
