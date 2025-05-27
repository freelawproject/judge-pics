from unittest import TestCase

from judge_pics.search import ImageSizes, portrait, query, show


class QueryTests(TestCase):
    def test_found_confident(self):
        result = query("Vadas Nandor", ImageSizes.SMALL.value)
        self.assertEqual(
            result,
            ["https://portraits.free.law/v2/128/vadas-nandor.jpeg"],
        )

    def test_found_not_confident(self):
        result = query("A", ImageSizes.LARGE.value)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_not_found(self):
        result = query("", ImageSizes.SMALL.value)
        self.assertEqual(result, [])


class PortraitTests(TestCase):
    def test_int_found(self):
        result = portrait(10156, ImageSizes.SMALL)
        self.assertEqual(
            result,
            "https://portraits.free.law/v2/128/vadas-nandor.jpeg",
        )

    def test_int_found_large(self):
        result = portrait(10156, ImageSizes.LARGE)
        self.assertEqual(
            result,
            "https://portraits.free.law/v2/512/vadas-nandor.jpeg",
        )

    def test_int_not_found(self):
        result = portrait(-1, ImageSizes.SMALL)
        self.assertIsNone(result)

    def test_str_found(self):
        result = portrait("Vadas Nandor", ImageSizes.SMALL)
        self.assertEqual(
            result,
            "https://portraits.free.law/v2/128/vadas-nandor.jpeg",
        )

    def test_str_not_found(self):
        result = portrait("", ImageSizes.SMALL)
        self.assertIsNone(result)


class ShowTests(TestCase):
    def test_show(self):
        result = show(10156, ImageSizes.SMALL)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("\x1b[48;5;234m"))


if __name__ == "__main__":
    import unittest

    unittest.main()
