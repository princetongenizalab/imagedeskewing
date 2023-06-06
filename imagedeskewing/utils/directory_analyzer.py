import os
from collections import defaultdict


class DirectoryAnalyzer:
    """
    A class used to analyze the contents of a directory.

    ...

    Attributes
    ----------
    dir_path : str
        The path of the directory to analyze.

    Methods
    -------
    count_file_type(file_extension):
        Counts the number of files of a specific type in the directory and its subdirectories.
    count_all_file_types():
        Counts the frequency of each file type in the directory and its subdirectories.
    count_all_file_sizes_by_type():
        Counts the total disk file size of each file type in the directory and its subdirectories.
    """

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.file_types = defaultdict(int)
        self.file_sizes = defaultdict(int)
        self._populate_data()

    def _populate_data(self):
        for root, _, files in os.walk(self.dir_path):
            for file in files:
                _, extension = os.path.splitext(file)
                extension = extension.lower()

                self.file_types[extension] += 1
                self.file_sizes[extension] += os.path.getsize(os.path.join(root, file))

    def count_file_type(self, file_extension):
        return self.file_types[file_extension.lower()]

    def count_all_file_types(self):
        return dict(self.file_types)

    def count_all_file_sizes_by_type(self):
        return dict(self.file_sizes)


if __name__ == "__main__":
    print("This file is not meant to be run directly.")
