import os
import unittest
from collections import defaultdict

from imagedeskewing.utils.directory_analyzer import DirectoryAnalyzer


class TestDirectoryAnalyzer(unittest.TestCase):

    def setUp(self):
        """
        Set up the testing environment before each test case.

        Create a test directory and set the file extensions to use for testing.
        """
        self.test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files")
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.test_file_extensions = [".txt", ".jpg", ".png"]

    def tearDown(self):
        """
        Clean up the testing environment after each test case.

        Remove the test directory.
        """
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def create_dummy_files(self, num_files, file_extension):
        """
        Create the specified number of dummy files with a specific extension in the test directory.

        Parameters
        ----------
        num_files : int
            The number of dummy files to create.
        file_extension : str
            The file extension for the dummy files. E.g., '.tiff'.
        """
        for i in range(num_files):
            with open(os.path.join(self.test_dir, f"dummy{i}{file_extension}"), "w") as f:
                f.write("This is a dummy file.")

    def test_count_file_type(self):
        """
        Test that the function counts the correct number of files.

        The function should correctly count the number of '.txt' files in the test directory.
        """
        num_files = 5
        self.create_dummy_files(num_files, self.test_file_extensions[0])

        analyzer = DirectoryAnalyzer(self.test_dir)
        txt_file_count = analyzer.count_file_type(self.test_file_extensions[0])
        self.assertEqual(txt_file_count, num_files, "The number of files counted is incorrect.")

    def test_count_file_type_no_files(self):
        """
        Test that the function counts zero when there are no files of the given type.

        The function should return 0 when counting the number of '.jpg' files in the test directory,
        since no '.jpg' files were created.
        """
        analyzer = DirectoryAnalyzer(self.test_dir)
        jpg_file_count = analyzer.count_file_type(".asdf")
        self.assertEqual(jpg_file_count, 0, "The number of files counted is incorrect.")

    def test_count_all_file_types(self):
        """
        Test that the function counts the correct number of files of all types.

        The function should correctly count the number of '.txt', '.jpg', and '.png' files in the test directory.
        """
        expected_counts = defaultdict(int)

        for extension in self.test_file_extensions:
            num_files = 5
            self.create_dummy_files(num_files, extension)
            expected_counts[extension] = num_files

        analyzer = DirectoryAnalyzer(self.test_dir)
        actual_counts = analyzer.count_all_file_types()
        self.assertEqual(actual_counts, expected_counts, "The number of files counted is incorrect.")

    def test_aggregate_files_by_type(self):
        """
        Test that the function aggregates the correct number of files of a given type.

        The function should correctly aggregate the '.txt' files in the test directory.
        """
        num_files = 5
        self.create_dummy_files(num_files, self.test_file_extensions[0])

        analyzer = DirectoryAnalyzer(self.test_dir)
        txt_files = analyzer.aggregate_files_by_type(self.test_dir, "txt")
        self.assertEqual(len(txt_files), num_files, "The number of files aggregated is incorrect.")


if __name__ == "__main__":
    unittest.main()
