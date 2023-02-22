import spacy

class Lemmatizor:
    """
    Initialize the French NLP model and create stop words set.
    """
    def __init__(self):
        self.nlp = spacy.load('fr_core_news_md')  # Load the French NLP model
        self.stop_words = self.nlp.Defaults.stop_words  # Create stop words set
        self.stop_words.add('.')  # Add punctuations to stop words set
        self.stop_words.add(',')
        self.stop_words.add(';')
        self.stop_words.add('!')
        self.stop_words.add(':')
        self.stop_words.add(' ')
        self.processed = None  # Initialize processed variable to None

    """
    Use the French NLP model to process the sentence.
    """
    def process(self, sentence):
        self.processed = self.nlp(sentence)  # Process the sentence using the French NLP model

    """
    Get the lemmatized words, excluding stop words.
    """
    def get_lemmas(self):
        if self.processed is not None:  # If the sentence has been processed
            return [lemma.lemma_ for lemma in self.processed if lemma.lemma_ not in self.stop_words]  # Return lemmatized words excluding stop words
        return []  # Return an empty list if the sentence has not been processed

    """
    Get named entities from the processed sentence.
    """
    def get_named_entities(self):
        if self.processed is not None:  # If the sentence has been processed
            return [ent.text for ent in self.processed.ents]  # Return named entities
        return []  # Return an empty list if the sentence has not been processed
