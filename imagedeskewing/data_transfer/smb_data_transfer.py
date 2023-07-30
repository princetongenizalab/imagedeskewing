import subprocess
import logging
from logging.handlers import RotatingFileHandler
import concurrent.futures
import csv
from pathlib import Path


def setup_logger():
    """
    Setup a logger for the script.

    Setup a logger for the script that logs to both the console and a file. The log file is rotated when it reaches
    200MB and 5 backups are kept.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler("smb_transfer.log", maxBytes=200000000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def download_file(remote_path, file_path):
    """
    Download a file from the SMB share.

    Parameters
    ----------
    remote_path : str
        Path to the remote directory to transfer the file to.
    file_path : str
        Path to the file to transfer.
    """
    logger = logging.getLogger(__name__)
    command = (f'smbclient {remote_path} -A smbcredentials -c'
               f' "get {file_path} {file_path}"')
    try:
        subprocess.run(command, shell=True, check=True, timeout=120)
    except subprocess.CalledProcessError as error:
        logger.error(f"Error occurred while transferring {file_path}: {str(error)}")
    except subprocess.TimeoutExpired:
        logger.error(f"Transfer of {file_path} timed out")
    except Exception as error:
        logger.error(f"An unexpected error occurred while transferring {file_path}: {str(error)}")


def download_all_files(remote_path, csv_file_path):
    """
    Read file paths from a CSV file and download each file.

    Parameters
    ----------
    remote_path : str
        Path to the remote directory to transfer the files to.
    csv_file_path : str
        Path to the CSV file containing file paths to download.
    """
    logger = logging.getLogger(__name__)
    with open(csv_file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for row in reader:
                file_path = row[0] # The first column in the CSV file contains the file path
                drive_letter, rest_of_path = file_path.split(":", 1)
                rest_of_path = rest_of_path.lstrip("\\")
                file_path = Path(rest_of_path)
                logger.info(f"Downloading file {file_path}")
                executor.submit(download_file, remote_path, str(file_path))


if __name__ == "__main__":
    setup_logger()
    logger = logging.getLogger(__name__)
    try:
        download_all_files("//path.to.remote/share", "/path/to/your/csvfile.csv")
    except OSError as e:
        logger.error(f"Invalid directory or insufficient permissions: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
