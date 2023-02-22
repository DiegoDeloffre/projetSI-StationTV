#This script is used to extract all xml files in the database into one json file for easier processing
#It will generate a json file containing every xml file contents
import argparse
import json
import xmltodict
from progress.bar import Bar

from src.path_finder import PathFinder, XMLPathFinder

def main(base_path, output):
    """Main function to extract data from xml files and save it as a json file."""

    # Finding all folders
    print('[-] Searching for all folders')
    finder = PathFinder(base_path) # Create an instance of PathFinder
    finder.run_finder() # Run the function to find the folders
    folders = finder.paths # Get the list of folders

    # Finding all XML files
    print('[-] Searching for all XML files')
    xml_finder = XMLPathFinder(folders) # Create an instance of XMLPathFinder
    xml_files = [] # Initialize an empty list to store the xml files
    for xml_file in xml_finder.extract(): # Extract the xml files
        xml_files.append(xml_file) # Append the xml file to the list

    # Extracting data from xml files
    print('[-] Extracting data')
    data = [] # Initialize an empty list to store the extracted data
    with Bar('Processing', max=len(xml_files)) as bar: # Create a progress bar
        for xml_file in xml_files:
            with open(xml_file, 'r', encoding='UTF-8') as file:
                # Read the content of the xml file
                stringed_xml = file.read()
                # Convert the xml content to python dictionary
                temp_data = xmltodict.parse(stringed_xml)
                # Add the xml file name to the dictionary
                temp_data['file'] = xml_file
                # Append the extracted data to the list
                data.append(temp_data)
            bar.next() # Move the bar to the next step
        bar.finish() # Finish the bar

    # Saving the extracted data as a json file
    print('[-] Saving data')
    with open(output, 'w+', encoding='UTF-8') as file:
        # Write the extracted data to the json file
        json.dump(data, file, ensure_ascii=False)

if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Generates metadata file')
    parser.add_argument('--base_path', help='Root path of the database', required=True)
    parser.add_argument('--output', help='Output path of the json file', default='output.json')
    args = parser.parse_args()
    main(args.base_path, args.output)
