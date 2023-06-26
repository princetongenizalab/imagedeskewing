import torch
import numpy as np

from segment_anything import sam_model_registry, SamPredictor


class InstanceSegmentationGenerator:
    """
    A class used to generate instance segmentation masks for objects in images
    using detected bounding boxes.

    Attributes
    ----------
    device : torch.device
        The device to use for model prediction.
    model : SamPredictor
        The instance segmentation model.

    Methods
    -------
    segment_objects(image: np.ndarray, bounding_boxes: np.ndarray) -> np.ndarray
        Locate objects in an image and return the instance segmentation masks.
    """

    def __init__(self, sam_model_type: str, weight_path: str):
        """
        Parameters
        ----------
        sam_model_type : str
            The type of model to use for instance segmentation.
        weight_path : str
            The path to the weight file of the model.
        """
        self.device = self._get_device()
        self.model = self._load_model(sam_model_type, weight_path, self.device)

    @staticmethod
    def _get_device() -> torch.device:
        """Get the device available for torch."""
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    @staticmethod
    def _load_model(sam_model_type: str, weight_path: str, device: torch.device) -> SamPredictor:
        """Load the model."""
        sam = sam_model_registry[sam_model_type](checkpoint=weight_path).to(device=device)
        return SamPredictor(sam)

    def segment_objects(self, image: np.ndarray, bounding_boxes: np.ndarray) -> np.ndarray:
        """
        Locate objects in an image and return the instance segmentation masks.

        Parameters
        ----------
        image : np.ndarray
            The image data in RGB format.
        bounding_boxes : np.ndarray
            The bounding boxes of the objects in the image in the xyxy format.

        Returns
        -------
        np.ndarray
            The instance segmentation masks.
        """
        self.model.set_image(image)
        result_masks = []
        for box in bounding_boxes:
            masks, scores, logits = self.model.predict(
                box=box,
                multimask_output=True
            )
            index = np.argmax(scores)
            result_masks.append(masks[index])
        return np.array(result_masks)
