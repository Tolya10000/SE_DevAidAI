import torch
from transformers import BertForSequenceClassification, AutoTokenizer
from fastapi import FastAPI
from starlette.status import HTTP_200_OK
from pydantic import BaseModel

app = FastAPI()
LABELS = ['neutral', 'happiness', 'sadness', 'enthusiasm', 'fear', 'anger', 'disgust']
tokenizer = AutoTokenizer.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection')
model = BertForSequenceClassification.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection')


class InputModel(BaseModel):
    text: str


class ResponseModel(BaseModel):
    neutral: float
    happiness: float
    sadness: float
    enthusiasm: float
    fear: float
    anger: float
    disgust: float


def predict_emotion(text: str) -> str:
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()

    return LABELS[predicted[0]]


def predict_emotions(text: str) -> dict:
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    emotions_list = {}
    for i in range(len(predicted.detach().numpy()[0].tolist())):
        emotions_list[LABELS[i]] = predicted.detach().numpy()[0].tolist()[i]
    return emotions_list


@app.post(
    '/estimate',
    operation_id='estimate_text',
    status_code=HTTP_200_OK,
    response_model=ResponseModel
)
def estimate_text(body: InputModel):
    return ResponseModel(**predict_emotions(body.text))
