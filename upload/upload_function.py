import functions_framework
import os
import random, string
from google.cloud import storage, firestore


@functions_framework.http
def hello_http(request):
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, PATCH, DELETE",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    f = request.files['file']
    random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
    filedir = os.path.join(os.getcwd(), random_string)
    filepath = os.path.join(filedir, f.filename)
    os.makedirs(filedir, exist_ok=True)
    f.save(filepath)

    BUCKET_NAME = "callpilot-voice-data"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)

    bucket_filename = "-".join([random_string, f.filename])
    blob = bucket.blob(bucket_filename)
    blob.upload_from_filename(filepath)

    db = firestore.Client()
    doc_ref = db.collection("voice_to_text").document(bucket_filename)
    doc_ref.set({
        'name': bucket_filename,
        'progress': "Speech to Text 변환 중..."
    })
    headers = {"Access-Control-Allow-Origin": "*"}
    return (
        {"body": bucket_filename},
        200,
        headers
    )