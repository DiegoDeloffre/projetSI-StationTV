import xml.etree.ElementTree as ET
from os import listdir, path


class PathFinder:
    """
        Initializes the PathFinder class with the base path.

        :param base_path: path to the database
    """
    def __init__(self, base_path):
        self.base_path = base_path  # Assign the base path to an instance variable
        self.paths = set()  # Initialize an empty set to store paths

    """
        Returns all the folders in the current folder path.

        :param current_folder: current folder path
        :param folders_and_files: list of folders and files in the current folder path
    """
    def _list_dirs(self, current_folder, folders_and_files):
        folders = set()  # Initialize an empty set to store folders
        for element in folders_and_files:
            # For each element in the folder_and_files list
            current_path = path.join(current_folder, element)  # Join the current folder path with the element name
            if path.isdir(current_path):  # Check if the current path is a directory
                folders.add(current_path)  # Add it to the folders set if it's a directory

        return folders

    """
        Visit every folder recursively until there are no more folders.

        :param starting_point: starting point for the search, default is None
    """
    def run_finder(self, starting_point=None):
        if starting_point is None:
            starting_point = self.base_path  # If starting point is None, set it to base_path

        folders = self._list_dirs(starting_point, listdir(starting_point))  # Get all the folders in the current path
        if len(folders) == 0:
            self.paths.add(starting_point)  # If there are no more folders, add the starting point to the paths set
            return

        for folder in folders:
            # For each folder in the current path
            next_path = path.join(starting_point, folder)  # Join the starting point with the folder name
            self.run_finder(starting_point=next_path)  # Recursively call the function for the next folder


class TextExtractor:
    """
        Initializes the TextExtractor class with a list of folders.

        :param folders: list of folders to extract text from
    """
    def __init__(self, folders):
        self.folders = folders  # Assign the folders to an instance variable
        self.indexes = set()  # Initialize an empty set for indexes

    """
        Extract the folder path and text field of every xml file.
    """
    def extract(self):
        for folder in self.folders:
            splited_path = path.normpath(folder).split(path.sep)
            timestamp = splited_path[-1]
            xml_file = ET.parse(path.join(folder, f'{timestamp}.xml'))
            # Parsing the xml file using ElementTree

            root = xml_file.getroot()
            desc = None
            if root.find('desc') is not None:
                # If desc field is present in the xml, assign it to desc variable
                desc = root.find('desc').text
            elif root.find('sub-title') is not None:
                # If desc field is not present in the xml but sub-title field is present, assign it to desc variable
                desc = root.find('sub-title').text

            if desc is not None:
                # If the desc is not None, yield a dictionary containing folder path and text
                yield {
                    "folder": folder,
                    "text": desc
                }
