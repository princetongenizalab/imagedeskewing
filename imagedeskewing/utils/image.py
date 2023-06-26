import os
import cv2
import numpy as np
from skimage.transform import rotate

class Image:
    """
    Image class for loading and handling image data.

    Attributes
    ----------
    path : str
        Path to the image file.
    image : np.ndarray
        Image data in RGB format.

    Methods
    -------
    load_image() -> np.ndarray
        Loads the image from path.
    as_array() -> np.ndarray
        Returns the image data as a numpy array.
    """

    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            The path to the image file to be loaded.
        """
        self.path = path
        self.image = self.load_image()

    def load_image(self) -> np.ndarray:
        """
        Load the image from path and convert it to RGB format.

        Returns
        -------
        np.ndarray
            Image data in RGB format.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"The specified image file {self.path} was not found.")

        image = cv2.imread(self.path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image_rgb

    def as_array(self) -> np.ndarray:
        """
        Get the loaded image data as a numpy array.

        Returns
        -------
        np.ndarray
            Image data in RGB format.
        """
        return self.image

    def rotate(self, angle: float) -> np.ndarray:
        """
        Rotate the image by the specified angle.

        Parameters
        ----------
        angle : float
            The angle to rotate the image by in degrees.

        Returns
        -------
        np.ndarray
            The rotated image data.
        """
        return rotate(self.image, angle, resize=True)
