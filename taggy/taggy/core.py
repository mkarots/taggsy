

class Taggy:

    def __init__(self, database=None, word_counter=None):
        self.database = database if database else {}
        self.word_counter = word_counter

    def add_text(self, text):
        raise NotImplementedError()

    def get_tags(self, document_ids):
        raise NotImplementedError()

