import torch
from transformers import BertForSequenceClassification, AutoTokenizer

import streamlit as st

LABELS = ['neutral', 'happiness', 'sadness', 'enthusiasm', 'fear', 'anger', 'disgust']
tokenizer = AutoTokenizer.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection')
model = BertForSequenceClassification.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection')


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


if __name__ == '__main__':
    with st.chat_message('assistant'):
        st.write('Привет, пиши предложение и я оценю выраженные эмоции')
    prompt = st.chat_input('Input')
    if prompt:
        with st.chat_message('assistant'):
            result = predict_emotions(prompt)
            st.write('Ваше предложение имеет следующие эмоции')
            st.write(result)
