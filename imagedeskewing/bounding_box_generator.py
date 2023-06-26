import numpy as np
import torch
import supervision as sv

from groundingdino.util.inference import Model


class BoundingBoxGenerator:
    """
    A class used to generate bounding boxes for objects in images.

    Attributes
    ----------
    device : torch.device
        The device to use for model prediction.
    model : groundingdino.util.inference.Model
        The GroundingDINO model.

    Methods
    -------
    find_objects(image_path: str, text_prompt: str, box_threshold: float, text_threshold: float) -> sv.Detections
        Locate objects in an image and return the bounding boxes.
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

    def find_objects(self, image: np.ndarray, text_prompt: str, box_threshold: float,
                     text_threshold: float) -> sv.Detections:
        """
        Locate objects in an image and return the bounding boxes.

        Parameters
        ----------
        image : np.ndarray
            The image data in RGB format.
        text_prompt : str
            The text prompt for the prediction. This can be a series of phrases separated by a comma or a single phrase.
        box_threshold : float
            The box threshold for the prediction. This is the confidence threshold for the bounding boxes.
        text_threshold : float
            The text threshold for the prediction. This is the similarity confidence threshold for the
            words to use as the labels.

        Returns
        -------
        sv.Detections
            Detections object containing the bounding boxes in xyxy format and confidence scores.
        """
        detections, phrases = self.model.predict_with_caption(
            image=image,
            caption=text_prompt,
            box_threshold=box_threshold,
            text_threshold=text_threshold
        )

        return detections
