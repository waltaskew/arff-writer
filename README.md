The Walt Askew Machine Learning Experience™
===========================================

In this repository, you will find tools for exploring the wonders of machine learning!  Quick start activate!

Requirements
------------
Download and install the Weka machine learning suite: http://www.cs.waikato.ac.nz/ml/weka/downloading.html

Quick Start
-----------
* check out this repository:
```
git clone git://github.com/waltaskew/arff-writer.git
```
* cd into the wonderful repository world:
```
cd arff-writer
```
* Write some functions that return useful features that will be used to classify the author of the text.
Here is an example of what your feature file should look like:

```python
import arff_writer
        
@arff_writer.feature()                  
def word_length(text):
    return len(text.split())
```
You can define as many feature functions as you want.
All functions which return feature values must have @arff_writer.feature() directly above their declaration.

* Generate your feautre file.  Assuming the file you wrote in step three is named my_features.py:

```python
PYTHONPATH=.:src/ src/gen_arff --feature_module=my_features --corpus_dir=examples/corpus/
```
This will generate a file named "feature.arff" in the current directory.  
Take a look!
You'll be able to spy the values your feature functions returned.

* Start weka, hit "Explorer," then "Open File," and point it towards the feature.arff file you generated.
* Select "All" on the Attributes pane
* On the "Classify" tab, choose and classifier, hit "Start" and see what your correct and incorrect classifications results are!

