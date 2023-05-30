import os
from collections import defaultdict


def count_file_type(dir_path, file_extension):
    """
    Counts the number of files of a specific type in a directory and its subdirectories.

    This function walks through each directory and subdirectory in the given path,
    counting the number of files with the specified file extension.

    Parameters
    ----------
    dir_path : str
        The path of the directory to search in.
    file_extension : str
        The file extension to count. E.g., '.tiff'.

    Returns
    -------
    int
        The number of files with the specified extension in the directory and its subdirectories.

    Examples
    --------
    >>> path = "/path/to/your/directory"
    >>> extension = ".tiff"
    >>> print(count_file_type(path, extension))
    5
    """

    count = 0

    for _, _, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(file_extension.lower()):
                count += 1

    return count


def count_all_file_types(dir_path):
    """
    Recursively traverses the input directory and counts the frequency of each file type.

    Parameters
    ----------
    dir_path : str
        The path of the directory to search in.

    Returns
    -------
    dict
        A dictionary with the file extensions as keys and their counts as values.

    Examples
    --------
    >>> path = "/path/to/your/directory"
    >>> print(count_all_file_types(path))
    {'.tiff': 5, '.png': 2, '.txt': 10}
    """
    count = defaultdict(int)

    for _, _, files in os.walk(dir_path):
        for file in files:
            _, extension = os.path.splitext(file)
            count[extension.lower()] += 1

    return count


if __name__ == "__main__":
    print("This file is not meant to be run directly.")
