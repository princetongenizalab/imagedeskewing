import unittest
import numpy as np
import cv2
from pathlib import Path
from imagedeskewing.utils.image import Image


class TestImage(unittest.TestCase):

    def setUp(self):
        """
        Creates a temporary RGB image file for testing.
        """
        self.temp_image_path = str(Path(__file__).parent / "temp_image.png")

        width = 128
        height = 128
        red_channel = np.linspace(np.linspace(0, 255, width), np.linspace(0, 255, width), height, dtype=int)[:, :, None]
        green_channel = np.linspace(np.linspace(0, 0, width), np.linspace(255, 0, width), height, dtype=int)[:, :, None]
        blue_channel = np.linspace(np.linspace(255, 255, width), np.linspace(0, 0, width), height, dtype=int)[:, :,None]
        self.temp_image = np.concatenate([red_channel, green_channel, blue_channel], axis=2)

        bgr_image = cv2.cvtColor(self.temp_image.astype(np.uint8), cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.temp_image_path, bgr_image)

    def tearDown(self):
        """
        Removes the temporary image file after testing.
        """
        Path(self.temp_image_path).unlink()

    def test_load_image(self):
        """
        Tests the load_image method of the Image class.
        """
        image = Image(self.temp_image_path)
        self.assertTrue(np.array_equal(image.image, self.temp_image), "Loaded image does not match the original.")

    def test_as_array(self):
        """
        Tests the as_array method of the Image class.
        """
        image = Image(self.temp_image_path)
        self.assertTrue(np.array_equal(image.as_array(), image.image), "Returned image does not match the stored one.")

    def test_load_non_existent_image(self):
        """
        Tests the handling of a non-existent image file.
        """
        with self.assertRaises(FileNotFoundError):
            Image("non_existent.jpg")


if __name__ == "__main__":
    unittest.main()
