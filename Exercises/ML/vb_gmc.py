'''
Variational Bayesian interface for Gaussian Mixture

This exercise is from GeeksForGeeks with the same title
The needed dataset is on Kaggle
'''

###   Importing the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.mixture import BayesianGaussianMixture
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.decomposition import PCA

### loading and cleaning the data

# load
X = pd.read_csv('CC_GENERAL.csv')

# Fropping the CUST_ID column from the data
X = X.drop('CUST_ID', axis=1)

# Handling the missing values
X.fillna(method = 'ffill', inplace = True)

X.head()

### Pre-processing the data

# scaling the data to bring all the attributes to a comparable level
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Normalize the data so that the data approx. follows a Gaussian distrib.
X_normalized = normalize(X_scaled)

# Converting the numpy array into pandas DataFrame
X_normalized = pd.DataFrame(X_normalized)

# Renaming the columns
X_normalized.columns = X.columns

X_normalized.head()

### Reducing the dimensionality of the data to make it visualizable

# Reducing the dimensions of the data
pca = PCA(n_components = 2)
X_principal = pca.fit_transform(X_normalized)

# Converting the reduced data into a pandas dataframe
X_principal = pd.DataFrame(X_principal)

# Renaming the columns
X_principal.columns = ['P1','P2']

X_principal.head()

### Building clustering models for different values of covariance_type
# covariance_type = 'full'
# Building and training the model
vbgm_model_full = BayesianGaussianMixture(n_components = 5,
                                          covariance_type = 'full')
vbgm_model_full.fit(X_normalized)

# Storing the labels
labels_full = vbgm_model_full.predict(X)
print(set(labels_full))

colors = {}
colors[0] = 'r'
colors[1] = 'g'
colors[2] = 'b'
colors[3] = 'k'

# Building the color vector for each data point
cvec = [colors[label] for label in labels_full]

# Defining the scatter plot for each color
r = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'r');
g = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'g');
b = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'b');
k = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'k');

# plotting the clustered data
plt.figure(figsize = (9,9))
plt.scatter(X_principal['P1'], X_principal['P2'], c = cvec)
plt.legend((r,g,b,k), ('label 0', 'label 1', 'label 2', 'label 3'))
plt.show()

# covariance_type = 'tied'
# building and training model
vbgm_model_tied = BayesianGaussianMisxture(n_components = 5,
                                           covariance_type = 'tied')
vbgm_model_tied.fit(X_normalized)

# Storing the labels
labels_tied = vbgm_model_tied.predict(X)
print(set(labels_tied))

colors = {}
colors[0] = 'r'
colors[1] = 'g'
colors[2] = 'b'
colors[3] = 'k'

# Building the color vector for each data point
cvec = [colors[label] for label in labels_tied]

# Defining the scatter plot for each color
r = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'r');
g = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'g');
b = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'b');
k = plt.scatter(X_principal['P1'], X_principal['P2'], color = 'k');

# Plotting the clustered data
plt.figure(figsize = (9,9))
plt.scatter(X_principal['P1'], X_principal['P2'], c = cvec)
plt.legend((r, g, b, k), ('label 0', 'label 2', 'label 3', 'label 4'))
plt.show()
