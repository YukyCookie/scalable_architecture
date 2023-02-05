import numpy as np
import pandas as pd
from sklearn.datasets import fetch_covtype
from sklearn.utils import check_array
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import ray
from ray import tune
from tune_sklearn import TuneGridSearchCV
import time

ray.init(address="auto")
# ray.init(address="192.168.2.54:6379")

t0 = time.time()
forests = fetch_covtype(random_state=41, shuffle=True)
X = check_array(forests.data, dtype=np.float32, order='C')
Y = (forests.target).astype(int)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=60000, test_size=5000, random_state=41)

rf = RandomForestClassifier(random_state=41)
rf.fit(X_train, Y_train)

n_estimators = [100,120,140]
max_depth = [5,4,3]
ccp_alpha = [0.00001, 0.0001, 0.001]

random_grid = {'n_estimators': n_estimators,
               'max_depth': max_depth,
               'ccp_alpha': ccp_alpha
               }
hyper = TuneGridSearchCV(estimator=rf,
                        param_grid=random_grid,
                        n_jobs=-1,
                        cv=3)
result = hyper.fit(X_train, Y_train)
t1 = time.time()
dtime = t1-t0

predict_be = rf.predict(X_test)
AccTest_be = accuracy_score(Y_test, predict_be)

predict_af = hyper.predict(X_test)
AccTest_af = accuracy_score(Y_test, predict_af)
# print("default parameter: {}".format(rf.get_params()))
print("Time:{}".format(dtime))