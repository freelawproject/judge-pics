from unittest import TestCase
import climage
import random
import os


class JudgePicsTests(TestCase):
    def test_basic_import(self):
        """
        Basic test of getting json data loaded.
        """
        from judge_pics import judge_pics


class JudgeScapersTests(TestCase):
    def test_basic_import(self):
        """
        Test if we can import the scrapers sub module.
        """
        from judge_pics.scrapers import cand_judges


class RandomJudgePortrait(TestCase):

    def test_random_judge_portrait(self):
        """Can we show a random judge portrait"""
        file = random.choice(
            os.listdir("judge_pics/data/orig/"))
        fp = f"judge_pics/data/orig/{file}"
        print(climage.convert(fp))


if __name__ == "__main__":
    import unittest

    unittest.main()
