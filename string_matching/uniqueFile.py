# This script is used to count every occurrence of keywords in all the audio files
# It needs the transcript file generated by transcripts and keywords cleaned file
# generated by both keywords_database and keywords_factoscope
# It will generates a unique json file containing containing every keyword and the number of occurrences
# for all the audio files

import argparse
import json
import re
import time
from fuzzywuzzy import fuzz, process
from progress.bar import Bar

def generate_empty_keywords_dict(keywords):
    """
    Generates an empty dictionary to store the count of keyword occurences.
    The dictionary keys are the keywords and the values are initialized to 0.
    """
    temp_dict = {}
    for keyword in keywords:
        if keyword not in temp_dict:
            temp_dict[keyword] = 0
    return temp_dict


def main(transcript_path, keywords_path, output_path):
    start_time = time.perf_counter()
    print('[-] Importing data')
    # Load keywords and transcripts data from files
    with open(keywords_path, 'r', encoding='UTF-8') as file:
        keywords = json.load(file)
    with open(transcript_path, 'r', encoding='UTF-8') as file:
        transcripts = json.load(file)

    print('[-] Generating statistics')
    data = []
    with Bar('Processing', max=len(transcripts)) as bar:
        occurences_dict = generate_empty_keywords_dict(keywords)
        for transcript in transcripts:
            # Tokenize the transcript text into words
            words = re.findall(r'\b\w+\b', transcript["text"])
            for keyword in keywords:
                # Find occurences of keyword in the words with at least 90% confidence
                result = process.extractBests(keyword, words, scorer=fuzz.token_set_ratio,
                                              score_cutoff=90, limit=None)
                occurences_dict[keyword] += len(result)
            bar.next()
        data.append(occurences_dict)
        bar.finish()

    print('[-] Saving results')
    # Save the keyword occurences data to the output file
    with open(output_path, 'w+', encoding='UTF-8') as file:
        json.dump(data, file, ensure_ascii=False)
    end_time = time.perf_counter()

    print("Duration:", end_time - start_time, "seconds")


# Parse command line arguments
parser = argparse.ArgumentParser(description='Counts keywords occurences for each audio files')
parser.add_argument('--transcript', help='Path of the transcripts file', required=True)
parser.add_argument('--keywords', help='Path of the keywords file', required=True)
parser.add_argument('--output', help='Output path of the json file', default='output.json')
args = parser.parse_args()

if __name__ == "__main__":
    main(args.transcript, args.keywords, args.output)
