import os
import argparse
from PIL import Image


class BatchConvert:
    """
    A class used to batch convert image types

    Parameters
    ----------
    input_dir : str
        The directory path where the images are located
    recursive : bool
        A flag used to determine whether to recursively search through subdirectories

    Methods
    -------
    convert_images(input_format, output_format, quality)
        Converts all images of a specified format in the directory to another format with specific quality.
    """

    def __init__(self, input_dir, recursive=False):
        """
        Parameters
        ----------
        input_dir : str
            The directory where the images are located
        recursive : bool, optional
            A flag to determine whether to recursively search through subdirectories (default is False)
        """
        self.input_dir = input_dir
        self.recursive = recursive

    def convert_images(self, input_format, output_format, quality=90):
        """
        Converts all images of a specified format in the directory to another format with specific quality

        Parameters
        ----------
        input_format : str
            The image format to convert from
        output_format : str
            The image format to convert to
        quality : int, optional
            The quality of the output images (default is 90)
        """
        for root, dirs, files in os.walk(self.input_dir):
            for file in files:
                if file.lower().endswith('.' + input_format.lower()):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(root, file.rsplit('.', 1)[0] + '.' + output_format)
                    img = Image.open(input_file)
                    img.save(output_file, output_format.upper(), quality=quality)

            # Only search through subdirectories if recursive flag is set
            if not self.recursive:
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch convert image types')
    parser.add_argument('--input_dir', required=True, help='Input directory containing images')
    parser.add_argument('--recursive', action='store_true', help='Recursively search through subdirectories')
    parser.add_argument('--input_format', required=True, help='Image format to convert from')
    parser.add_argument('--output_format', required=True, help='Image format to convert to')
    parser.add_argument('--quality', type=int, default=90, help='Quality of output images')

    args = parser.parse_args()

    converter = BatchConvert(args.input_dir, args.recursive)
    converter.convert_images(args.input_format, args.output_format, args.quality)
