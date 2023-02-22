import xml.etree.ElementTree as ET

class TextExtractor:
    """
        Initialize the TextExtractor with the input file path.

        :param file: The path of the xml file to extract descriptions from.
    """
    def __init__(self, file):
        self.file = file

    """
        Extracts descriptions for each News tag in the xml file.

        :return: A list of extracted descriptions.
    """
    def extract(self):

        texts = []
        # Parse the xml file
        xml_file = ET.parse(self.file)
        # Get the root element
        root = xml_file.getroot()
        # Find all News elements
        news = root.findall('News')
        # Loop through all News elements
        for news_entry in news:
            # Check if the 'texteDescriptif' attribute exists
            if 'texteDescriptif' in news_entry.attrib:
                # Add the description to the texts list
                texts.append(news_entry.attrib['texteDescriptif'])

        # Return the extracted descriptions
        return texts
