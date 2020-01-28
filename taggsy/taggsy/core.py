import os

from .helpers import is_word, is_stopword, filter_stopwords, generate_random_string

SENTENCE_SEPARATOR = '.'


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


class Word(DocumentComponent):

    def __init__(self, text=None, sentence_text=None, document=None):
        super().__init__()
        self.text = text if text is not None else None
        self.sentence_text = sentence_text if sentence_text is not None else None
        self.document = document if document else None
    
    def __str__(self):
        return f'{self.__class__.__name__!s}(text={self.text!s}, sentence_text={self.sentence_text!s}, document={self.document!s})'

    def __repr__(self):
        return f'{self.__class__.__name__!r}(text={self.text!r}, sentence_text={self.sentence_text!r}, document={self.document!r})'
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.text == other.text

    def __hash__(self):
        return hash(self.text)        

    @classmethod
    def from_text(cls, text, sentence_text=None, document=None):
        return cls(text=text, sentence_text=sentence_text, document=document)

    def _compute(self, table):
        if not self.text:
            return table
        if self.text in table:
            if self.document.name not in table[self.text]['docs']:
                table[self.text]['docs'].append(self.document.name)
                table[self.text]['sentences'].append(self.sentence_text)
                table[self.text]['count'] += 1
        else:
            table[self.text] = {'count': 1, 'docs': [self.document.name], 'sentences': [self.sentence_text]}
        return table

    
class Sentence(DocumentComponent):

    def __init__(self, text=None, words=None, document=None):
        super().__init__()
        self.text = text if text is not None else ''
        self.words = words if words is not None else []
        self.document = document if document is not None else None

    def __str__(self):
        return f'{self.__class__.__name__!s}(text={self.text!s}, words={self.words!s}, document={self.document!s})'

    def __repr__(self):
        return f'{self.__class__.__name__!r}(text={self.text!r}, words={self.words!r}, document={self.document!r})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.text == other.text and self.words == other.words
    
    def __hash__(self):
        return (hash((self.text, self.words)))

    def _compute(self, table):
        for word in self.words:
            word.compute(table=table)
        return table

    @classmethod
    def from_text(cls, text, document):
        return cls(
            text=text, 
            words=[Word.from_text(text=word, sentence_text=text, document=document) for word in filter_stopwords(words=text.split())]
            )


class Document(DocumentComponent):
    
    def __init__(self, name=None, text=None, sentences=None):
        super().__init__()
        self.name = name if name is not None else generate_random_string()
        self.sentences = sentences if sentences is not None else []
        self.text = text if text is not None else ''
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.text == other.text
        
    def __repr__(self):
        return f'{self.__class__.__name__!r}(name={self.name!r}, sentences={self.sentences!r}, text={self.text!r})'
    
    def __str__(self):
        return f'{self.__class__.__name__!s}(name={self.name!s}, sentences={self.sentences!s}, text={self.text!s})'
    
    def _compute(self, table):
        for sentence in self.sentences:
            sentence.compute(table=table)
        return table

    @classmethod
    def from_path(cls, path):
        with open(path, 'r') as f:
            return cls.from_text(
                name=os.path.basename(path),
                text=f.read()
                )

    @classmethod
    def from_text(cls, text, name=None):
        document = cls(text=text, name=name)
        document.sentences = [Sentence.from_text(document=document, text=dot_seperated_string) for dot_seperated_string in text.split(SENTENCE_SEPARATOR)]
        return document
    

class Core(DocumentComponent):

    def __init__(self, documents=None):
        super().__init__()
        self.table = {}
        self.documents = documents if documents is not None else []

    def __repr__(self):
        return f'{self.__class__.__name__!r}(table={self.table!r}, documents={self.documents!r})'
    
    def __str__(self):
        return f'{self.__class__.__name__!s}(table={self.table!s}, documents={self.documents!s})'
    
    def add_documents(self, docs):
        for doc in docs:
            self.add_document(doc)
    
    def add_document(self, doc, name=None):
        if os.path.exists(doc):
            document = Document.from_path(path=doc)
        else:
            document = Document.from_text(text=doc, name=name)
        self.documents.append(document)
        self.should_recompute = True
        return document.name

    def most_common(self):
        return self.compute()

    def _compute(self):
        for document in self.documents:
            table = document.compute(table=self.table)
        results = {key: value for key,value in self.table.items() if value['count'] >= 2}
        return {key: value for key, value in sorted(results.items(), key=lambda x: x[1].get('count'), reverse=True)}

