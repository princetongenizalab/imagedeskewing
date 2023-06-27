import os
from typing import Dict
from collections import defaultdict


class DirectoryAnalyzer:
    """
    The DirectoryAnalyzer class provides methods to analyze and summarize
    the contents of a specific directory, including file type and file size.

    Attributes
    ----------
    dir_path : str
        The path of the directory to analyze.
    file_types : defaultdict[int]
        A defaultdict to hold the count of each file type in the directory.
    file_sizes : defaultdict[int]
        A defaultdict to hold the total size of each file type in the directory.

    Methods
    -------
    count_file_type(file_extension: str) -> int:
        Returns the count of files with a specific file type(extension) in the directory and its subdirectories.
    count_all_file_types() -> Dict[str, int]:
        Returns a dictionary containing the count of each file type in the directory and its subdirectories.
    count_all_file_sizes_by_type() -> Dict[str, int]:
        Returns a dictionary containing the total disk file size (in bytes) of each file type in the directory
        and its subdirectories.
    """

    def __init__(self, dir_path: str):
        """
        Parameters
        ----------
        dir_path : str
            The path of the directory to analyze.
        """
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(f"{dir_path} is not a directory.")
        self.dir_path = dir_path
        self.file_types = defaultdict(int)
        self.file_sizes = defaultdict(int)
        self._populate_data()

    def _populate_data(self):
        """
        Populates the file_types and file_sizes attributes with data from
        the directory and its subdirectories.
        """
        for root, _, files in os.walk(self.dir_path):
            for file in files:
                _, extension = os.path.splitext(file)
                extension = extension.lower()

                self.file_types[extension] += 1
                self.file_sizes[extension] += os.path.getsize(os.path.join(root, file))

    def count_file_type(self, file_extension: str) -> int:
        """
        Returns the count of files with a specific file type(extension) in the directory and its subdirectories.

        Parameters
        ----------
        file_extension : str
            The file extension to count.

        Returns
        -------
        int
            The count of files with the specified extension.
        """
        return self.file_types[file_extension.lower()]

    def count_all_file_types(self) -> Dict[str, int]:
        """
        Returns a dictionary containing the count of each file type in the directory and its subdirectories.

        Returns
        -------
        Dict[str, int]
            A dictionary where the keys are the file extensions and the values are their respective counts.
        """
        return dict(self.file_types)

    def count_all_file_sizes_by_type(self) -> Dict[str, int]:
        """
        Returns a dictionary containing the total disk file size (in bytes) of each file type in the directory
        and its subdirectories.

        Returns
        -------
        Dict[str, int]
            A dictionary where the keys are the file extensions and the values are the total size of files
            with that extension.
        """
        return dict(self.file_sizes)
