#!/usr/bin/python
from google.cloud import vision, storage
import boto3
import os
import json

def get_aws_image():
    try:
        s3_client = boto3.client('s3')
        s3_object = s3_client.get_object(Bucket=os.environ['AWS_IMAGE_SRC'], Key='shanghai.jpeg')
        object_content = s3_object['Body'].read()
        return object_content
    except Exception as e:
        print(f"An error occurred: {e}")

def label_detection(image_data):
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.content = image_data

    response = client.label_detection(image=image)
    print('########## Showing access to Vision API data ##########')
    print('Labels (and confidence score):')
    print('=' * 30)
    results_set = {}
    for label in response.label_annotations:
        print(label.description, '(%.2f%%)' % (label.score*100.))
        results_set[label.description] = '(%.2f%%)' % (label.score*100.)
    return results_set

def upload_to_gcs(label_content,image_data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ['GCP_IMAGE_DST'])

    blob = bucket.blob('shanghai.json')
    blob.upload_from_string(json.dumps(label_content), content_type="application/json")

    blob = bucket.blob('shanghai.jpeg')
    blob.upload_from_string(image_data, content_type="image/jpeg")

def script_handler(event=None, context=None):
    image_data = get_aws_image()
    label_content = label_detection(image_data)
    upload_to_gcs(label_content,image_data)

if __name__ == "__main__":
    script_handler()