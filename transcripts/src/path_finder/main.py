from os import listdir, path

class PathFinder:
    """
        Initialize the class with base_path, the starting directory to look for folders.

        :param base_path: The base path to start the directory search from.
    """
    def __init__(self, base_path):
        self.base_path = base_path
        self.paths = set()

    """
        A helper function to list all the directories in the current_folder.

        :param current_folder: The current folder to search for subdirectories.
        :param folders_and_files: A list of elements in the current_folder.
        :return: A set of subdirectories found in the current_folder.
    """
    def _list_dirs(self, current_folder, folders_and_files):
        folders = set()
        # Iterate over all elements in the folder to check if they are directories
        for element in folders_and_files:
            current_path = path.join(current_folder, element)
            if path.isdir(current_path):
                folders.add(current_path)
        # Return all the directories found in the current_folder
        return folders

    """
        The main function to run the directory search.

        :param starting_point: The starting point for the directory search.
        :return: None
    """
    def run_finder(self, starting_point=None):
        # If no starting point is provided, use the base_path as the starting point
        if starting_point is None:
            starting_point = self.base_path
        # List all the directories in the current folder
        folders = self._list_dirs(starting_point, listdir(starting_point))
        # If there are no more directories, add the current folder to the paths set
        if len(folders) == 0:
            self.paths.add(starting_point)
            return
        # For each directory found, call run_finder again with the directory as the new starting point
        for folder in folders:
            next_path = path.join(starting_point, folder)
            self.run_finder(starting_point=next_path)
