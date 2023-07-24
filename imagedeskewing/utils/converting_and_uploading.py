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
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def _load_image(path):
    return Image.open(path)


def _save_image_as_jpg(image, output_path, quality=90):
    image.save(output_path, 'JPEG', quality=quality, optimize=True)


def get_file_paths(root_dir, file_type):
    file_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(file_type):
                file_paths.append(os.path.join(root, file))
    return file_paths


def convert_path_to_output_path(path, output_dir, input_dir_prefix):
    file_path = path[len(input_dir_prefix):]
    if file_path.startswith('/'):
        file_path = file_path[1:]
    file_directory = os.path.dirname(file_path)
    file_name = os.path.basename(file_path).split('.')[0] + '.jpg'
    return os.path.join(output_dir, file_directory, file_name)


def convert_to_jpg(path, input_dir_prefix, output_dir='output'):
    image = _load_image(path)
    output_path = convert_path_to_output_path(path, output_dir, input_dir_prefix)
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    _save_image_as_jpg(image, output_path)


def main(file_type, input_dir='input', output_dir='output'):
    logger = setup_logger()
    start_time = time.time()
    logger.info(f'Searching {input_dir} for {file_type}\'s')
    file_paths = get_file_paths(input_dir, file_type)
    logger.info(f'Found {len(file_paths)} files')
    for path in file_paths:
        convert_to_jpg(path, input_dir, output_dir)
        logger.info(f'Converted {path}')
    logger.info(f'Finished in {time.time() - start_time} seconds')


if __name__ == '__main__':
    main('.tif', '/Volumes/NES_SCAD_Share/cairogeniza', '/Volumes/fileset-rustow/test_lab_move')