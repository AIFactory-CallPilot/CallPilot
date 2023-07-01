import functions_framework
import os
import openai
from google.cloud import storage, firestore


@functions_framework.http
def hello_http(request):
    BUCKET_NAME = ""
    OBJECT_NAME = ""
    content_type = request.headers["content-type"]
    if content_type != "application/json":
        raise ValueError("application type should be 'application/json'")

    request_json = request.get_json(silent=True)
    if not request_json:
        raise ValueError("cannot serialize request to json")

    if "bucket" not in request_json or "object" not in request_json or "collection" not in request_json:
        raise ValueError("request payload field 'bucket' / 'object' should be included")
    BUCKET_NAME = request_json['bucket']
    OBJECT_NAME = request_json['object']
    FIRESTORE_COLLECTION = str(request_json['collection'])
    print(BUCKET_NAME, OBJECT_NAME, FIRESTORE_COLLECTION)
    # # cloud storage에서 파일 가져오기
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    filepath = os.path.join(os.getcwd(), OBJECT_NAME)

    bucket.blob(blob_name=OBJECT_NAME).download_to_filename(filepath)

    # openai whisper api 사용
    openai.api_key = os.environ['OPENAI_API_KEY']
    audio_file = open(filepath, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # text = "openai result"
    text = transcript['text']
    # firestore에 데이터 저장
    firestore_update(OBJECT_NAME, text, FIRESTORE_COLLECTION)
    return {
        'statusCode': 200,
        'body': text
    }


def firestore_update(filename: str, text: str, collection_name: str):
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(filename)
    result = doc_ref.set({
        'name': filename,
        'text': text,
        "progress": "LLM 요약 중..."
    })
    print(result)
    return result

