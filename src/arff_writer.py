"""Functions for generating ARFF files."""


import datetime
import numbers


RELATION_LINE = '@RELATION %s'
DATA_LINE = '@DATA'
ATTRIBUTE_LINE = '@ATTRIBUTE %s %s'


def escape_string(string):
    """Quote and escape the given string."""
    if not isinstance(string, basestring):
        string = str(string)
    return '"%s"' % string.replace('"', r'\"')


class FeatureFunction(object):
    """Thin wrapper around a function which generates features
    for an ARFF file.
    """
    TO_STRING = {
        'numeric': lambda x: str(float(x)),
        'integer': lambda x: str(float(int(x))),
        'real': lambda x: str(float(x)),
        'nominal': escape_string,
        'string': escape_string,
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
            data_type = '{%s}' % ','.join(escape_string(nominal) for
                    nominal in self.nominals)
        else:
            data_type = self.attribute_type

        return ATTRIBUTE_LINE % (self.attribute_name, data_type)

    def set_type_from_val(self, val):
        """Deduce the proper to_string function from the type of val."""
        # Fun facts -- you have to check isinstance(val, bool) before
        # isinstance(val, numbers.Number) because for unfathomable
        # reasons, bool is an integer subclass.
        if isinstance(val, bool):
            attribute_type = 'nominal'
            self.nominals = [str(True), str(False)]
        elif isinstance(val, basestring):
            attribute_type = 'string'
        elif isinstance(val, numbers.Number):
            attribute_type = 'numeric'
        elif isinstance(val, (datetime.date, datetime.datetime)):
            attribute_type = 'date'
        else:
            raise ValueError("Unable to deduce ARFF type of %s" % val)

        self.attribute_type = attribute_type
        self.result_to_string = self.TO_STRING[attribute_type]
        return attribute_type

    def __call__(self, *args, **kwargs):
        """Return the result of the wrapped function as a string
        suitable for an ARFF file.
        """
        result = self.func(*args, **kwargs)
        if self.result_to_string is None:
            self.set_type_from_val(result)
        return self.result_to_string(result)


def feature(fname=None, returns=None, nominals=None):
    """Decorator for designating functions as weka feature functions."""

    def feature_maker(func):
        """Adds nescessary weka attributes to a function."""

        return FeatureFunction(
                func,
                attribute_name=fname,
                attribute_type=returns,
                nominals=nominals)

    return feature_maker


def find_feature_functions(module):
    """Return an interator yielding all feature functions
    on the given module.
    """
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, FeatureFunction):
            yield attr


def get_header(feature_funcs, relation_name, class_name, classifications):
    """Return a string representing the header of an ARFF file."""

    classification_feature = FeatureFunction(
            None, attribute_name=class_name,
            attribute_type='nominal', nominals=classifications)
    feature_funcs = feature_funcs + [classification_feature]

    lines = []
    lines.append(RELATION_LINE % relation_name)
    lines.append('\n')
    for func in feature_funcs:
        lines.append(func.attribute_string())
    lines.append('\n')
    lines.append(DATA_LINE)
    return '\n'.join(lines)


def build_feature_file(relation_name, module, input_vals, class_name):
    """Write an arff file."""
    funcs = list(find_feature_functions(module))

    feature_vals = []
    classifications = set()
    for input_val, classification in input_vals:
        features = [func(input_val) for func in funcs]
        features.append(escape_string(classification))
        classifications.add(classification)
        feature_vals.append(','.join(features))

    contents = [get_header(funcs, relation_name, class_name, classifications)]
    contents.extend(feature_vals)
    return '\n'.join(contents)


def write_feature_file(
        out_file_name, relation_name, module, input_vals, class_name):
    """Write an arff file."""
    with open(out_file_name, 'w') as out_file:
        out_file.write(build_feature_file(
            relation_name, module, input_vals, class_name))
        out_file.write('\n')
