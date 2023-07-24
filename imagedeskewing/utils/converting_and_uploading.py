import logging
import time
import os
from PIL import Image


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler(f'logs/{time.strftime("%Y%m%d-%H%M%S")}.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    steam_handler = logging.StreamHandler()
    steam_handler.setFormatter(formatter)
    logger.addHandler(steam_handler)
    return logger


def _load_image(path):
    return Image.open(path)


def _save_image_as_jpg(image, output_path, quality=80):
    image.save(output_path, 'JPEG', quality=quality, optimize=True)


def get_file_paths(root_dir):
    file_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def convert_path_to_output_path(path, output_dir):
    return os.path.join(output_dir, os.path.dirname(path), os.path.basename(path).split('.')[0] + '.jpg'

def convert_to_jpg(path, output_dir='output'):
    image = _load_image(path)
    output_path = convert_path_to_output_path(path, output_dir)
    _save_image_as_jpg(image, output_path)


def main(input_dir='input', output_dir='output'):
    logger = setup_logger()
    start_time = time.time()
    file_paths = get_file_paths(input_dir)
    logger.info(f'Found {len(file_paths)} files')
    for path in file_paths:
        convert_to_jpg(path, output_dir)
        logger.info(f'Converted {path}')
    logger.info(f'Finished in {time.time() - start_time} seconds')


if __name__ == '__main__':
    main()