import os
import unittest
from imagedeskewing.utils.count_files import count_file_type


class TestCountFiles(unittest.TestCase):
    def setUp(self):
        """
        Set up the testing environment before each test case.

        Create a test directory and set the file extension to use for testing.
        """
        self.test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files")
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.test_file_extension = ".txt"

    def tearDown(self):
        """
        Clean up the testing environment after each test case.

        Remove the test directory.
        """
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def create_dummy_files(self, num_files):
        """
        Create the specified number of dummy files in the test directory.

        Parameters
        ----------
        num_files : int
            The number of dummy files to create.
        """
        for i in range(num_files):
            with open(os.path.join(self.test_dir, f"dummy{i}{self.test_file_extension}"), 'w') as f:
                f.write("This is a dummy file.")

    def test_count_file_type(self):
        """
        Test that the function counts the correct number of files.

        The function should correctly count the number of '.txt' files in the test directory.
        """
        num_files = 5
        self.create_dummy_files(num_files)

        txt_file_count = count_file_type(self.test_dir, self.test_file_extension)
        self.assertEqual(txt_file_count, num_files)

    def test_count_file_type_no_files(self):
        """
        Test that the function counts zero when there are no files of the given type.

        The function should return 0 when counting the number of '.jpg' files in the test directory,
        since no '.jpg' files were created.
        """
        jpg_file_count = count_file_type(self.test_dir, ".jpg")
        self.assertEqual(jpg_file_count, 0)


if __name__ == "__main__":
    unittest.main()
