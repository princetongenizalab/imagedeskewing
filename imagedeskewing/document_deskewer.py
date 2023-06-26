import numpy as np

from deskew import determine_skew


def calculate_skew_angle(image: np.ndarray) -> float:
    """Calculate the skew angle of an image.

    Parameters
    ----------
    image : np.ndarray
        The image data in RGB format.

    Returns
    -------
    float
        The skew angle of the image in degrees.
    """
    return determine_skew(image)
