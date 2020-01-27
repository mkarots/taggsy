import os

from .helpers import is_word, is_stopword, filter_stopwords, generate_random_string

SENTENCE_SEPARATOR = '.'


class CoreModel:
    
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
            

class Word(CoreModel):

    def __init__(self, text=None, sentence_text=None, document=None):
        super().__init__()
        self.text = text if text is not None else None
        self.sentence_text = sentence_text if sentence_text is not None else None
        self.document = document if document else []
    
    @classmethod
    def from_text(cls, text, sentence_text, document):
        return cls(text=text, sentence_text=sentence_text, document=document)

    def _compute(self, table):
        if self.text in table:
            if self.document.name not in table[self.text]['docs']:
                table[self.text]['docs'].append(self.document.name)
                table[self.text]['sentences'].append(self.sentence_text)
                table[self.text]['count'] += 1
        else:
            table[self.text] = {'count': 1, 'docs': [self.document.name], 'sentences': [self.sentence_text]}
        return table

    def __hash__(self):
        return hash(self.text)
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name


class Sentence(CoreModel):

    def __init__(self, text=None, words=None, document=None):
        super().__init__()
        self.text = text if text is not None else ''
        self.words = words if words is not None else []
        self.document = document if document is not None else None

    def _compute(self, table):
        for word in self.words:
            table = word.compute(table=table)
        return table

    @classmethod
    def from_text(cls, text, document):
        return cls(text=text, 
            words=[Word.from_text(text=word, sentence_text=text, document=document) for word in filter_stopwords(words=text.split())])


class Document(CoreModel):
    
    def __init__(self, name=None, text=None, sentences=None):
        super().__init__()
        self.name = name if name is not None else generate_random_string()
        self.sentences = sentences if sentences is not None else []
        self.text = text if text is not None else ''

    def _compute(self, table):
        for sentence in self.sentences:
            table = sentence.compute(table=table)
        return table

    @classmethod
    def from_path(cls, path):
        return cls.from_text(name=os.path.basename(path), text=open(path, 'r').read())

    @classmethod
    def from_text(cls, text, name=None):
        document = cls(text=text, name=name)
        document.sentences = [Sentence.from_text(document=document, text=dot_seperated_string) for dot_seperated_string in text.split(SENTENCE_SEPARATOR)]
        return document
    

class Core(CoreModel):

    def __init__(self, documents=None):
        super().__init__()
        self.table = {}
        self.documents = documents if documents is not None else []

    def add_document(self, path=None, text=None, name=None):
        if path:
            document = Document.from_path(path=path)
        elif text:
            document = Document.from_text(text=text, name=name)
        self.documents.append(document)
        self.should_recompute = True
        return document.name

    def most_common(self):
        return self.compute()

    def _compute(self):
        for document in self.documents:
            table = document.compute(table=self.table)
        results = {k: v for k,v in self.table.items() if v['count'] > 2}
        return {k: v for k, v in sorted(results.items(), key=lambda x: x[1].get('count'), reverse=True)}

