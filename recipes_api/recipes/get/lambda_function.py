import boto3
import json
import logging

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

def handle_event(event, context):


    # parse the recipe id from the parameters
    try:
        recipe_id =  event['params']['querystring']['id']

        try:
            id_num = int(recipe_id)

            if id_num < 0:
                return {"code": -1, "data": "recipe_id (%d) most be positive." % id_num}

            # lookup that id in our database
            if "debug" in context:
                resource = boto3.resource("dynamodb",
                        endpoint_url="http://localhost:8000",
                        aws_access_key_id="fake",
                        aws_secret_access_key="fake")
            else:
                resource = boto3.resource("dynamodb")

            table = resource.Table('my_cookbook_recipes')
            response = table.get_item(Key={'id': id_num})

            if 'Item' in response:
                return {"code": 0, "data": response['Item']}
            else:
                return {"code": 1, "data": "No recipe ith id %d" % id_num}
        except ValueError:
            return {"code": -1, "data": "recipe_id must be an integer"}
    except KeyError:
        return {"code": -1, "data": "Failed to parse query prameter 'id'"}
