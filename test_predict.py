import os
import unittest
from app import predict_emotion, predict_emotions
from threading import Thread
from time import sleep
from requests.api import get


class TestApi(unittest.TestCase):
    def setUp(self):

        self.predict_data = {
            'Привет!': 'happiness',
            'Ненавижу выходить на улицу в дождь!!!': 'anger',
            'Мне очень грустно, когда много домашнего задания': 'sadness',
            'Может сходим погулять?': 'enthusiasm',
            'Я боюсь темноты': 'fear',
            'Сегодня обычный день': 'neutral',
            'disgust': 'disgust',
        }

    def test_predict(self):
        for k, v in filter((lambda x: x[1] != 'disgust'), self.predict_data.items()):
            assert predict_emotion(k) == v

    def test_sum_predict(self):
        for k in self.predict_data.keys():
            assert round(sum(predict_emotions(k).values()), 1) == 1.0

    def test_keys_predict(self):
        assert sorted(predict_emotions('Тест').keys()) == sorted(self.predict_data.values())

    def test_api(self):
        t = Thread(target=os.system, args=('streamlit run app.py --server.port 1460',))
        t.daemon = True
        t.start()
        sleep(5)
        assert get('http://127.0.0.1:1460').status_code == 200


if __name__ == '__main__':
    unittest.main()
