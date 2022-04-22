from unittest import TestCase
import climage
import random
import os


class RandomJudgePortrait(TestCase):
    def test_random_judge_portrait(self):
        """Can we show a random judge portrait"""
        file = random.choice(os.listdir("judge_pics/data/orig/"))
        fp = f"judge_pics/data/orig/{file}"
        print(climage.convert(fp, width=40))


if __name__ == "__main__":
    import unittest

    unittest.main()
