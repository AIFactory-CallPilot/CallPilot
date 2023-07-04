import os
from fastapi import FastAPI, HTTPException
from google.cloud import firestore

app = FastAPI()


@app.get("/{name}")
def get_response(name: str):
    db = firestore.Client()
    result = db.collection(os.environ["FIRESTORE_COLLECTION"]).document(name).get()
    if not result.exists:
        HTTPException(status_code=404, detail=f"object name {name=} not found.")
    return result.to_dict()
