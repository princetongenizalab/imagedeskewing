import subprocess
import logging
from logging.handlers import RotatingFileHandler
import concurrent.futures
import csv


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


def download_file(remote_host, file_path, local_path):
    """
    Download a file from the SMB share.

    Parameters
    ----------
    remote_host : str
        Path to the remote host to download the file from.
    file_path : str
        Path to the file to transfer.
    local_path : str
        Path to the save the file to locally.
    """
    logger = logging.getLogger(__name__)
    command = (f'smbclient {remote_host} -A smbcredentials -c'
               f' "get {file_path} {local_path}"')
    try:
        process = subprocess.run(command, shell=True, check=True, timeout=120, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        logger.error(f"Error occurred while transferring {file_path}: {str(error)}")
    except subprocess.TimeoutExpired:
        logger.error(f"Transfer of {file_path} timed out")
    except Exception as error:
        logger.error(f"An unexpected error occurred while transferring {file_path}: {str(error)}")

    if process.stdout:
        stdout = process.stdout.decode("utf-8")
        logger.info(f"command output for file {file_path} - {stdout}")


def download_all_files(remote_path, csv_file_path):
    """
    Read file paths from a CSV file and download each file.

    Parameters
    ----------
    remote_path : str
        Path to the remote host to download the files from.
    csv_file_path : str
        Path to the CSV file containing file paths to download.
    """
    logger = logging.getLogger(__name__)
    jobs = []
    with open(csv_file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for row in reader:
                file_path = row[0]  # The first column in the CSV file contains the file path
                output_path = row[6]
                drive_letter, rest_of_path = file_path.split(":", 1)
                rest_of_path = rest_of_path.lstrip("\\")
                file_path = rest_of_path.replace("\\", "/")
                logger.info(f"Downloading file {file_path}")
                executor.submit(download_file, remote_path, file_path, output_path)


if __name__ == "__main__":
    setup_logger()
    logger = logging.getLogger(__name__)
    try:
        download_all_files("//lockhart.princeton.edu/NES_SCAD_Share", "data/eve_index_cleaned.csv")
    except OSError as e:
        logger.error(f"Invalid directory or insufficient permissions: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
