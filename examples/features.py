import arff_writer


@arff_writer.feature(fname='echo', returns='string')
def str_func(x):
    return x


@arff_writer.feature(fname='echo_snakes', returns='string')
def another_func(x):
    return x + ' snakes'


@arff_writer.feature()
def just_two(x):
    return 2


def not_a_feature(x):
    return x + 1
