import os
import openai
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import firestore

app = FastAPI()

# os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


class Payload(BaseModel):
    bucket: str
    object: str
    collection: str


@app.post("/")
def process(payload: Payload):
    db = firestore.Client()
    result = db.collection(payload.collection).document(payload.object).get()
    if not result.exists:
        HTTPException(status_code=404, detail=f"object name {payload.object=} not found.")
    text = result.to_dict()['text']
    summary = summarize(text)

    firestore_update(payload.object, summary, payload.collection)
    return {
        'statusCode': 200,
        'body': summary
    }


def summarize(text: str):
    # template = """
    # Write a summary of the conversation. This is Telephone Consultation between two persons.
    #
    # {text}
    #
    # Answer in Korean:
    # """
    # prompt = PromptTemplate(template=template, input_variables=['text'])
    # summary_chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=prompt, verbose=True)
    # docs = [Document(page_content=text)]
    #
    # summary_result = summary_chain.run(docs)
    summary_result = "test"
    return summary_result


def firestore_update(filename: str, summary: str, collection_name: str):
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(filename)
    result = doc_ref.set({
        'name': filename,
        "progress": "요약 완료.",
        "summary": summary
    }, merge=True)
    print(result)
    return result
