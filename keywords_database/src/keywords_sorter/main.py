from src.lemmas import Lemmatizor

class KeywordSorter:
    """
    Initializes the KeywordSorter class with the keywords dictionary.

    :param keywords_dict: the keywords dictionary
    """
    def __init__(self, keywords_dict):
        self.keywords_dict = keywords_dict
        self.lemmas = {}
        self._parse()

    """
    Parses the keyword dictionary to get the lemmas and count their occurrences.
    """
    def _parse(self):
        lemmatizor = Lemmatizor()
        # Loop through each keyword dictionary
        for keyword_dict in self.keywords_dict:
            # Use the Lemmatizor to process the text field in the keyword dictionary
            lemmatizor.process(keyword_dict["text"])
            # Loop through the lemmas from the Lemmatizor
            for lemma in lemmatizor.get_lemmas():
                # Check if the lemma is in the lemmas dictionary
                if lemma not in self.lemmas:
                    # If not, add the lemma to the dictionary with a count of 0
                    self.lemmas[lemma] = 0
                # Increment the count of the lemma by 1
                self.lemmas[lemma] += 1

    """
    Sorts the lemmas dictionary by the number of occurrences.

    :return: the sorted lemmas dictionary
    """
    def sort(self):
        # Sort the lemmas dictionary by the number of occurrences in reverse order
        return dict(sorted(self.lemmas.items(), key=lambda item: item[1], reverse=True))
