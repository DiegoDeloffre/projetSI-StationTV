import spacy

class Lemmatizor:
    """
        Initializes the Lemmatizor class by loading the French language model using spacy
        and initialize the processed sentence to None.
   """
    def __init__(self):
        self.nlp = spacy.load('fr_core_news_md')
        self.stop_words = self.nlp.Defaults.stop_words
        self.stop_words.update({'.', ',', ';', '!', ':', ' '})
        self.processed = None

    """
        Process the input sentence using spacy NLP model.
    """
    def process(self, sentence):

        self.processed = self.nlp(sentence)

    """
        Get the lemmatized form of each word in the processed sentence, filtering out stop words.

        :return: A list of lemmas.
    """
    def get_lemmas(self):

        if self.processed:
            return [
                lemma.lemma_ for lemma in self.processed
                if lemma.lemma_ not in self.stop_words
            ]
        return []

    """
        Get the named entities from the processed sentence.

        :return: A list of named entities.
    """
    def get_named_entities(self):

        if self.processed:
            return [ent.lemma_ for ent in self.processed.ents]
        return []
