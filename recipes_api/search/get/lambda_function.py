import boto3
from fuzzywuzzy import fuzz
import json
import logging

from recipes_api.common import stage

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

GOOD_ENOUGH_RATIO = 50


def could_be_number(x):
    try:
        int(x)
        float(x)
        return True
    except ValueError:
        return False


def could_be_dict(x):
    try:
        json.loads(x)
        return True
    except ValueError:
        return False


def handle_event(event, context):

    # parse the recipe id from the parameters
    try:
        recipe_keywords = event['params']['querystring']['keywords']

        # basic input validation
        if could_be_number(recipe_keywords):
            return {"code": -1, "data": "recipe name cannot be a number"}
        if could_be_dict(recipe_keywords):
            return {"code": -1, "data": "recipe name cannot be json/a dict"}

        # connect to database
        if stage.PROD:
            resource = boto3.resource("dynamodb")
        else:
            resource = boto3.resource(
                "dynamodb",
                endpoint_url="http://localhost:8000",
                aws_access_key_id="fake",
                aws_secret_access_key="fake",
                region_name="us-east-1")

        table = resource.Table('my_cookbook_recipes')
        response = table.scan()

        http_code = response['ResponseMetadata']['HTTPStatusCode']
        if http_code != 200:
            return {"code": -1, "data": "failed to scan recipes table"}

        # The simplest thing we can do right now is a fuzzy match
        matching_items = []
        for item in response['Items']:
            recipe_name = item['name']
            ratio = fuzz.partial_token_set_ratio(recipe_keywords, recipe_name)
            if ratio < GOOD_ENOUGH_RATIO:
                matching_items.append(item)

        return {"code": 0, "data": matching_items}

    except KeyError:
        return {"code": -1,
                "data": "Failed to parse query prameter 'keywords'"}
