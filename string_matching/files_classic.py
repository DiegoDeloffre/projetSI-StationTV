# This script is used to count every occurrence of keywords per processed audio file
# It needs the transcript file generated by transcripts and keywords cleaned file
# generated by both keywords_database and keywords_factoscope
# It will generates a json file containing every keyword for an audio file and will store
# them in the same hierarchy as the original database

import argparse
import json
import os
import re
import time
from fuzzywuzzy import fuzz
from progress.bar import Bar


def generate_empty_keywords_dict(keywords):
    """Generates an empty keywords dictionary with 0 values"""
    temp_dict = {}
    for keyword in keywords:
        if keyword not in temp_dict:
            temp_dict[keyword] = []
    return temp_dict


def generate_keywords_ids(keywords):
    """Generates a dictionary of keywords and their corresponding ids"""
    temp_dict = {}
    for idx, keyword in enumerate(keywords):
        if keyword not in temp_dict:
            temp_dict[keyword] = idx
    return temp_dict


def generate_output(transcript, transcriptTab, keywords, keyword_ids):
    """Generates the final output containing keyword occurrences in the transcript"""
    current_data = {
        "file": transcript['file']
    }
    occurences_dict = generate_empty_keywords_dict(keywords)
    data = []
    for keyword in keywords:
        # Searching for keyword occurence in text with 90% confidence
        results = []
        for word in transcriptTab:
            score = fuzz.token_set_ratio(keyword, word)
            if score >= 90:
                results.append((word, score))

        if len(results) > 0:
            position = -1
            for i, result in enumerate(results):
                word, score = result
                position = transcript["text"].find(word, position + 1)
                data.append([keyword_ids[keyword], keyword, position, score, word])
        current_data['keywords'] = data

    return current_data


def main(transcript_path, keywords_path):
    """Main function which calls other functions to process transcripts and count keyword occurrences"""
    print('[-] Importing data')
    # Loading data needed
    with open(keywords_path, 'r', encoding='UTF-8') as file:
        keywords = json.load(file)

    with open(transcript_path, 'r', encoding='UTF-8') as file:
        transcripts = json.load(file)

    keyword_ids = generate_keywords_ids(keywords)
    print('[-] Generating statistics')

    with Bar('Processing', max=len(transcripts)) as bar:
        for transcript in transcripts:
            start_time = time.perf_counter()

            # Tokenize the string into words
            tab = re.findall(r'\b\w+\b', transcript["text"])

            # Generate the output
            data = generate_output(transcript, tab, keywords, keyword_ids)

            file_path = transcript["file"]
            timestamp = str(int(time.time()))

            # Split the file path into directory and filename
            directory, filename = os.path.split(file_path)

            # Remove the "F:/" part from the directory
            directory = directory[3:]

            # Create the directory hierarchy if it does not exist
            os.makedirs(directory, exist_ok=True)

            # Write the JSON data to the file
            with open(f"{directory}/{timestamp}_spot.json", "w", encoding="utf-8") as f:
                json.dump(data, f)

            bar.next()
            end_time = time.perf_counter()

            print("Durée d'exécution :", end_time - start_time, "secondes")
        bar.finish()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Counts keywords occurences for each transcript')
parser.add_argument('--transcript', help='Path of the transcripts file', required=True)
parser.add_argument('--keywords', help='Path of the keywords file', required=True)
args = parser.parse_args()

if __name__ == "__main__":
    main(args.transcript, args.keywords)