import features
import arff_writer

arff_writer.write_feature_file('test.arff', 'test', features, ['a', 'b'])
