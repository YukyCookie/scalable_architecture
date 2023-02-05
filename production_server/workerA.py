from celery import Celery

from numpy import loadtxt
import numpy as np
import requests
import pandas as pd
import requests
import sklearn 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pickle

model_file = './model.pkl'
data_file = './preprocessing.csv'


def load_data():
    dataset =  pd.read_csv(data_file)
    y = dataset['stargazers_count']
    X = dataset.drop('stargazers_count',1)
    return X, y

def load_model():
    # load json and create model
    pkl_file = open(model_file, 'rb')
    loaded_model = pickle.load(pkl_file)
    return loaded_model

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task
def get_accuracy():
    X, y = load_data()
    loaded_model = load_model()
    predictions = loaded_model.predict(X)
    result = metrics.r2_score(predictions, y)
    return {"model":str(loaded_model), "result":result}