# Smart-photo-search

This project is an implementation of a photo album web application which allows people to upload pictures onto a storage space and search from the existed photos by casual and colloquial queries. The way of inputing query includes both text and voice. By integrating several Amazon Web Services such as ElasticSearch, Rekognition, Lex bot and Transcribe, we were able to quickly develop the described functions into a serverless and scalable realization. An immediate new version releasing is achieved by using CodePipline. And the whole project is packaged as a Cloudformation template ready to deploy the exact same functions anywhere.

# Demonstration

[put the gif here]

Before any user uploads their own photos, we stored into the database thousands of images that belong to one or perhaps multiple labels that can be recognized by Amazon Rekognition. Then we input query like "dogs", "show me dogs" or "show me photos with dogs and cats" by typing or speaking, and the webpage displayed the searching results and they are exactly what we want. 

Next, to show that the photos uploaded by users to the website are indeed stored in the databases and are assigned with correct labels. We first search for "horse" and confirmed that there's no picture of a horse already existed, and then we upload a horse's image through the interface of the website and do the searching again. This time the website returns the one picture that we just uploaded, it's "the" picture of a horse and it's perfectly-identified as a horse.

# System Architecture

[put the system architecture here]

## ElasticSearch
Elasticsearch is a distributed, RESTful search and analytics engine that centrally stores data so the users can search, index, and analyze data of all shapes and sizes.

We store JSON objects in the ElasticSearch that reference the S3 objects from PUT events and an array of string labels describing them, one for each label detected by Rekognition.

The JSON object has the following schema:
`{
  “objectKey”: “my-photo.jpg”,
  “bucket”: “my-photo-bucket”,
  “createdTimestamp”: “2018-11-05T12:40:02”,
  “labels”: [
    “person”,
    “dog”,
    “ball”,
    “park”
  ]
}`

## Lambda Function
AWS Lambda allows user to run code without provisioning or managing servers. Here the lambda functions are assigned to handle the event of uploading and the event of searching.

The "index-photos" lambda function:
It is triggered when a PUT event of a photo to S3 bucket happens. It will obtain the S3 access information of this photo, apply Rekognition function to detect the labels of it, and compose that information into a JSON object and store it into ElasticSearch .

The "search-photos" lambda function:
This function is responsible for handling the query input by the user and return the corresponding results. Since we allow users to input colloquial contexts, the first step of processing is to disambiguate it. This work is done by sending the context to a configured Lex bot. The Lex bot will return the extracted keywords (the labels) if there's any, and the function will take these words and searching on the ElasticSearch. Then, we use the search results from Elasticsearch to tell the front-end which pictures it should display to the user. 

## Amazon Lex
Amazon Lex is a tools to tackle challenging deep learning problems, such as speech recognition and language understanding.

We created a "SearchIntent" that can pick up both keyword searches, as well as sentence searches.

## CodePipeline
AWS CodePipeline is a continuous delivery service that automates the steps required to release your software changes continuously. We created a pipeline that can builds and deploys the code for/to Lambda functions/ builds and deploys frontend code to its corresponding S3 bucket.

While new commit is pushed to GitHub (both for frontend and backend repos), CodePipeline will build and deploy the code to the corresponding AWS infrastructure.

## CloudFormation
CloudFormation allows user to use a template to model and provision, in an automated and secure manner, all the resources needed for the applications across all regions and accounts.

We created a CloudFormation template to represent all the infrastructure resources and permissions that is ready to deploy the entire identical functional stack as this project at any place.

## Others
Other Amazon Web Services we used but not introduced above includes **S3 bucket** (photo storage), **Rekognition** (detection of labels), **API Gateway** (generate a SDK for an API defines PUT and GET event on the front-end) and **Transcribe** (use voice rather than text to perform the search).

