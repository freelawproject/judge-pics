from unittest import TestCase
import os

class JudgePicsTests(TestCase):

    def test_basic_import(self):
        """
        Basic test of getting json data loaded.
        """
        from judge_pics import judge_pics

    def test_judge_root_points_to_image_data(self):
        """
        Make sure we can get the path to the image files from the
        judge_root path given by judge_pics.
        """

        from judge_pics import judge_root
        dir_list = os.listdir(judge_root)

        for size in ('orig', '128', '256', '512'):
            assert size in dir_list


class JudgeScapersTests(TestCase):

    def test_basic_import(self):
        """
        Test if we can import the scrapers sub module.
        """
        from judge_pics import scrapers


if __name__ == '__main__':
    import unittest
    unittest.main()
