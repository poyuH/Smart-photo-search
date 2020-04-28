"""
Note: we need access to CloudWatch and Amazon Lex service for this
lambda function. To do that go to IAM > Create a role > add 
"CloudWatchFullAccess" and "AmazonLexFullAcess" to create a role.
Attach this role to this lambda function.

Note: Don't use Lambda Proxy integration while attaching lambda to API gateway
"""
import json
import boto3
# from aws_requests_auth.aws_auth import AWSRequestsAuth
import requests

print('Loading function')

AMAZON_LEX_BOT = "Search"
LEX_BOT_ALIAS = "v_one"
USER_ID = "user"
# used by the lex to specify which user is it communicating with

TABLENAME = 'photos'
ELASTIC_SEARCH_URL = "https://search-photos-ajsv2de7bdfaxuhjx74leuu66a.us-east-1.es.amazonaws.com/_search?q="

# session = boto3.session.Session()
# credentials = session.get_credentials().get_frozen_credentials()
# es_host = 'search-photos-ajsv2de7bdfaxuhjx74leuu66a.us-east-1.es.amazonaws.com'
# awsauth = AWSRequestsAuth(
#     aws_access_key=credentials.access_key,
#     aws_secret_access_key=credentials.secret_key,
#     aws_token=credentials.token,
#     aws_host=es_host,
#     aws_region=session.region_name,
#     aws_service='es'
# )
# elasticsearch
def get_photos_ids(URL, labels):
    """
    return photos ids having the 
    labels as desired 
    """
    
    URL = URL + str(labels)
    #response = requests.get(URL, auth=awsauth).content
    response = requests.get(URL).content
    data = json.loads(response)
    hits = data["hits"]["hits"]
    id_list = []
    labels_list = []
    for result in hits:
        _id = result["_source"]["objectKey"]
        id_list.append(_id)
        _labels = result["_source"]["labels"]
        labels_list.append(_labels)
    return id_list, labels_list

def post_on_lex(query, user_id=USER_ID):
    """
    Get the user input from the frontend as text and pass
    it to lex. Lex will generate a new response.

    it will return a json response: 
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html
    """
    client = boto3.client('lex-runtime')
    lex_response = client.post_text(botName=AMAZON_LEX_BOT,
                                    botAlias=LEX_BOT_ALIAS,
                                    userId=user_id, 
                                    inputText=query)
    
    if lex_response['slots']['Label_one'] and lex_response['slots']['Label_two']:
        labels = 'labels:' + lex_response['slots']['Label_one'] + '+' + 'labels:' + lex_response['slots']['Label_two']
    elif lex_response['slots']['Label_one']:
        labels = 'labels:' + lex_response['slots']['Label_one']
    else:
        return
    return labels


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin":"*",
            "Access-Control-Allow-Credentials" : True,
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    # messages = json.loads(event['body'])['messages']
    # assert len(messages) == 1
    # message = messages[0]
    # user_id = message['unstructured']['id']
    # text = message['unstructured']['text']
    # # time = message['unstructured']['time']
    # response_text, user_id = post_on_lex(str(text), str(user_id))
    # time = datetime.datetime.now().isoformat()
    # response = {"messages": [{"type": "message", "unstructured": {
    #     "id": str(user_id), "text": str(response_text), "timestamp": str(time)}}]}
    # return respond(None, response)
    
    query = event['queryStringParameters']['q']
    labels = post_on_lex(query)
    id_list, labels_list = get_photos_ids(ELASTIC_SEARCH_URL, labels)
    
    results = []
    for i, l in zip(id_list, labels_list):
        results.append({"url": 'https://prj3photostore.s3.amazonaws.com/' + i, "labels": l})
    response = {"results": results}    
    return respond(None, response)
