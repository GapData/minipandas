from pandas.core import generic


class Series(generic.NDFrame):
    pass


ops.add_special_arithmetic_methods(Series)
