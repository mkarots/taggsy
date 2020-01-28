## Problem Statement

The end goal is to have a software package that can generate hashtags based on common words between different texts/documents, in an efficient way, i.e, given 2 documents that contain "This is a hashtag", "Create hashtag today" the output, should contain the word 'hashtag', a reference to the documents it is contained, and a reference of the sentences it is contained in.


## Challenges

* **Avoiding unnecessary calculations** 
Given that even a medium sized document can contain thousands of characters, we need to be careful with using too much memory or doing innefficient/repeated calculations.
* **Not all words are of the same importance/value**. For example stopwords like 'is', 'are', 'and' do not provide value as it they are very common, and to be found in almost all texts.


## Proposed Solutions

Overview of solution(pseudocode):

```python

table = {}
for document in documents:
  for sentence in document:
    for word in sentence:
      table[word].append((document_id, sentence))
sort table with  respect to document_id count
return table 
      
```

In order to parse a document, we will break it down  into sentences, and then we will break down each sentence in the words it is made of, creating an object for each one of them. There is an intrinsic hierarchical structure to a document, sentences and words and for this reason, the objects involved mimic a physical document, (e.g Document, Sentence, Word).

In order to count occurences of words we will loop over all documents and traverse all sentences and words. Note that we need to count only one occurence of each word in each document, which means that if the word 'inspiration' exists in a document twice, we only need to record it once, which is a subtle but important optimization (we would avoid this optimization if for example we were to count the total number of occurences of words).

In order to traverse the tree effectively, we will take advantage of the the hierarchy of a document, by defining an abstract class called `DocumentComponent` and give it a method called `compute` as in: 


```python
class DocumentComponent:
    
    def compute(self):
        raise NotImplementedError('Subclasses should implement this method')
```

The classes `Word`, `Sentence`, `Document`, `Core` all inherit from `DocumentComponent`.
This makes `Word`, `Sentence`, `Document`, `Core`, have an identical interface. In order to avoid a Document and the Core component from redoing a calculation we protect the `compute` function with a flag in the primitive class like: 


```python
class DocumentComponent:
    
    def __init__(self):
        self.should_recompute = True

    def _compute(self):
        raise NotImplementedError('Subclasses should implement this method')

    def compute(self, *args, **kwargs):
        '''
        Wrapper for the compute function
        '''
        if self.should_recompute:
            self.should_recompute = False
            return self._compute(*args, **kwargs)
```

Classes are now responsible for setting the `should_recompute` parameter in order to avoid unnecesary computations.


### Avoiding unnecessary calculations:
In order to avoid unncessary calculations, we need to make use of the following two insights: 
a) Every document should only be counted once.
b) We need not care about a word if it appears twice on the same document


### Filtering out words:
There are two kinds of filtering involved 

* a) Filtering of non-words 
    We need to filter non-words so we get left with the actual words. Initially, the text will be split, into sentences using the dot '.' as a sentence separator. After this step, the rest of the punctuation is ignored.


* b) Filtering of stopwords
    We need to filter out stopwords, so we are left with the non-common words in the texts. This can easy be done by using an existing library like nltk or spacy. 


## Requirements
  
  ### Functional requirements:

  * Software should compute the most common occurring words between 2 or more documents.
  
  ### Non functional requirements:

* Implementation language: python

* Compatible platforms: Linux/MacOS

* API should be straighforward to use

* Should be usable both programmatically and as a script

* Library format: python package

* Output is in json/python dictionary format
