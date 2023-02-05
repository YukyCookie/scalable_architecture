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

#Linear regression
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
Lr = LinearRegression()
Lr.fit(X_train,y_train)
y_pred = Lr.predict(X_test)
results[Lr] = metrics.r2_score(y_pred,y_test)

#Random Forest
RF = RandomForestRegressor()
RF.fit(X_train,y_train)
y2_pred = RF.predict(X_test)
results[RF] = metrics.r2_score(y2_pred,y_test)

#Decision Tree
DT = DecisionTreeRegressor()
DT.fit(X_train,y_train)
y3_pred = DT.predict(X_test)
results[DT] = metrics.r2_score(y3_pred,y_test)

#Ridge
Ridge = Ridge()
Ridge.fit(X_train,y_train)
y4_pred = Ridge.predict(X_test)
results[Ridge] = metrics.r2_score(y4_pred,y_test)

#Bayesian Ridge
BR = BayesianRidge()
BR.fit(X_train,y_train)
pickle_fn = "BayesianRidge_model.pkl"
y5_pred = BR.predict(X_test)
results[BR] = metrics.r2_score(y5_pred,y_test)

model_to_save = max(results, key=results.get)

with open('model.pkl',"wb") as f:
    pickle.dump(model_to_save,f)


