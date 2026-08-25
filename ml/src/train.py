import pandas as pd
from features import create_features

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

featured_df = create_features("ml/data/raw/ramradar-price-index.csv")

X = featured_df[
        [
            "previous_price", 
            "prev_7_day_price", 
            "prev_month_price", 
            "prev_7_day_price_avg", 
            "prev_month_price_avg"
        ]
    ]

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
model = LinearRegression()
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