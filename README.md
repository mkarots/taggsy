### README


Taggsy is a python library that will pick the most common occuring words between a number documents.

Example usage: 

```python
from taggsy import Core
core = Core()
text1 = 'An example document'
text2 = 'Another document'

core.add_documents([text1, text2])
print(core.most_common())

>>> {'document': 
    {'count': 2,
     'docs': ['fbyzuj', 'ktbuwx'],
     'sentences': ['An example document', 'Another document']}}
```

Or run as python module

```shell

pip install . 

python -mtaggsy doc1.txt doc2.txt 
```


