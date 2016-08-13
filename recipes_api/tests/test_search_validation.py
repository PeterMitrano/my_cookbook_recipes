import json
import logging
import os
import random
import unittest

from recipes_api.search.get import lambda_function as get_search
from recipes_api.tests import test_util


logging.getLogger('nose').setLevel(logging.WARNING)


class ValidationTest(unittest.TestCase):
    def make_event(self, recipe_id):
        return {"params": {"querystring": {"keywords": str(recipe_id)}}}

    def test_str(self):
        event = self.make_event('pancakes')
        response = get_search.handle_event(event, None)
        self.assertGreaterEqual(response['code'], 0)

    def test_int(self):
        for i in range(-100, 100, 10):
            event = self.make_event(i)
            response = get_search.handle_event(event, None)
            self.assertLess(response['code'], 0)
            self.assertEqual(type(response['data']), str)

    def test_float(self):
        for i in range(10):
            recipe_id = random.random() * 100 - 50
            event = self.make_event(recipe_id)
            response = get_search.handle_event(event, None)
            self.assertLess(response['code'], 0)
            self.assertEqual(type(response['data']), str)

    def test_json(self):
        j = json.dumps({'evil': 'input_dict'})
        event = self.make_event(j)
        response = get_search.handle_event(event, None)
        self.assertLess(response['code'], 0)
        self.assertEqual(type(response['data']), str)
