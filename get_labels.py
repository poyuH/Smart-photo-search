import boto3
import base64
import cv2
import urllib
import json
import requests

rekognition = boto3.client("rekognition")
f = open("./download (1).jpg", "rb")
data = f.read()
f.close()
# data = base64.b64encode(data)
response = rekognition.detect_labels(
    Image={"Bytes": data}, MaxLabels=10, MinConfidence=90
)
labels = []
if response["Labels"]:
    for label in response["Labels"]:
        name = label["Name"]
        labels.append(name)
to_post = {"title": "house", "bucket": "photos", "labels": labels}
r = requests.post(
    "https://search-photos-ajsv2de7bdfaxuhjx74leuu66a.us-east-1.es.amazonaws.com/movies/_doc",
    json={"title": "spirited2 away"},
)
print(r.text)
# https://search-photos-ajsv2de7bdfaxuhjx74leuu66a.us-east-1.es.amazonaws.com/movies/_search?q=labels:dog
