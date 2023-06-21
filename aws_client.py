import os

from dotenv import load_dotenv
import boto3

load_dotenv()


# def get_s3_object_list():
#     aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
#     aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
#     region_name = os.environ["AWS_REGION"]
#
#     s3 = boto3.resource("s3",
#                         aws_access_key_id=aws_access_key_id,
#                         aws_secret_access_key=aws_secret_access_key,
#                         region_name=region_name
#                         )
#     # bucket name은 callpilot-voice-data로 고정되어 있음
#     bucket = s3.Bucket("callpilot-voice-data")
#     for obj in bucket.objects.all():
#         print(obj)
#         print(obj.key)
#         if not os.path.exists(os.path.dirname(obj.key)):
#             os.makedirs(os.path.dirname(obj.key))
#         if obj.key.endswith(".mp3"):
#             bucket.download_file(obj.key, obj.key)
#             break
#     return

def dynamoDB_put_item(table_name: str, key: str, value: str, category: str, phase: str) -> int:
    aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    region_name = os.environ["AWS_REGION"]
    dynamodb = boto3.resource("dynamodb",
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name
                              )
    table = dynamodb.Table(table_name)
    response = table.put_item(
        Item={
            'name': key,
            'text': value,
            'category': category,
            'phase': phase
        }
    )
    print(response)
    return response['ResponseMetadata']['HTTPStatusCode']
