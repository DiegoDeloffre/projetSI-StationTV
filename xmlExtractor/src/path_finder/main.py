from os import listdir, path
import xml.etree.ElementTree as ET


class PathFinder:
    """
    A class for finding all subdirectories under a given path.
    """

    """
        Initialize the PathFinder object with a base path.
    """
    def __init__(self, base_path):
        self.base_path = base_path
        self.paths = set()

    """
        A helper function that returns a set of subdirectories within a given folder.
    """
    def _list_dirs(self, current_folder, folders_and_files):

        folders = set()
        for element in folders_and_files:
            current_path = path.join(current_folder, element)
            if path.isdir(current_path):
                folders.add(current_path)

        return folders

    """
        A function that finds all subdirectories under the base path or a given starting point.
    """
    def run_finder(self, starting_point=None):
        if starting_point is None:
            starting_point = self.base_path

        folders = self._list_dirs(starting_point, listdir(starting_point))

        if len(folders) == 0:
            self.paths.add(starting_point)
            return

        for folder in folders:
            next_path = path.join(starting_point, folder)
            self.run_finder(starting_point=next_path)


class XMLPathFinder:
    """
    A class for finding XML files within a set of folders.
    """

    """
        Initialize the XMLPathFinder object with a set of folders.
    """
    def __init__(self, folders):
        self.folders = folders

    """
        A generator function that yields the path of each XML file within the set of folders.
    """
    def extract(self):
        for folder in self.folders:
            splited_path = path.normpath(folder).split(path.sep)
            timestamp = splited_path[-1]
            xml_file = path.join(folder, f'{timestamp}.xml')
            yield xml_file
