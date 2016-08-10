import logging
import random
import unittest

from recipes_api.recipes.get import lambda_function

logging.getLogger('nose').setLevel(logging.WARNING)

CONTEXT = {"debug": True}

class ValidationTest(unittest.TestCase):
    def make_event(self, recipe_id):
        return {
            "params": {
                "querystring": {
                    "id": str(recipe_id)
                }
            }
        }

    def test_valid_int(self):
        for i in range(0, 100, 5):
            logging.getLogger("TEST").info(i)
            event = self.make_event(i)
            response = lambda_function.handle_event(event, CONTEXT)
            self.assertGreaterEqual(response['code'], 0)

    def test_invalid_int(self):
        for i in range(-100, -1, 5):
            logging.getLogger("TEST").info(i)
            event = self.make_event(i)
            response = lambda_function.handle_event(event, CONTEXT)
            self.assertLess(response['code'], 0)
            self.assertEqual(type(response['data']), str)

    def test_float(self):
        for i in range(10):
            recipe_id = random.random() * 100 - 50
            event = self.make_event(recipe_id)
            response = lambda_function.handle_event(event, CONTEXT)
            self.assertLess(response['code'], 0)
            self.assertEqual(type(response['data']), str)

