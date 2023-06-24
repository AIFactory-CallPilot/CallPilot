import glob
import os
import whisper
# import aws_client
import boto3
from speech_to_text import speech_to_text


def handler(event, context):
    binary_data = event.get("body-json", "")
    model = whisper.load_model("small", in_memory=True)

    # input으로 들어온 파일 읽어서 기록
    with open("/tmp/input_file.mp3", "wb") as writer:
        writer.write(bytes(binary_data, encoding='utf-8'))

    result = speech_to_text(model, "/tmp/input_file.mp3")

    # dynamoDB에 저장
    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table("test-table")
    response = table.put_item(
        Item={
            'name': 'test1',
            'text': result
        }
    )
    print(response)
    return {
        'statusCode': 200,
        'body': "binary data length : " + str(len(binary_data)) + " text: " + result
    }
