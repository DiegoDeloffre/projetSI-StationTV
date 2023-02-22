#This script is used to retrieve and sort keywords from the factoscope database
#It will save the list as a json file

import argparse
import json

# Import the classes from the specified modules
from src.path_finder import TextExtractor
from src.keywords_sorter import KeywordSorter


def main(xml_file, output_file):
    # Extract the descriptions from the XML file
    print('[-] Extracting descriptions')
    extractor = TextExtractor(xml_file)
    extracted_dict = []
    # Loop through each extracted text dictionary
    for text_dict in extractor.extract():
        extracted_dict.append(text_dict)

    # Process the lemmas
    print('[-] Processing lemmas')
    sorter = KeywordSorter(extracted_dict)
    # Write the sorted list of keywords to the output file
    with open(f'{output_file}', 'w+', encoding='UTF-8') as file:
        json.dump(sorter.sort(), file, ensure_ascii=False)


# Parse the command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates sorted list of keywords')
    parser.add_argument('--xml_file', help='Root path of the database', required=True)
    parser.add_argument('--output', help='Output path of the json file', default='output.json')
    args = parser.parse_args()
    main(args.xml_file, args.output)
