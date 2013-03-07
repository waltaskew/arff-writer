"""Functions for generating ARFF files."""


import datetime
import numbers


RELATION_LINE = '@RELATION %s'
DATA_LINE = '@DATA'
ATTRIBUTE_LINE = '@ATTRIBUTE %s %s'


class FeatureFunction(object):
    """Thin wrapper around a function which generates features
    for an ARFF file.
    """
    TO_STRING = {
        'numeric': lambda x: str(float(x)),
        'integer': lambda x: str(float(int(x))),
        'real': lambda x: str(float(x)),
        'nominal': lambda x: '"%s"' % x.replace('"', r'\"'),
        'string': lambda x: '"%s"' % x.replace('"', r'\"'),
        'date': lambda x: '"%s"' % x.strftime('%Y-%m-%d %H:%M:%S')
    }

    def __init__(self, func, attribute_name=None,
            attribute_type=None, nominals=None):
        if attribute_name is None:
            attribute_name = func.__name__

        if attribute_type is not None and attribute_type not in self.TO_STRING:
            raise ValueError('Unkonw attribute type %s given' % attribute_type)
        elif attribute_type == 'nominal' and nominals is None:
            raise ValueError(
                'Feature %s is of type nominal but declares no nominals set' %
                attribute_name)

        self.func = func
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        self.nominals = nominals

        if attribute_type is not None:
            self.result_to_string = self.TO_STRING[attribute_type]
        else:
            self.result_to_string = None

    def attribute_string(self):
        """Return an attribute string for this feature."""
        if self.attribute_type == 'nominal':
            data_type = '{%s}' % ','.join(nominal.replace('"', r'\"') for
                    nominal in self.nominals)
        else:
            data_type = self.attribute_type

        return ATTRIBUTE_LINE % (self.attribute_name, data_type)

    def deduce_to_string_func(self, val):
        """Deduce the proper to_string function from the type of val."""
        if isinstance(val, basestring):
            self.result_to_string = self.TO_STRING['string']
            self.attribute_type = 'string'
        elif isinstance(val, numbers.Number):
            self.result_to_string = self.TO_STRING['numeric']
            self.attribute_type = 'numeric'
        elif isinstance(val, (datetime.date, datetime.datetime)):
            self.result_to_string = self.TO_STRING['date']
            self.attribute_type = 'date'
        else:
            raise ValueError("Unable to deduce ARFF type of %s" % val)

    def __call__(self, *args, **kwargs):
        """Return the result of the wrapped function as a string
        suitable for an ARFF file.
        """
        result = self.func(*args, **kwargs)
        if self.result_to_string is None:
            self.deduce_to_string_func(result)
        return self.result_to_string(result)


def feature(fname=None, returns=None, nominals=None):
    """Decorator for designating functions as weka feature functions."""

    def feature_maker(func):
        """Adds nescessary weka attributes to a function."""
        if fname is None:
            name = func.__name__

        return FeatureFunction(
                func,
                attribute_name=fname,
                attribute_type=returns,
                nominals=nominals)

    return feature_maker


def find_feature_functions(module):
    """Return an iterator yielding all feature functions
    on the given module.
    """
    funcs = []
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, FeatureFunction):
            funcs.append(attr)
    return funcs


def get_feature_values(feature_funcs, input_vals):
    """Return an iterator yielding the features for each input in the
    list of input vals.
    """
    for input_val in input_vals:
        yield [func(input_val) for func in feature_funcs]


def get_header(feature_funcs, relation_name):
    """Return a string representing the header of an ARFF file."""
    lines = []
    lines.append(RELATION_LINE % relation_name)
    lines.append('\n')
    for func in feature_funcs:
        lines.append(func.attribute_string())
    lines.append('\n')
    lines.append(DATA_LINE + '\n')
    return '\n'.join(lines)


def write_feature_file(out_file_name, relation_name, module, input_vals):
    """Write an arff file."""
    funcs = find_feature_functions(module)

    feature_vals = []
    for features in get_feature_values(funcs, input_vals):
        feature_vals.append(','.join(features))

    with open(out_file_name, 'w') as out_file:
        out_file.write(get_header(funcs, relation_name))
        out_file.write('\n'.join(feature_vals))
        out_file.write('\n')
