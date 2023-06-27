import argparse
import numpy as np

from bounding_box_generator import BoundingBoxGenerator
from instance_segmentation_generator import InstanceSegmentationGenerator
from utils.image import Image
from document_skew_estimator import calculate_skew_angle
from skimage.io import imsave

def deskew_image(image_path: str, output_path: str):
    """Deskew an image.

    Parameters
    ----------
    image_path : str
        The path to the image file to be deskewed.
    output_path : str
        The path to the output image file.
    """
    image = Image(image_path)

    #### TEMPORARY CODE ####
    grounding_dino_config_path = "/scratch/gpfs/eh0560/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
    grounding_dino_weight_path = "/scratch/gpfs/eh0560/imagedeskewing/models/grounding_dino_models/groundingdino_swint_ogc.pth"

    sam_checkpoint_path = "../../models/sam_models/sam_vit_h_4b8939.pth"
    model_type = "vit_h"

    text_prompt = "old brown paper"
    box_threshold = 0.50
    text_threshold = 0.25
    ########################

    bbg = BoundingBoxGenerator(grounding_dino_config_path, grounding_dino_weight_path)
    detections = bbg.find_objects(image.as_array(), text_prompt, box_threshold, text_threshold)

    isg = InstanceSegmentationGenerator(model_type, sam_checkpoint_path)
    detections.mask = isg.segment_objects(image.as_array(), detections.xyxy)

    # Flattening all the masks to a single mask.
    mask = np.any(detections.mask, axis=0)

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

def parse_args():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
