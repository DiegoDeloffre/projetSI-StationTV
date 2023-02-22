import json
from os import path
import whisper
from threading import Thread
from progress.bar import Bar
from src.lemmas import Lemmatizor


# STTBrain class to process and save the transcription results
class STTBrain:
    """
        Initializes the STTBrain class

        Parameters:
        file_list (list): List of files to be processed
        output_file (str): File to save the processing results
        model (str, optional): Model name to use for transcribing the audio. Defaults to 'base'.
        processed (list, optional): List of already processed files. Defaults to [].
    """
    def __init__(self, file_list, output_file, model='base', processed=[]):
        # List of files to be processed
        self.file_list = file_list
        # File to save the processing results
        self.output_file = output_file
        # Loading the whisper model
        self.model = whisper.load_model(model)
        # Initializing the Lemmatizor class
        self.lemmatisor = Lemmatizor()
        # List of already processed files
        self.results = processed

    """
        Starts the processing of the files and saves the results
    """
    def run(self):
        # Variable to keep track of processed files
        index = 0
        # Using a progress bar to show the processing status
        with Bar('Processing', max=len(self.file_list)) as bar:
            for file in self.file_list:
                # Increasing the processed file counter
                index += 1
                # Getting the transcription result from the model
                result = self.model.transcribe(file, fp16=False)
                # Processing the text using the Lemmatizor class
                self.lemmatisor.process(result['text'])
                # Adding the result to the list of results
                self.results.append({
                    "file": file,
                    "text": result['text'],
                    "lemmas": self.lemmatisor.get_lemmas(),
                    "named_entities": self.lemmatisor.get_named_entities()
                })
                # Saving progress every 10 processed files in case recovery is needed
                if index % 10 == 0:
                    self.save_progress()
                # Updating the progress bar
                bar.next()
            # Finishing the progress bar
            bar.finish()
            # Saving the final results
            self.save_progress()

    """
        Saves the current processing results to the output file
    """
    def save_progress(self):
        # Checking if the output file exists
        if not path.exists(self.output_file):
            # Initializing an empty list if the file does not exist
            jsoned_content = []
        else:
            # Loading the content of previous saves
            with open(self.output_file, 'r', encoding='UTF-8') as file:
                jsoned_content = json.loads(file.read())
        # Appending the new results to the existing results
        for file in self.results:
            jsoned_content.append(file)
        # Writing the results to the output file
        with open(self.output_file, 'w', encoding='UTF-8') as file:
            json.dump(jsoned_content, file, ensure_ascii=False)

        # Clearing the results list
        self.results = []

# STTWorker class to process the files using multiple threads
class STTWorker(Thread):
    # class variable to store the results of STT
    results = []

    """
        Initialize the class with a list of files and a model name.

        :param file_list: list of audio files to transcribe.
        :param model: name of the model to use for transcription. Default is "base".
    """
    def __init__(self, file_list, model="base"):

        # Call the parent class constructor
        Thread.__init__(self)

        # initialize the file list and model name
        self.file_list = file_list
        self.model = whisper.load_model(model)
        self.lemmatisor = Lemmatizor()

    """
        Perform the speech to text transcription for each file in the file list.

        :return: None
    """
    def run(self):

        # Loop over the files in the file list
        for file in self.file_list:
            # Transcribe the audio in the file using the STT model
            result = self.model.transcribe(file)
            # Process the result text
            self.lemmatisor.process(result['text'])
            # Append the result to the class variable results
            STTWorker.results.append({
                "file": file,
                "text": result['text'],
                "lemmas": self.lemmatisor.get_lemmas(),
                "named_entities": self.lemmatisor.get_named_entities()
            })

if __name__ == "__main__":
    # Create an instance of the STTBrain with file list and number of workers
    brain = STTBrain(["video.MP4", "video.MP4"], 1)
    # Start the brain to run the STT process
    brain.run()
