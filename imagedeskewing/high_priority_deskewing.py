import os
import sys

import numpy as np
import pandas as pd

from bounding_box_generator import BoundingBoxGenerator
from instance_segmentation_generator import InstanceSegmentationGenerator
from utils.image import Image
from skimage.io import imsave


from deskew import determine_skew

def find_images(directory, extension):
    """
    Returns the abs path to all files with a specified extension in a parent directory.

    Parameters
    ----------
    directory : str
        The parent directory to search for the files.
    extension : str
        The extension of the files to be found.

    Returns
    -------
    images : list
        The list of absolute paths to the found files.
    """
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                images.append(file_path)
    return images


def calculate_skew_angle(image: np.ndarray) -> float:
    """Calculate the skew angle of an image.

    Parameters
    ----------
    image : np.ndarray
        The image data in RGB format.

    Returns
    -------
    float
        The skew angle of the image in degrees where an angle > 0 is a counter-clockwise rotation and an angle < 0 is a
        clockwise rotation.
    """
    return determine_skew(image, min_deviation=0.025, num_peaks=100)


def deskew_image(image_path: str, output_path: str, bbg, isg):
    image = Image(image_path)

    text_prompt = "old brown paper"
    box_threshold = 0.50
    text_threshold = 0.25

    detections = bbg.find_objects(image.as_array(), text_prompt, box_threshold, text_threshold)
    detections.mask = isg.segment_objects(image.as_array(), detections.xyxy)

    if (not detections.mask):
        imsave(output_path, image.as_array())
        return 0

    # Flattening all the masks to a single mask.
    mask = np.any(detections.mask, axis=0)

    print(mask)

    # Computing the smallest bounding box that contains all the masks.
    x0 = int(detections.xyxy[:, 0].min())
    y0 = int(detections.xyxy[:, 1].min())
    x1 = int(detections.xyxy[:, 2].max())
    y1 = int(detections.xyxy[:, 3].max())

    # Adding padding so the image is not cropped too tightly.
    # Found that this improves the accuracy of the skew angle estimation.
    padding = 20
    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(image.get_width(), x1 + padding)
    y1 = min(image.get_height(), y1 + padding)

    cropped_image = image.as_array()[y0:y1, x0:x1]

    skew_angle = calculate_skew_angle(cropped_image)

    imsave(output_path, image.rotated(skew_angle))

    return skew_angle


def main():
    images = find_images("/scratch/gpfs/RUSTOW/htr_deskewing_image_dataset", ".tif")

    grounding_dino_config_path = "/scratch/gpfs/eh0560/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
    grounding_dino_weight_path = "/scratch/gpfs/eh0560/imagedeskewing/models/grounding_dino_models/groundingdino_swint_ogc.pth"

    sam_checkpoint_path = "../../models/sam_models/sam_vit_h_4b8939.pth"
    model_type = "vit_h"

    bbg = BoundingBoxGenerator(grounding_dino_config_path, grounding_dino_weight_path)
    isg = InstanceSegmentationGenerator(model_type, sam_checkpoint_path)

    output_directory = "/scratch/gpfs/RUSTOW/deskewed_htr_dataset/"
    output_paths = []
    for image_path in images:
        output_path = output_directory + image_path.replace("/scratch/gpfs/RUSTOW/htr_deskewing_image_dataset/", "", 1)
        output_path = output_path.split(".tif")[0] + ".jpg"
        output_paths.append(output_path)

    angles = {}
    for input_image_path, output_image_path in zip(images, output_paths):
        dir_name = os.path.dirname(output_image_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        angle = deskew_image(input_image_path, output_image_path, bbg, isg)
        angles[input_image_path] = angle

    df = pd.DataFrame(angles)
    df.to_csv("angles.csv", index=False)