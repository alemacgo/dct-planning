# e, not_k, ...
class InstanceFact:
    def __init__(self, name, arity):
        self.name = name
        self.arity = arity

# free_domain, free_range, not_f, ...
class QuantifiedRelationFact(InstanceFact):
    pass

# <, >, =, ...
class PredefinedRelationFact(InstanceFact):
    pass
