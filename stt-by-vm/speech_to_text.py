import whisper
import os
from google.cloud import storage, firestore


def speech_to_text(model: whisper.Whisper, filename: str) -> str:
    result = model.transcribe(filename)
    return result['text']


def firestore_update(filename: str, text: str):
    FIRESTORE_COLLECTION = os.environ['FIRESTORE_COLLECTION']
    db = firestore.Client()
    doc_ref = db.collection(FIRESTORE_COLLECTION).document(filename)
    result = doc_ref.set({
        'name': filename,
        'text': text,
        "progress": "LLM 요약 중..."
    })
    print(result)
    return result


def process():
    BUCKET_NAME = os.environ['BUCKET_NAME']
    OBJECT_NAME = os.environ["OBJECT_NAME"]

    # # cloud storage에서 파일 가져오기
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    filepath = os.path.join(os.getcwd(), OBJECT_NAME)

    bucket.blob(blob_name=OBJECT_NAME).download_to_filename(filepath)

    model = whisper.load_model("small", download_root=os.getcwd())
    text = speech_to_text(model, filepath)
    print(text)
    firestore_update(OBJECT_NAME, text)
    return


process()
