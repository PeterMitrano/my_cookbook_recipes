import json
import boto3

def handle_event(event, context):
    # parse the recipe id from the parameters
    try:
        recipe_id =  event['params']['querystring']['id']

        # lookup that id in our database
        resource = boto3.resource("dynamodb")

        try:
            id_num = int(recipe_id)

            table = resource.Table('my_cookbook_recipes')
            response = table.get_item(Key={'id': id_num})

            if 'Item' in response:
                return response['Item']
            else:
                return "No recipe ith id %d" % id_num
        except ValueError:
            return "recipe_id must be an integer"
    except KeyError:
        return "Failed to parse query prameter 'id'"
