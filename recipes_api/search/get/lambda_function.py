import boto3
from fuzzywuzzy import fuzz
import json
import logging
import os

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

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
        if 'DEBUG' in os.environ:
            resource = boto3.resource(
                "dynamodb",
                endpoint_url="http://localhost:8000",
                aws_access_key_id="fake",
                aws_secret_access_key="fake",
                region_name="us-east-1")
        else:
            resource = boto3.resource("dynamodb")

        table = resource.Table('my_cookbook_recipes')
        response = table.scan()

        # The simplest thing we can do right now is a fuzzy match
        fuzz.partial_token_set_ratio(recipe_keywords, item)

        return {"code": 0, "data": recipe_keywords}

    except KeyError:
        return {"code": -1, "data": "Failed to parse query prameter 'keywords'"}
