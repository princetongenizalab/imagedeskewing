import cv2


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
    load_image()
        Loads the image from path.

    get_image() -> np.ndarray
        Returns the image data.
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

    def load_image(self):
        """
        Load the image using OpenCV (cv2) library, and convert it to RGB format.

        Returns
        -------
        np.ndarray
            Image data in RGB format.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        """
        try:
            image = cv2.imread(self.path)

            # Convert the image from BGR to RGB format
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            return image_rgb

        except FileNotFoundError:
            print(f"The specified image file {self.path} was not found.")

    def get_image(self) -> "np.ndarray":
        """
        Get the loaded image data.

        Returns
        -------
        np.ndarray
            Image data in RGB format.
        """
        return self.image
