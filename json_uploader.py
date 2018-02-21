import boto3
import os
import json
import decimal


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Test')

s3 = boto3.resource('s3')
bucket_name = 'eqoresumetest'
bucket = s3.Bucket(bucket_name)


def write_json_to_dynamo(folder):
    if folder[:-1] != '/' or folder[-1] != '\\':
        folder += '/'

    with table.batch_writer() as batch:
        for filename in os.listdir(folder):
            try:
                file = json.load(open(folder + filename), parse_float=decimal.Decimal)
            except json.decoder.JSONDecodeError:
                print(filename + " could not be decoded")
                continue

            batch.put_item(Item = file['User'])


def upload_resumes(folder):
    for filename in os.listdir(folder):
        s3.Object(bucket_name, filename).put(Body=open(folder + filename, 'rb'))


def upload_pictures(folder):
    for filename in os.listdir(folder):
        s3.Object(bucket_name, filename).put(Body=open(folder + filename, 'rb'))


json_folder = 'JSON Files/'
write_json_to_dynamo(json_folder)


resume_folder = 'resumes/'
upload_resumes(resume_folder)


pic_folder = 'profile/'
upload_pictures(pic_folder)



