import boto3 

# Create a DynamoDB client with the specified endpoint URL
dynamo_db = boto3.resource('dynamodb', endpoint_url = "http://localhost:8000")
table = dynamo_db.Table('Movies')

# ===================== CREATE SECONDARY INDEX =====================
# Create a global secondary index on the 'Genre' attribute
table.update(
    AttributeDefinitions = [
        {
            'AttributeName':'Genre',
            'AttributeType':'S'
        },
    ],
    GlobalSecondaryIndexUpdates = [{
        'Create':{
            'IndexName': 'GenrePrimary',
            'KeySchema': [
                {
                    'AttributeName':'Genre',
                    'KeyType':'HASH'
                },
            ],
            'Projection': {
                'ProjectionType':'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits':100,
                'WriteCapacityUnits':100
            }
        }  
    }]
)

# ===================== QUERY SECONDARY INDEX =====================
# Scan all movies in the secondary index
print("All movies in the secondary index:")
for movie in table.scan(TableName='Movies', IndexName = "GenrePrimary")['Items']:
    for k,v in movie.items():
        print(k, ' : ', v)
    print()

# ===================== QUERY SPECIFIC GENRES =====================
from boto3.dynamodb.conditions import Key, Attr

# Query drama movies from secondary index
print("Drama movies:")
drama_movies = table.query(
    IndexName = 'GenrePrimary',
    Limit = 50,
    ExpressionAttributeNames = {
        '#y':'Year'
    },
    ExpressionAttributeValues={
    },
    KeyConditionExpression=Key('Genre').eq('Drama'),
    ProjectionExpression = "Title, #y, Genre, Director"
)

# Query crime movies from secondary index
print("Crime movies:")
crime_movies = table.query(
    IndexName = 'GenrePrimary',
    Limit = 50,
    ExpressionAttributeNames = {
        '#y':'Year'
    },
    ExpressionAttributeValues={
    },
    KeyConditionExpression=Key('Genre').eq('Crime'),
    ProjectionExpression = "Title, #y, Genre, Director"
)

# Print results of both queries
for movie in drama_movies['Items'] + crime_movies['Items']:
    for k,v in movie.items():
        print(k, ' : ', v)
    print()

# Suggestions:
# 1. Consider adding error handling for each operation.
# 2. Implement logging to track the execution flow and any potential issues.
# 3. Use pagination for large result sets to improve performance.
# 4. Consider creating a function to perform queries to avoid code duplication.
# 5. Use environment variables for sensitive information like endpoint URLs.