import boto3
import os
import json
import decimal


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Main_Table')

s3 = boto3.resource('s3')
jpeg_bucket_name = 'eqo-jpeg-test'
jpeg_bucket = s3.Bucket(jpeg_bucket_name)

pdf_bucket_name = 'eqo-pdf-test'
pdf_bucket = s3.Bucket(pdf_bucket_name)


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
        s3.Object(jpeg_bucket_name, filename).put(Body=open(folder + filename, 'rb'))


def upload_pictures(folder):
    for filename in os.listdir(folder):
        s3.Object(pdf_bucket_name, filename).put(Body=open(folder + filename, 'rb'))


json_folder = 'JSON Files/'
write_json_to_dynamo(json_folder)


resume_folder = 'resumes/'
upload_resumes(resume_folder)


pic_folder = 'profile/'
upload_pictures(pic_folder)



