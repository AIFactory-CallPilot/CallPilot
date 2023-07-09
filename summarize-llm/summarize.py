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
    template = """
    You are a CSR of Seoul City service call center. You will read conversation between customer and CSR.
    Write a summary of following conversation. 
    
    Conversation: {text}

    Format must be one sentence of "질문" , one paragraph of "답변" . 
    Summarize it in Korean, with periodic style. You must summarize "질문" in only one sentence.  
    "답변" could be more than one sentence, but concise.
    If there are any specific price, number or name in counselor's answer, mention it. 
    "답변" should be less than 500 bytes length.
    
    질문:
    답변:
    """
    prompt = PromptTemplate(template=template, input_variables=['text'])
    summary_chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=prompt, verbose=True)
    docs = [Document(page_content=text)]

    summary_result = summary_chain.run(docs)
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
