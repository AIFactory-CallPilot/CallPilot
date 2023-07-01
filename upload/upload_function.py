import functions_framework
import os
import random, string
from google.cloud import storage



@functions_framework.http
def hello_http(request):
    f = request.files['file']
    random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
    filedir = os.path.join(os.getcwd(), random_string)
    filepath = os.path.join(filedir, f.filename)
    os.makedirs(filedir, exist_ok=True)
    f.save(filepath)

    BUCKET_NAME = "callpilot-voice-data"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)

    blob = bucket.blob("-".join(random_string, f.filename))
    blob.upload_from_filename(filepath)

    return {
        'statusCode': 200,
        'body': filepath
    }