from src.lemmas import Lemmatizor

class KeywordSorter:
    """
         Initialize the KeywordSorter class with input keywords_dict.

        :param keywords_dict: Dictionary of keywords to be processed and sorted.
    """
    def __init__(self, keywords_dict):
        # Saving input keywords_dict to class variable
        self.keywords_dict = keywords_dict
        # Initializing dictionary for lemmas
        self.lemmas = {}
        # Parsing the keywords_dict to count lemmas
        self._parse()

    """
        Parse the keywords_dict to count lemmas.
    """
    def _parse(self):
        # Initializing Lemmatizor object
        lemmatizor = Lemmatizor()
        # Iterating over each keyword_dict
        for keyword_dict in self.keywords_dict:
            # Processing the keyword_dict using lemmatizor object
            lemmatizor.process(keyword_dict)
            # Getting lemmas from the processed keyword_dict
            for lemma in lemmatizor.get_lemmas():
                # If the lemma is not already in lemmas dictionary, add it with value 0
                if lemma not in self.lemmas:
                    self.lemmas[lemma] = 0
                # Increment the count for the lemma in lemmas dictionary
                self.lemmas[lemma] += 1

    """
         Sort the lemmas dictionary based on their count (number of occurences) in descending order.

        :return: A dictionary of sorted lemmas and their counts.
    """
    def sort(self):
        # Sorting the lemmas dictionary based on value (number of occurences)
        # in reverse order (descending order)
        return dict(sorted(self.lemmas.items(), key=lambda item: item[1], reverse=True))
