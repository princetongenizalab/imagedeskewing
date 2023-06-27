import os
import numpy as np
from skimage.transform import rotate
from skimage.io import imread
from skimage.util import img_as_ubyte

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
    rotated(angle: float) -> np.ndarray
        Returns a rotated version of the image.
    get_height() -> int
        Returns the height of the image.
    get_width() -> int
        Returns the width of the image.
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

    def get_height(self) -> int:
        """
        Get the height of the image.

        Returns
        -------
        int
            The height of the image.
        """
        return self.image.shape[0]

    def get_width(self) -> int:
        """
        Get the width of the image.

        Returns
        -------
        int
            The width of the image.
        """
        return self.image.shape[1]

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

        image = imread(self.path)

        if image.ndim == 2:
            image = np.stack((image, image, image), axis=-1)
        elif image.ndim == 3 and image.shape[-1] == 4:
            image = image[:, :, :3]

        return image

    def as_array(self) -> np.ndarray:
        """
        Get the loaded image data as a numpy array.

        Returns
        -------
        np.ndarray
            Image data in RGB format.
        """
        return self.image

    def rotated(self, angle: float) -> np.ndarray:
        """
        Returns a rotated version of the image.

        Parameters
        ----------
        angle : float
            The angle to rotate the image by in degrees where an angle > 0 rotates the image counter-clockwise and
            an angle < 0 rotates the image clockwise.

        Returns
        -------
        np.ndarray
            The rotated image data.
        """
        rotated = rotate(self.image, angle, resize=True)
        return img_as_ubyte(rotated)
