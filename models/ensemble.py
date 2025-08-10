from sklearn.model_selection import train_test_split
from models import logistic_regression
from models import random_forest
from models import svm
from data import unify
import pandas as pd
from sklearn.metrics import classification_report

data = unify.get_data()

y = data['republican_victory'].astype(bool)
X = data.drop(['state','year','district'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=21)

logreg = logistic_regression.LogReg(X_train, y_train)
rf = random_forest.RF(X_train, y_train)
sv = svm.SVM(X_train, y_train)


predictions_df = pd.DataFrame()

predictions_df['SVM'] = sv.predict_proba(X_test)[:,1].astype('float64')
predictions_df['RF'] = rf.predict_proba(X_test)[:,1].astype('float64')
predictions_df['LR'] = logreg.predict_proba(X_test)[:,1].astype('float64')

predictions_df['prob'] = predictions_df.mean(axis=1)
predictions_df['prediction'] = predictions_df['prob'].apply(lambda x: 1 if x >= 0.5 else 0)


prediction_list = predictions_df['prediction'].astype(list)

print(classification_report(y_test, prediction_list))
