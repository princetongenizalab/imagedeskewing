import os
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import concurrent.futures

def setup_logger():
    """
    Setup a logger for the script.

    Setup a logger for the script that logs to both the console and a file. The log file is rotated when it reaches
    200MB and 5 backups are kept.

    Returns
    -------
    logger : logging.Logger
        Logger for the script.
    """
    logger = logging.getLogger('smb_transfer')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler('smb_transfer.log', maxBytes=200000000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def transfer_file(file_path, logger):
    """
    Transfer a file to the SMB share.

    Parameters
    ----------
    file_path : str
        Path to the file to transfer.
    logger : logging.Logger
        Logger for the script.
    """
    command = (f'smbclient //172.19.70.125/NES_SCAD_Share -A smbcredentials -c'
               f' "get {file_path} {file_path}"')
    try:
        subprocess.run(command, shell=True, check=True, timeout=120)
    except subprocess.CalledProcessError as error:
        logger.error(f'Error occurred while transferring {file_path}: {str(error)}')
    except subprocess.TimeoutExpired:
        logger.error(f'Transfer of {file_path} timed out')
    except Exception as error:
        logger.error(f'An unexpected error occurred while transferring {file_path}: {str(error)}')


def traverse_directory_and_transfer(directory_path, logger):
    """
    Traverse a directory and transfer all files to the SMB share.

    Parameters
    ----------
    directory_path : str
        Path to the directory to traverse.
    logger : logging.Logger
        Logger for the script.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                full_file_path = os.path.join(root, file)
                logger.info(f'Transferring file {full_file_path}')
                executor.submit(transfer_file, full_file_path, logger)


if __name__ == "__main__":
    logger = setup_logger()
    try:
        traverse_directory_and_transfer("/path/to/your/directory", logger)
    except OSError as e:
        logger.error(f'Invalid directory or insufficient permissions: {str(e)}')
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
