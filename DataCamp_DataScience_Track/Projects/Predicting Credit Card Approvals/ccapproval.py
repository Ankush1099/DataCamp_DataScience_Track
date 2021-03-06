# -*- coding: utf-8 -*-
"""
Created on Wed May 20 19:06:11 2020

@author: Ankush
"""

#Step 1. Credit card applications
# Import pandas
import pandas as pd
# Load dataset
cc_apps = pd.read_excel("dataset.xlsx", header = None)
# Inspect data
cc_apps.head()

#Step 2. Inspecting the applications
# Print summary statistics
cc_apps_description = cc_apps.describe()
print(cc_apps_description)
# Print DataFrame information
cc_apps_info = cc_apps.info()
print(cc_apps_info)
# Inspect missing values in the dataset
cc_apps.tail(17)

#Step 3. Handling the missing values (part i)
# Import numpy
import numpy as np
# Inspect missing values in the dataset
cc_apps.tail(17)
# Replace the '?'s with NaN
cc_apps = cc_apps.replace('?',np.nan)
# Inspect the missing values again
cc_apps.tail(17)

#Step 4. Handling the missing values (part ii)
# Impute the missing values with mean imputation
cc_apps.fillna((cc_apps.mean()), inplace=True)
# Count the number of NaNs in the dataset to verify
cc_apps.isnull().sum()

#Step 5. Handling the missing values (part iii)
# Iterate over each column of cc_apps
for col in range(0,14):
    # Check if the column is of object type
    if cc_apps[col].dtypes == 'object':
        # Impute with the most frequent value
        cc_apps = cc_apps.fillna(cc_apps[col].value_counts().index[0])

# Count the number of NaNs in the dataset and print the counts to verify
cc_apps.isnull().sum()

#Step 6. Preprocessing the data (part i)
# Import LabelEncoder
from sklearn.preprocessing import LabelEncoder
# Instantiate LabelEncoder
le = LabelEncoder()
# Iterate over all the values of each column and extract their dtypes
for col in range(0,14):
    # Compare if the dtype is object
    if cc_apps[col].dtypes=='object':
    # Use LabelEncoder to do the numeric transformation
        cc_apps[col]=le.fit_transform(cc_apps[col])

#Step 7. Splitting the dataset into train and test sets
# Import train_test_split
from sklearn.model_selection import train_test_split
# Drop the features 11 and 13 and convert the DataFrame to a NumPy array
cc_apps = cc_apps.drop([11,13], axis=1)
cc_apps = cc_apps.values

# Segregate features and labels into separate variables
X,y = cc_apps[:,0:-1] , cc_apps[:,-1]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                y,
                                test_size=0.33,
                                random_state= 42)

#Step 8. Preprocessing the data (part ii)
# Import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
# Instantiate MinMaxScaler and use it to rescale X_train and X_test
scaler = MinMaxScaler(feature_range=(0,1))
rescaledX_train = scaler.fit_transform(X_train)
rescaledX_test = scaler.fit_transform(X_test)

#Step 9. Fitting a logistic regression model to the train set
# Import LogisticRegression
from sklearn.linear_model import LogisticRegression
# Instantiate a LogisticRegression classifier with default parameter values
logreg = LogisticRegression()
# Fit logreg to the train set
logreg.fit(X_train,y_train)

#Step 10. Making predictions and evaluating performance
# Import confusion_matrix
from sklearn.metrics import confusion_matrix
# Use logreg to predict instances from the test set and store it
y_pred = logreg.predict(rescaledX_test)
# Get the accuracy score of logreg model and print it
#print("Accuracy of logistic regression classifier: ", score(y_test, rescaledX_test))
# Print the confusion matrix of the logreg model
cm = confusion_matrix(y_test, y_pred)
cm

#Step 11. Grid searching and making the model perform better
# Import GridSearchCV
from sklearn.model_selection import GridSearchCV
# Define the grid of values for tol and max_iter
tol = [0.01,0.001,0.0001]
max_iter = [100,150,200]
# Create a dictionary where tol and max_iter are keys and the lists of their values are corresponding values
param_grid = dict({'tol' : tol, 'max_iter' : max_iter})

#Step 12. Finding the best performing model
# Instantiate GridSearchCV with the required parameters
grid_model = GridSearchCV(estimator=logreg, param_grid=param_grid, cv=5)
# Use scaler to rescale X and assign it to rescaledX
rescaledX = scaler.fit_transform(X)
# Fit data to grid_model
grid_model_result = grid_model.fit(rescaledX, y)
# Summarize results
best_score, best_params = grid_model_result.best_score_, grid_model_result.best_params_
print("Best: %f using %s" % (best_score, best_params))

