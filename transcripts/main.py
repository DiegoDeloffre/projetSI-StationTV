#This script is used to turn audio files into readable text and lists of both lemmas and named entities
#You can choose the model used for Speech to Text (https://github.com/openai/whisper)
#It will generate the results in a json file

import argparse
from os import path
import json

# Importing required modules from the src directory
from src.path_finder import PathFinder
from src.stt import STTBrain


def main(base_path, level, output_file):
    """
    Main function that performs the speech-to-text transcription
    """
    print('[-] Searching for all folders')
    # Create an instance of PathFinder to find all folders containing audio files
    finder = PathFinder(base_path)
    finder.run_finder()
    folders = finder.paths

    # Load any previous progress made in a previous run, if any
    already_processed = []
    jsoned_file = []
    if path.isfile(output_file):
        with open(output_file, 'r', encoding='UTF-8') as file:
            jsoned_file = json.load(file, ensure_ascii=False)
            for element in jsoned_file:
                already_processed.append(element['file'])

    # Generate the path of the audio files that need to be transcribed
    audio_files = []
    for folder in folders:
        audio_file = f'{path.normpath(folder).split(path.sep)[-1]}_audio.mp4'
        if audio_file not in already_processed:
            audio_files.append(path.join(folder, audio_file))

    print('[-] Starting Speech To Text')
    # Create an instance of STTBrain to perform speech-to-text transcription
    stt = STTBrain(audio_files, output_file, model=level, processed=already_processed)
    stt.run()


if __name__ == "__main__":
    # Argument parser to parse command-line arguments
    parser = argparse.ArgumentParser(description='Generates transcripts of audio files from the database')
    parser.add_argument('--base_path', help='Root path of the database', required=True)
    parser.add_argument('--output', help='Output path of the json file', default='output.json')
    parser.add_argument('--level', help='Level of STT', default='base')
    args = parser.parse_args()
    main(args.base_path, args.level, args.output)
    