import unittest
import decimal

from decimilify import decimilify

class DecimilifyTest(unittest.TestCase):
    def test_decimilify(self):
        d = {
                "z": 0.25,
                "a": 1,
                "b": "2",
                "c": 1.23,
                "d": [
                    1.25,
                    1,
                    1,42,
                    4
                ],
                "e": {
                    "a": 1.2,
                    "b": [
                        "one",
                        "two",
                        "tree"
                    ]
                }
        }
        test_d = {
                "z": decimal.Decimal(0.25),
                "a": 1,
                "b": "2",
                "c": decimal.Decimal(1.23),
                "d": [
                    decimal.Decimal(1.25),
                    1,
                    decimal.Decimal(1.42),
                    4
                ],
                "e": {
                    "a": decimal.Decimal(1.2),
                    "b": [
                        "one",
                        "two",
                        "tree"
                    ]
                }
        }
        new_d = decimilify(d)
        self.assertTrue(new_d, test_d)
