from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import BayesianRidge
from sklearn import metrics
import pandas as pd
import pickle
import ray

ray.init(address="auto")
data = pd.read_csv('training_dataset.csv')
y = data['stargazers_count']
X = data.drop('stargazers_count', 1)
results = {}

#Ridge
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
Ridge = Ridge()
Ridge.fit(X_train,y_train)
y4_pred = Ridge.predict(X_test)
results[Ridge] = metrics.r2_score(y4_pred,y_test)

with open('model.pkl',"wb") as f:
    pickle.dump(Ridge,f)