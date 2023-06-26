import torch
import numpy as np

from groundingdino.util.inference import Model

from utils.image import Image


class BoundingBoxGenerator:
    """
    A class used to generate bounding boxes using GroundingDINO.

    Attributes
    ----------
    device : torch.device
        The device to use for model prediction.
    model : groundingdino.util.inference.Model
        The GroundingDINO model.

    Methods
    -------
    load_model(config_path: str, weight_path: str) -> None
        Load the GroundingDINO model.
    annotate_image(image_path: str, text_prompt: str, box_threshold: float, text_threshold: float) -> np.ndarray
        Load an image, generate bounding boxes, and annotate the detections.
    """

    def __init__(self, config_path: str, weight_path: str):
        """
        Parameters
        ----------
        config_path : str
            The path to the config file of the GroundingDINO model.
        weight_path : str
            The path to the weight file of the GroundingDINO model.
        """
        self.device = self._get_device()
        self.model = self._load_model(config_path, weight_path, self.device)

    @staticmethod
    def _get_device() -> torch.device:
        """Get the device available for torch."""
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    @staticmethod
    def _load_model(config_path: str, weight_path: str, device: torch.device) -> Model:
        """Load the GroundingDINO model."""
        return Model(model_config_path=config_path, model_checkpoint_path=weight_path, device=device)

    def annotate_image(self, image_path: str, text_prompt: str, box_threshold: float,
                       text_threshold: float) -> np.ndarray:
        """
        Load an image, generate bounding boxes, and annotate the detections.

        Parameters
        ----------
        image_path : str
            The path to the image file.
        text_prompt : str
            The text prompt for the prediction.
        box_threshold : float
            The box threshold for the prediction.
        text_threshold : float
            The text threshold for the prediction.

        Returns
        -------
        np.ndarray
            Annotated image with bounding boxes and segmentation annotations.
        """
        image = Image(image_path)
        detections, phrases = self.model.predict_with_caption(
            image=image,
            caption=text_prompt,
            box_threshold=box_threshold,
            text_threshold=text_threshold
        )

        print(detections)

        return None # TODO: Implement this

