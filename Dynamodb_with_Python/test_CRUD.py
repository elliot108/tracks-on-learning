import boto3 

# Create a DynamoDB client with the specified endpoint URL
dynamo_db = boto3.resource('dynamodb', endpoint_url = "http://localhost:8000")
table = dynamo_db.Table('Movies')

# ===================== CREATE OPERATIONS =====================

# 1. Create Table
#------------------------------------------------------------
dynamo_db.create_table(
    TableName = "Movies",
    AttributeDefinitions = [
        {'AttributeName':'Title',
        'AttributeType':'S'},  # String type attribute for the title
        {'AttributeName':'ReleaseDate',
        'AttributeType':'S'}   # String type attribute for the release date
    ],
    KeySchema = [
        {'AttributeName':'Title',
        'KeyType':'HASH'},  # Partition key
        {'AttributeName':'Release Date',
           'KeyType':'RANGE'}  # Sort key
    ],
    ProvisionedThroughput = {
            'ReadCapacityUnits': 5,  # Read capacity units
            'WriteCapacityUnits': 5  # Write capacity units
        }
    )

# 2. Create Item
#------------------------------------------------------------
# 2.1 Using client (low-level) API
dynamo_db.put_item(
    Item = {
        'Title':{'S':'Titanic'},
        'Release Date':{'S':'1997'}
    },
    ReturnConsumedCapacity='TOTAL',
    TableName = 'Movies'
)

# 2.2 Using resource (high-level) API
table.put_item(
    Item={
        'Title':'Notebook',
        'Release Date':'2008'
    }
)

# 3. Batch Write
#------------------------------------------------------------
from decimal import Decimal

movies = [
    {
        "Title": "Inception",
        "Director": "Christopher Nolan",
        "Release Date": "2010",
        "Genre": "Sci-Fi",
        "Rating": Decimal("8.8"),
        "Duration Minutes": 148
    },
    {
        "Title": "The Shawshank Redemption",
        "Director": "Frank Darabont",
        "Release Date": "1994",
        "Genre": "Drama",
        "Rating": Decimal("9.3"),
        "Duration Minutes": 142
    },
    {
        "Title": "The Godfather",
        "Director": "Francis Ford Coppola",
        "Release Date": "1972",
        "Genre": "Crime",
        "Rating": Decimal("9.2"),
        "Duration Minutes": 175
    },
    {
        "Title": "The Dark Knight",
        "Director": "Christopher Nolan",
        "Release Date": "2008",
        "Genre": "Action",
        "Rating": Decimal("9.0"),
        "Duration Minutes": 152
    },
    {
        "Title": "Pulp Fiction",
        "Director": "Quentin Tarantino",
        "Release Date": "1994",
        "Genre": "Crime",
        "Rating": Decimal("8.9"),
        "Duration Minutes": 154
    }
]

with table.batch_writer() as batch:
    for movie in movies:
        batch.put_item(movie)

# ===================== READ OPERATIONS =====================

# 1. Get Item
#------------------------------------------------------------
# 1.1 Using client (low-level) API
movie = dynamo_db.get_item(
    Key = {
        'Title': {'S': 'The Notebook'},
        'Release Date': {'S':'2008'}
    },
    AttributesToGet = ['Cast'],
    # ReturnConsumedCapacity='TOTAL',
    TableName = 'Movies'
)['Item']

# 1.2 Using resource (high-level) API
item = table.get_item(
    Key = {
        'Title':'Notebook',
        'Release Date':'2008'
    }
)

print(item)

# 2. Scan
#------------------------------------------------------------
from boto3.dynamodb.conditions import Attr
response = table.scan(
    Limit = 50,
    ProjectionExpression = 'Title, Director, Genre',
    FilterExpression = Attr('Director').eq('Christopher Nolan')
)

# 3. Query
#------------------------------------------------------------
response = table.query(
    Limit = 50,
    
    ExpressionAttributeNames = {
        '#T' : 'Title'
    },
    ExpressionAttributeValues = {
        ':I':'Inception'
    },
    KeyConditionExpression = "#T = :I",
    ProjectionExpression = "Director, Genre"
)

for item in response["Items"]:
    for k,v in item.items():
        print(k, " = ", v)

# ===================== UPDATE OPERATIONS =====================

# 1. Update Item
#------------------------------------------------------------
# 1.1 Using client (low-level) API
dynamo_db.update_item(
    Key = {
        'Title': {'S': 'The Notebook'},
        'Release Date': {'S':'2008'}
    },
    ExpressionAttributeNames = {
        '#c' :'Cast'
    },
    # ExpressionAttributeValues = {
    #     ':c' :{'S':'Ryan Gosling'}
    # },
    UpdateExpression = "REMOVE #c",
    TableName = "Movies"
    
)

# 1.2 Using resource (high-level) API
table.update_item(
    Key = {
        'Title':'Notebook',
        'Release Date':'2008'
    },

    ExpressionAttributeNames = {
        '#c':'Cast'
    },
    UpdateExpression = "SET #c = :c",
    
    ExpressionAttributeValues = {
        ':c':'Someone else'
    }
)
print(movie)

# 2. Update Table
#------------------------------------------------------------
table.update(
    AttributeDefinitions = [
        {
            'AttributeName':'Title',
            'AttributeType':'S'
        },
        {
            'AttributeName':'ReleaseDate',
            'AttributeType':'S'
        }
    ]
)

# ===================== DELETE OPERATIONS =====================

# 1. Delete Item
#------------------------------------------------------------
dynamo_db.delete_item(
    TableName = 'Movies',
    Key = {
        'Title': {'S': 'The Notebook'},
        'Release Date': {'S':'2008'}
    },
    ExpressionAttributeNames = {
        '#t':'Title'
    }, 
    ExpressionAttributeValues = {
        ':t' :{'S' : 'The Notebook'} 
    },
    ConditionExpression = "#t = :t"
)

# 2. Delete Table
#------------------------------------------------------------
table.delete()

# Suggestion: Consider adding error handling and logging for each operation
# to improve the robustness of the code.
