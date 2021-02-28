# -*- coding: utf-8 -*-
"""HR_analysics_Catboost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BRkEOBETTBz8Izd2zHx6aMGLyX3P90MQ

#Imp. Libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""#Imp. Dataset"""

train=pd.read_csv('HR_train.csv')
test=pd.read_csv('HR_Test.csv')

train.head()

print(test)

"""#Analysing Data"""

train.info()

train.isnull().any()

train.isnull().sum()

test.isnull().sum()

"""#NUM of promoted"""

train['is_promoted'].value_counts()

"""#% of Promoted from total"""

percent=(4668/54808)*100
print("Total percent of Promoted: {:.2f}%".format(percent))

"""#Filling missing values in Train"""

train['education'].fillna(train['education'].mode()[0], inplace = True)
train['previous_year_rating'].fillna(1, inplace = True)
train.isnull().sum().sum()

"""#Filling missing values in Test"""

test['education'].fillna(test['education'].mode()[0],inplace=True)
test['previous_year_rating'].fillna(1,inplace=True)
test.isnull().sum().sum()

"""#Removing Employee Id"""

train = train.drop(['employee_id'] , axis=1)
train.columns

empl_id=test['employee_id']
test = test.drop(['employee_id'] , axis=1)
test.columns

X_test=test
X_test.columns

"""#One Hot Encoding for test set"""

x_test = test
x_test = pd.get_dummies(X_test)
x_test.columns

"""#Splitting Data"""

x=train.iloc[:,:-1]
y=train.iloc[:,-1]

print("X",x.shape)
print("Y",y.shape)

"""#One Hot Encoding for Trainset"""

x = pd.get_dummies(x)
x.columns

"""#SMOTE"""

from imblearn.over_sampling import SMOTE

x_sample, y_sample = SMOTE().fit_sample(x, y.values.ravel())

x_sample = pd.DataFrame(x_sample)
y_sample = pd.DataFrame(y_sample)

# checking the sizes of the sample data
print("Size of x-sample :", x_sample.shape)
print("Size of y-sample :", y_sample.shape)

"""#Splitting Train and Test Data in TRAIN Data"""

from sklearn.model_selection import train_test_split
x_train , x_valid ,y_train ,y_valid=train_test_split(x_sample,y_sample,test_size=0.2,random_state=0)

print("Shape of x_train: ", x_train.shape)
print("Shape of x_valid: ", x_valid.shape)
print("Shape of y_train: ", y_train.shape)
print("Shape of y_valid: ", y_valid.shape)

"""#Feature Scaling and PCA"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test  = sc.transform(x_test)
x_valid = sc.transform(x_valid)

from sklearn.decomposition import PCA

pca = PCA(n_components = None)
x_train = pca.fit_transform(x_train)
x_test = pca.transform(x_test)
x_valid = pca.transform(x_valid)

"""#Model

#CatBoost
"""

!pip install catboost

from catboost import CatBoostClassifier
classifier = CatBoostClassifier()
classifier.fit(x_train, y_train)

from sklearn.metrics import confusion_matrix, accuracy_score
y_pred = classifier.predict(x_valid)
cm = confusion_matrix(y_valid, y_pred)
print(cm)
accuracy_score(y_valid, y_pred)

y_pred = classifier.predict(x_test)
print("Accuracy of :",classifier.score(x_train,y_train))

"""#Submission"""

submission=pd.read_csv("HR_Submission.csv")
submission.head()

submission=pd.DataFrame({"employee_id":empl_id,"is_promoted":y_pred})
submission.head()

filename = 'submission.csv'
submission.to_csv(filename, index = False)

print("Saved File : ", filename)