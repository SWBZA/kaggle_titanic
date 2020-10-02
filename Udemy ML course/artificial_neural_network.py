# -*- coding: utf-8 -*-
"""artificial_neural_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_Qu3gUBYUB_SrNGqrR7Hw4UNyvd55PsH

# Artificial Neural Network

### Importing the libraries
"""

import numpy as np
import pandas as pd
import tensorflow as tf

tf.__version__

"""## Part 1 - Data Preprocessing

### Importing the dataset
"""

dataset = pd.read_csv('train.csv')
X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, 0].values

"""### Taking care of missing data"""

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X)
X = imputer.transform(X)

"""### Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""### Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""## Part 2 - Building the ANN

### Initializing the ANN
"""

ann = tf.keras.models.Sequential()

"""### Adding the input layer and the first hidden layer"""

ann.add(tf.keras.layers.Dense(units=7, activation='relu'))

"""### Adding the second hidden layer"""

ann.add(tf.keras.layers.Dense(units=2, activation='relu'))

"""### Adding the output layer"""

ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

"""## Part 3 - Training the ANN

### Compiling the ANN
"""

ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
#SGD
#RMSprop
#Adam
#Adadelta
#Adagrad
#Adamax
#Nadam
#Ftrl

"""### Training the ANN on the Training set"""

ann.fit(X_train, y_train, batch_size = 32, epochs = 1000)

"""## Part 4 - Making the predictions and evaluating the model

### Making a prediction on the test set
"""

y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.75)

"""### Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

"""## Making competition prediction"""

# Import data
dataset = pd.read_csv('test.csv')
X_competition = dataset.iloc[:, 1:-1].values

# Take care of missing data
imputer_comp = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer_comp.fit(X_competition)
X_competition = imputer.transform(X_competition)

# Scale features
X_competition = sc.fit_transform(X_competition)

# Make prediction on competition test set using trained model
y_pred = ann.predict(X_competition)
y_pred = (y_pred > 0.5)
y_competition = pd.DataFrame(y_pred)
y_competition = y_competition*1 # Change booleans to 1 / 0

# Concatenate prediction and passenger ID columns
submission = pd.DataFrame(
    pd.concat([dataset.iloc[:, 0],  y_competition.iloc[:, :]], axis=1))

# Fix column headings
submission.columns = ['PassengerID', 'Survived']

# Write to file
submission.to_csv('NeuralNet.csv', index=False)

