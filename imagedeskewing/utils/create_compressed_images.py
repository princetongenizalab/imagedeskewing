import os
import logging
from PIL import Image, UnidentifiedImageError
from multiprocessing import Pool, cpu_count
from datetime import datetime


def configure_logging():
    log_filename = datetime.now().strftime("logs/compress_and_resize_log_%Y%m%d_%H%M%S.log")
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging configured.")


def compress_and_resize(image_tuple):
    image_path, output_path, max_size, quality, format = image_tuple
    try:
        with Image.open(image_path) as img:
            aspect_ratio = img.width / img.height
            new_width = max_size if img.width > img.height else int(max_size * aspect_ratio)
            new_height = int(new_width / aspect_ratio) if img.width > img.height else max_size
            resized_img = img.resize((new_width, new_height), Image.Resampling.BICUBIC)
            resized_img.save(output_path, format=format, quality=quality)
            logging.info(f"Successfully resized and compressed {image_path}.")
    except FileNotFoundError:
        logging.error(f"Error: File {image_path} not found.")
    except UnidentifiedImageError:
        logging.error(f"Error: Unsupported image format in {image_path}.")
    except Exception as e:
        logging.error(f"Error: {e}.")


def main():
    configure_logging()
    input_folder = 'images/eve'
    output_folder = 'compressed_images/eve'
    max_size = 800
    quality = 90
    format = 'JPEG'
    Image.MAX_IMAGE_PIXELS = None

    if not os.path.exists(input_folder):
        logging.error(f"Error: Directory {input_folder} not found.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = os.listdir(input_folder)
    image_tuples = []
    for image in images:
        file_name = os.path.splitext(image)[0]
        file_extension = '.jpg'
        path = os.path.join(input_folder, image)
        output_path = os.path.join(output_folder, f"{file_name}_compressed{file_extension}")
        image_tuples.append((path, output_path, max_size, quality, format))

    logging.info("Starting image compression and resizing.")
    logging.info(f"Number of cores used: {cpu_count()}")
    with Pool(cpu_count()) as pool:
        pool.map(compress_and_resize, image_tuples)
    logging.info("Image compression and resizing completed.")


if __name__ == '__main__':
    main()

