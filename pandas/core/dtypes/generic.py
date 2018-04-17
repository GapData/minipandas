# def create_pandas_abc_type(name, attr, comp):
#     @classmethod
#     def _check(cls, inst):
#         return getattr(inst, attr, '_typ') in comp
#
#     dct = dict(__instancecheck__=_check, __subclasscheck__=_check)
#     meta = type("ABCBase", (type, ), dct)
#     return meta(name, tuple(), dct)
#
#
#ABCIndex = []
#create_pandas_abc_type("ABCIndex", "_typ", ("index", ))

class ABCSeries:
    pass