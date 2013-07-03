The Walt Askew Machine Learning Experience™
===========================================

In this repository, you will find tools for exploring the wonders of machine learning!  Quick start time!

Requirements
------------
Download and install the Weka machine learning suite: http://www.cs.waikato.ac.nz/ml/weka/downloading.html

Download and install Git: http://git-scm.com/downloads

Quick Start
-----------
1. check out this repository:

    ```
    git clone git://github.com/waltaskew/arff-writer.git
    ```
    
2. cd into this wonderful repository:
    ```
    cd arff-writer
    ```

3. Write some functions that return useful features that will be used to classify the author of the text.
    Here is an example of what your feature file should look like:

    ```python
    import arff_writer
        
    @arff_writer.feature()                  
    def word_count(text):
        return len(text.split())
    ```
    
    You can define as many feature functions as you want.
    All functions which return feature values must have @arff_writer.feature() directly above their declaration.

4. Generate your feature file.  Assuming the file you wrote in the previous step is named my_features.py:

    ```python
    PYTHONPATH=.:src/ src/gen_arff --feature_module=my_features --corpus_dir=examples/corpus/
    ```
    
    This will generate a file named "feature.arff" in the current directory.  
    Take a look!
    You'll be able to spy the values your feature functions returned.

5. Start weka, hit "Explorer," then "Open File," and point it towards the feature.arff file you generated.
6. Select "All" on the Attributes pane
7. On the "Classify" tab, choose and classifier, hit "Start" and see what your correct and incorrect classifications results are!

Details
-------
Take a look at the examples/corpus directory in this repository.
You'll see directories with author names filled with texts each author has written.
These files and directories are the input to our feature functions.

Each text file in the author sub directories will be passed in-turn to all the feature functions you define.
The output of these functions is collected in the features.arff file, which we can then use for classification experiments in Weka.

If you would like to add more authors and texts to the project,
this is as simple as creating a new directory with the author's name and filling it with text files written by that author.
I have taken the texts in the example corpus from Project Guttenberg and selected texts from some of my favorite authors.

Project Guttenberg files have headers and footers beginning with 
```
*** START OF THIS PROJECT GUTENBERG EBOOK <book name> ***
*** END OF THIS PROJECT GUTENBERG EBOOK <book name> ***
```
respectively, which will be parsed out of the files before they are passed to the defined feature functions.

