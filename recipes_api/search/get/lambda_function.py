import boto3
import json
import logging

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)


def handle_event(event, context):

    # parse the recipe id from the parameters
    try:
        recipe_id = event['params']['querystring']['keywords']

        # connect to database
        if "debug" in context:
            resource = boto3.resource(
                "dynamodb",
                endpoint_url="http://localhost:8000",
                aws_access_key_id="fake",
                aws_secret_access_key="fake",
                region_name="us-east-1")
        else:
            resource = boto3.resource("dynamodb")

        table = resource.Table('my_cookbook_recipes')

        #pretend to do stuff...
        return {"code": 0, "data": "no recipes for you fool!"}

    except KeyError:
        return {"code": -1, "data": "Failed to parse query prameter 'keywords'"}
