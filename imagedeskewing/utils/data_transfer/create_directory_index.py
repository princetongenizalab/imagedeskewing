import os
import pandas as pd


def create_file_index(directory):
    """Create a pandas dataframe with file information for all files in a parent directory.

    Recursively walks through all subdirectories and returns a dataframe with all files in the parent directory.
    Creates a pandas dataframe with the following columns:
    - file_path
    - file_name
    - file_extension
    - file_size
    - file_last_modified
    - file_created

    Parameters
    ----------
    directory : str
        Parent directory to walk through and create a dataframe of all files.

    Returns
    -------
    df : pandas dataframe
        Dataframe with all files in the parent directory.
    """
    files = []
    for root, directories, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    df = pd.DataFrame(files, columns=["file_path"])

    df["file_name"] = df["file_path"].apply(lambda x: os.path.basename(x))
    df["file_extension"] = df["file_path"].apply(lambda x: os.path.splitext(x)[1])
    df["file_size"] = df["file_path"].apply(lambda x: os.path.getsize(x))
    df["file_last_modified"] = df["file_path"].apply(lambda x: os.path.getmtime(x))
    df["file_created"] = df["file_path"].apply(lambda x: os.path.getctime(x))

    return df


if __name__ == '__main__':
    directory = r"Z:\cairogeniza"
    df = create_file_index(directory)
    df.to_csv("index.csv", index=False)
    
