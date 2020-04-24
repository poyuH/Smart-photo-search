import boto3
import os
import time

s3 = boto3.client("s3")

files = os.listdir("./trees")
for file in files:
    s3.upload_file(
        f"./trees/{file}",
        "prj3photostore",
        f"{file}",
        {"ContentType": "image/png", "ACL": "public-read"},
    )
    print("sleep")
    time.sleep(10)
print("DONE")
