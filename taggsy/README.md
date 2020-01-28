### README


Taggsy is a python library that will pick the most common occuring words between a number documents.

Example usage: 

```python
from taggsy import Core
core = Core()
text1 = 'An example document'
text2 = 'Another document'

core.add_documents([text1, text2])
core.most_common()
```


