import boto3
import glob
import json
import os
import decimilify

table_name = 'my_cookbook_recipes'


def main():

    # pull in the samples from files
    samples = []
    samples_dir = '../../samples'
    if os.path.exists(samples_dir):
        sample_filenames = glob.glob(samples_dir + '*.json')
        for filename in sample_filenames:
            with open(filename, 'r') as f:
                sample = json.load(f)
                samples.append(sample)
    else:
        print 'no samples directory. quitting'
        return

    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="fake_region",
        aws_access_key_id="fake_id",
        aws_secret_access_key="fake_key")

    tables = [table.name for table in dynamodb.tables.all()]
    if table_name not in tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            })
        table.wait_until_exists()
    else:
        table = dynamodb.Table(table_name)

    # table exists, now insert.
    for sample in samples:

        # boto3 doesn't do floats
        sample = decimilify.decimilify(sample)
        item_key = {'id': 0}

        # ok so this badass python formats the update expression
        # don't fight it--the tests show it works. Just learn to love it
        updateExpr = 'SET '
        exprAttributeValues = {}
        exprAttributeNames = {}
        for key in sample:
            expr_val_key = ':%s' % key
            exprAttributeValues[expr_val_key] = sample[key]
            expr_name_key = '#_%s' % key
            exprAttributeNames[expr_name_key] = key
            updateExpr += '%s = :%s,' % (expr_name_key, key)

        updateExpr = updateExpr[:-1]  #strip trailing comma

        response = table.update_item(
            Key=item_key,
            UpdateExpression=updateExpr,
            ExpressionAttributeNames=exprAttributeNames,
            ExpressionAttributeValues=exprAttributeValues)

    print "Table ready."

if __name__ == "__main__":
    main()
