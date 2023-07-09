import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{name}")
def get_response(name: str):
    db = firestore.Client()
    result = db.collection(os.environ["FIRESTORE_COLLECTION"]).document(name).get()
    if not result.exists:
        HTTPException(status_code=404, detail=f"object name {name=} not found.")
    return result.to_dict()
