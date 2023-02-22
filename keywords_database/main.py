#This script is used to retrieve and sort keywords from the database
#It will save the list as a json file

import argparse
import json
from progress.bar import Bar

from src.path_finder import PathFinder, TextExtractor
from src.keywords_sorter import KeywordSorter

def main(base_path, output_file) :
    # Search for all folders that contain xml files
    print('[-] Searching for all folders')
    finder = PathFinder(base_path)
    finder.run_finder()
    folders = finder.paths

    # Extract descriptions from the xml files
    print('[-] Extracting descriptions')
    extractor = TextExtractor(folders)
    extracted_dict = []
    with Bar('Processing', max=len(folders)) as bar:
        for text_dict in extractor.extract():
            # Load the current values from the output file
            with open(output_file, 'r', encoding='UTF-8') as out_file:
                current_values = json.load(out_file)
            # Add the newly extracted text dict to the current values
            current_values.append(text_dict)
            extracted_dict.append(text_dict)
            # Write the updated values to the output file
            with open(output_file, 'w+', encoding='UTF-8') as out_file:
                json.dump(current_values, out_file, ensure_ascii=False)
            bar.next()
        bar.finish()

    # Process the lemmas and sort them
    print('[-] Processing lemmas')
    sorter = KeywordSorter(extracted_dict)
    with open(f'keywords_{output_file}', 'w+', encoding='UTF-8') as file:
        json.dump(sorter.sort(), file, ensure_ascii=False)

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Generates sorted list of keywords')
    parser.add_argument('--base_path', help='Root path of the database', required=True)
    parser.add_argument('--output', help='Output path of the json file', default='output.json')
    args = parser.parse_args()

    # Run the main function
    main(args.base_path, args.output)
