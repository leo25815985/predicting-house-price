# -*- coding: utf-8 -*-
"""housing price prediction

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LVIkRuk5Vd2YlaAAQh61Lkldw1AHl1DT
"""

!pip install pandas
!pip install scikit-learn==1.3.0
!pip install numpy
!pip install matplotlib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

# Load the dataset
data = pd.read_csv("Housing.csv")

# Basic exploration
print(data.head())
#print(data.info())
#print(data.describe())

# Map categorical values to numerical
mapping = {
    'yes': 1,
    'no': 0,
    'furnished': 1,
    'semi-furnished': 0.5,
    'unfurnished': 0
}
data = data.replace(mapping)

# Handle missing values
data = data.fillna(data.median())

# Convert categorical variables (if any)
data = pd.get_dummies(data, drop_first=True)

# Split the data
X = data.drop('price', axis=1)
y = data['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Fit the model
model = LinearRegression()
cv_scores = cross_val_score(model, X, y, cv=5)  # X is features, y is target

print("Cross-validation scores:", cv_scores)
print("Average score:", cv_scores.mean())

# Fit the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data = pd.read_csv("Housing.csv")

# Identify numeric and categorical columns
numeric_features = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
categorical_features = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']

# Split the data
X = data.drop('price', axis=1)
y = data['price']

# Remove outliers
z_scores = np.abs((y - y.mean()) / y.std())
X = X[z_scores < 3]
y = y[z_scores < 3]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create preprocessing steps
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create a pipeline that combines preprocessing and model
models = {
    'RandomForest': RandomForestRegressor(random_state=42),
    'GradientBoosting': GradientBoostingRegressor(random_state=42)
}

param_grids = {
    'RandomForest': {'model__n_estimators': [100, 200, 300], 'model__max_depth': [10, 20, 30, None]},
    'GradientBoosting': {'model__n_estimators': [100, 200], 'model__learning_rate': [0.01, 0.1], 'model__max_depth': [3, 5]}
}

best_model = None
best_score = float('-inf')

for name, model in models.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    grid_search = GridSearchCV(pipeline, param_grids[name], cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)

    if -grid_search.best_score_ > best_score:
        best_score = -grid_search.best_score_
        best_model = grid_search.best_estimator_

# Final evaluation
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Best model: {type(best_model.named_steps['model']).__name__}")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Feature importance (for tree-based models)
if hasattr(best_model.named_steps['model'], 'feature_importances_'):
    importances = best_model.named_steps['model'].feature_importances_
    feature_names = best_model.named_steps['preprocessor'].get_feature_names_out()
    for name, importance in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
        print(f"{name}: {importance}")