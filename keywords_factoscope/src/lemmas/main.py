import spacy

class Lemmatizor :
    """
        Initialize the French NLP model and create stop words set.
    """
    def __init__(self) :
        self.nlp = spacy.load('fr_core_news_md')
        # Get the default stop words from spacy and add custom stop words
        self.stop_words = self.nlp.Defaults.stop_words
        self.stop_words.update([
            '.', ',', ';', '!', ':', ' ',
            '«', '»', '(', ')', '-', '[', ']', '…'
        ])

    """
        Processing the input sentence using the spacy model

        :param sentence: The sentence to be processed
    """
    def process(self, sentence):

        self.processed = self.nlp(sentence)

    """
        Return a list of lemmas of the processed sentence, otherwise an empty list

        :return: A list of lemmas
    """
    def get_lemmas(self):

        if hasattr(self, 'processed'):
            return [lemma.lemma_ for lemma in self.processed if lemma.lemma_ not in self.stop_words]
        return []

    """
        Return a list of named entities of the processed sentence, otherwise an empty list

        :return: A list of named entities
    """
    def get_named_entities(self):

        if hasattr(self, 'processed'):
            return [ent.lemma_ for ent in self.processed.ents]
        return []
