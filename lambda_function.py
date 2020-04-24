"""
label the photo which are added to the s3 bucket using 
rekognition
"""

import json
import urllib.parse
import boto3
import datetime
import requests

URL = "https://search-photos-ajsv2de7bdfaxuhjx74leuu66a.us-east-1.es.amazonaws.com/index/_doc"

print("Loading Please")
s3 = boto3.client("s3")
es = boto3.client("es")
rekognition = boto3.client("rekognition")


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    try:
        response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": bucket, "Name": key}},
            MaxLabels=10,
            MinConfidence=90,
        )
        labels = []
        labels = []
        if response["Labels"]:
            for label in response["Labels"]:
                name = label["Name"]
                labels.append(name)
        print(f"labels are {labels}")
        to_post = {
            "objectKey": key,
            "bucket": bucket,
            "createdTimeStamp": str(datetime.datetime.now()),
            "labels": labels,
        }
        r = requests.post(
            "https://search-photos-ajsv2de7bdfaxuhjx74leuu66a.us-east-1.es.amazonaws.com/indices/_doc",
            json=to_post,
        )
        print(r.text)
    except Exception as e:
        print(e)
        print(
            "Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.".format(
                key, bucket
            )
        )
        raise e
