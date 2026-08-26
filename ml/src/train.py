import pandas as pd
from .features import create_features

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import joblib

# from sklearn.ensemble import RandomForestRegressor
# from sklearn.linear_model import Ridge
# from sklearn.linear_model import Lasso

# from xgboost import XGBRegressor

featured_df = create_features("ml/data/raw/ramradar-price-index.csv")

# FOR ONEHOTENCORDER
# fit          → learn
# transform    → convert
# fit_transform → learn + convert

categorical = [
    "ram_type", 
    "form_factor"
]

numerical = [
    "previous_price", 
    "prev_7_day_price", 
    "prev_month_price", 
    "prev_7_day_price_avg", 
    "prev_month_price_avg",
    "price_diff_1_d",
    "prce_diff_1_d_pct",
    "7d_displacement"
]

preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(), categorical),
        ("numerical", "passthrough", numerical)
    ]
)

X = featured_df[categorical + numerical]

y = featured_df["avg_price_per_gb"]

# reg = LinearRegression() # this is a class
# reg.fit(X, y)
# score = reg.score(X, y) 
# R^2 score is how much of the variation did the model explain also called Coeff of Determination
# R^2 = 1 perfect prediction R^2 = 0 just predicting the avg of all R^2 < 0 worse than the baseline
# when i ran the print below got R^2 score: 0.9834 which on paper is very good but for time vs price it is sus
# why -> most of the prev day price == today's price so the model will essentially predict it 
# so we split the data into 80% of training data and 20% future as testing data then check the score
# print(f"R^2 score: {score:.4f}")

# SPLITTING DATASET INTO 80:20 TRAIN:TEST 
split_idx = int(len(featured_df) * 0.8)
X_train = X.iloc[:split_idx] # iloc is just integer location for dataframes in pandas same as index in arrays since we use row names but we are using split index
X_test = X.iloc[split_idx:]
y_train = y.iloc[:split_idx]
y_test = y.iloc[split_idx:]

# ML MODEL
model = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)
model.fit(X_train, y_train)

# R^2 SCORE
trainScore = model.score(X_train, y_train)
testScore = model.score(X_test, y_test) # what i am interested in this is the future prediction
print(f"R^2 Score of Trained Data: {trainScore:.4f}") # score : 0.9832 or 98.32% accuracy in predicting the training variation
print(f"R^2 Score of Tested Data: {testScore:.4f}") # score : 0.8319 or 83.19% accuracy prediction in future data

# MAE - Mean Absolute Error - simply the average absolute difference between actual and predicted values.
# RMSE — Root Mean Squared Error - does almost the same thing, but penalizes large errors more heavily. 
# NOTE - RMSE >= MAE always

y_train_prediction = model.predict(X_train)
y_test_prediction = model.predict(X_test)

train_mae = mean_absolute_error(y_train, y_train_prediction)
train_rmse = root_mean_squared_error(y_train, y_train_prediction)

test_mae = mean_absolute_error(y_test, y_test_prediction)
test_rmse = root_mean_squared_error(y_test, y_test_prediction)

print("----TRAIN SCORE----")
print(f"MAE Score: {train_mae:.4f}")
print(f"RMSE Score: {train_rmse:.4f}")
print("----TEST SCORE----")
print(f"MAE Score: {test_mae:.4f}")
print(f"RMSE Score: {test_rmse:.4f}")

# RANDOM FOREST REGRESSION 
# NOTE - Decision-tree-based models like Random Forest cannot extrapolate values higher or lower than the minimum/maximum 
# targets seen in y_train. If price trends in y_test reach brand-new historical highs or lows, Random Forest will flatten 
# its predictions at the boundary.
# n_estimators=100 => it is number of trees in the forest each tree is a prediction and all predictions are combined
# More trees generally make the model more stable, but increase training time.
# max_depth=2 => Controls how deep each decision tree is allowed to grow. max_depth=3 means the tree can have at most 3 levels of decisions.
# max_depth=None => means the trees can keep growing until their stopping conditions are reached. this makes the model very good but
# also makes it "overfit" no idea what this means for now
# Random Forest uses randomness when constructing its trees. random_state gives that randomness a fixed starting point.

# Worse than Linear Regression

# rf_model = RandomForestRegressor(n_estimators=100, max_depth = 5, random_state=42)
# rf_model.fit(X_train, y_train)

# y_train_prediction_rf = rf_model.predict(X_train)
# y_test_prediction_rf = rf_model.predict(X_test)

# train_rf_r2 = rf_model.score(X_train, y_train)
# train_rf_mae = mean_absolute_error(y_train, y_train_prediction_rf)
# train_rf_rmse = root_mean_squared_error(y_train, y_train_prediction_rf)

# test_rf_r2 = rf_model.score(X_test, y_test)
# test_rf_mae = mean_absolute_error(y_test, y_test_prediction_rf)
# test_rf_rmse = root_mean_squared_error(y_test, y_test_prediction_rf)

# print("----TRAIN SCORE RF----")
# print(f"R^2 Score: {train_rf_r2: .4f}")
# print(f"MAE Score: {train_rf_mae: .4f}")
# print(f"RMSE Score: {train_rf_rmse: .4f}")
# print("----TEST SCORE RF----")
# print(f"R^2 Score: {test_rf_r2: .4f}")
# print(f"MAE Score: {test_rf_mae: .4f}")
# print(f"RMSE Score: {test_rf_rmse: .4f}")

"""
Since linear models can naturally extrapolate trends beyond historical min/max values, your best move for predicting absolute 
prices is regularized linear regression.Regularization adds a penalty to prevent correlated features 
(prev_7_day_price_avg, prev_month_price_avg) from causing high variance.

Ridge Regression ($L_2$ Penalty): Shrinks feature weights to stabilize correlated inputs without dropping them completely.
alpha = 0       → essentially Linear Regression
alpha = 0.01    → very weak regularization
alpha = 1       → moderate
alpha = 10      → stronger
alpha = 100     → very strong

Lasso Regression ($L_1$ Penalty): Drives redundant feature weights to exact zero, performing automatic feature selection.
alpha = 0.001  → very weak regularization
alpha = 0.01   → weak
alpha = 0.1    → moderate
alpha = 1      → strong
alpha = 10     → very strong
alpha = 100    → extremely strong

Ridge → shrinks coefficients toward 0
Lasso → can shrink coefficients all the way to 0
"""

# ridge = Ridge(alpha = 1) # at alpha = 1 0.806 < Linear Regression at alpha = 10 0.8195 < Linear Regression
# ridge.fit(X_train, y_train)
# print(f"Ridge R^2 Score: {ridge.score(X_test, y_test) : .4f}")

# lasso = Lasso(alpha=0.01) # at alpha = 0.8326 > Linear Regression so slightly better than Linear
# lasso.fit(X_train, y_train)
# print(f"Lasso R^2 Score: {lasso.score(X_test, y_test) : .4f}")

# print("\n\n\n")

# Match feature names with learned coefficients
# coef_df = pd.DataFrame({
#     'Feature': X.columns,
#     'Coefficient': lasso.coef_
# }).sort_values(by='Coefficient', ascending=False)

# print(coef_df)
# print(f"Intercept: {lasso.intercept_:.4f}")

# DecisionTreeRegressor - A Decision Tree splits your feature space into a series of orthogonal, axis-aligned rectangular boxes 
# using binary IF/THEN rules 
# (e.g., IF previous_price > 12.50 AND prev_7_day_price_avg <= 11.20).
# To make a prediction for a target value $y$, the tree routes a sample down through its branches until it lands in a terminal node 
# (leaf). The predicted value is simply the average of all training samples that landed inside that exact leaf node.

# XGBoost - Extreme Gradient Boosting -> Unlike a Random Forest (which builds many independent trees in parallel and averages them),
# XGBoost builds trees sequentially. 

# xgb_model = XGBRegressor(n_estimators = 100, max_depth = 3, learning_rate = 0.05, random_state = 42)
# # learning rate is the shriking factor 

# xgb_model.fit(X_train, y_train)

# print("----XGBoost----")
# print(f"R^2 Score: {xgb_model.score(X_test, y_test): .4f}") # -2.9598 super bad 

# Since all models are worse than LR we go with LR

results = pd.DataFrame(
    {
        "actual_price" : y_test,
        "predicted_price" : y_test_prediction
    }
)

results["error"] = abs(
    results["actual_price"] - results["predicted_price"]
)


results.sort_values("error", ascending=False)

results.reset_index(drop=True)

joblib.dump(model, "ml/models/linearRegressionModel.pkl")

# print(results.head(30))