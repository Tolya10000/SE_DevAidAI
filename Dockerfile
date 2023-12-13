FROM python:3.11

USER root
WORKDIR /app

COPY ./app.py ./
COPY ./requirements.in ./

RUN pip install --upgrade pip \
    && pip install -r requirements.in

CMD ["streamlit", "run", "app.py", "--server.port", "1460"]