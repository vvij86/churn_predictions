# ============================================================
# Superannuation - Customer Churn Prediction
# Random Forest Only - Step by Step Learning Program
# ============================================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier


def wait_for_user():
    input("\nPress ENTER to continue to next step...")


# ------------------------------------------------------------
# Step 1: Load Dataset
# ------------------------------------------------------------

print("\nSTEP 1: Loading dataset...")

data = pd.read_csv("superannuation_churn_dataset.csv")

print("Dataset loaded successfully")
print("Total rows and columns:", data.shape)

print("\nFirst 5 rows:")
print(data.head())

wait_for_user()


# ------------------------------------------------------------
# Step 2: Basic Data Understanding
# ------------------------------------------------------------

print("\nSTEP 2: Understanding dataset...")

print("\nColumn names:")
print(data.columns.tolist())

print("\nData types:")
print(data.dtypes)

print("\nMissing values:")
print(data.isnull().sum())

wait_for_user()


# ------------------------------------------------------------
# Step 3: Data Cleaning
# ------------------------------------------------------------

print("\nSTEP 3: Cleaning dataset...")

before_duplicates = data.shape[0]
data = data.drop_duplicates()
after_duplicates = data.shape[0]

print("Duplicate rows removed:", before_duplicates - after_duplicates)

if "member_id" in data.columns:
    data = data.drop("member_id", axis=1)
    print("member_id column removed because it is only an ID, not useful for prediction")

for col in data.columns:
    if pd.api.types.is_numeric_dtype(data[col]):
        if data[col].isnull().any():
            data[col] = data[col].fillna(data[col].median())
            print(f"Filled missing numeric values in {col} using median")
    else:
        if data[col].isnull().any():
            mode_val = data[col].mode()
            if len(mode_val) > 0:
                data[col] = data[col].fillna(mode_val[0])
                print(f"Filled missing text values in {col} using most common value")

print("Missing values handled successfully")

wait_for_user()


# ------------------------------------------------------------
# Step 4: Validate Target Column
# ------------------------------------------------------------

print("\nSTEP 4: Validating target column...")

if "churn" not in data.columns:
    raise ValueError("churn column not found in dataset")

print("churn column found")
print("This is the output column we are trying to predict")

wait_for_user()


# ------------------------------------------------------------
# Step 5: Convert Target Column to 0 and 1
# ------------------------------------------------------------

print("\nSTEP 5: Converting churn column...")

if not pd.api.types.is_numeric_dtype(data["churn"]):
    data["churn"] = data["churn"].astype(str).str.strip().str.lower()

    data["churn"] = data["churn"].map({
        "no": 0,
        "yes": 1,
        "stay": 0,
        "churn": 1
    })

if data["churn"].isnull().any():
    raise ValueError("Some churn values could not be converted. Please check churn column values.")

data["churn"] = data["churn"].astype(int)

print("Target churn column converted successfully")
print("0 = Customer will stay")
print("1 = Customer may churn")

print("\nChurn value count:")
print(data["churn"].value_counts())

wait_for_user()


# ------------------------------------------------------------
# Step 6: Encode Categorical Input Columns
# ------------------------------------------------------------

print("\nSTEP 6: Encoding categorical input columns...")

label_encoders = {}

for col in data.columns:
    if col == "churn":
        continue

    if not pd.api.types.is_numeric_dtype(data[col]):
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le
        print(f"Encoded column: {col}")

print("Categorical encoding completed")
print("Text values are converted into numbers because ML model understands numbers only")

wait_for_user()


# ------------------------------------------------------------
# Step 7: Split Input and Output
# ------------------------------------------------------------

print("\nSTEP 7: Splitting features and target...")

X = data.drop("churn", axis=1)
y = data["churn"]

print("Input columns used for prediction:")
print(X.columns.tolist())

print("\nTarget column: churn")
print("0 = Stay")
print("1 = Churn")

wait_for_user()


# ------------------------------------------------------------
# Step 8: Train-Test Split
# ------------------------------------------------------------

print("\nSTEP 8: Splitting data into training and testing...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training records:", X_train.shape[0])
print("Testing records:", X_test.shape[0])

print("\nMeaning:")
print("Training data is used to teach the Random Forest model")
print("Testing data is used to check how well the model predicts unseen customers")

wait_for_user()


# ------------------------------------------------------------
# Step 9: Train Random Forest Model
# ------------------------------------------------------------

print("\nSTEP 9: Training Random Forest model...")

rf_model = RandomForestClassifier(
    n_estimators=100,
    criterion="gini",
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    class_weight="balanced"
)

rf_model.fit(X_train, y_train)

print("Random Forest training completed")

print("\nMeaning:")
print("Random Forest creates many Decision Trees")
print("Each tree gives one prediction")
print("Final prediction is decided by majority voting")
print("This usually reduces overfitting compared to a single Decision Tree")

wait_for_user()


# ------------------------------------------------------------
# Step 10: Predict Using Random Forest
# ------------------------------------------------------------

print("\nSTEP 10: Predicting using Random Forest...")

rf_pred = rf_model.predict(X_test)

print("Prediction completed")

print("\nFirst 10 predictions:")
print(rf_pred[:10])

print("\nMeaning:")
print("0 = Model predicted customer will stay")
print("1 = Model predicted customer may churn")

wait_for_user()


# ------------------------------------------------------------
# Step 11: Evaluate Random Forest Model
# ------------------------------------------------------------

print("\nSTEP 11: Evaluating Random Forest model...")

accuracy = accuracy_score(y_test, rf_pred) * 100

print(f"\nAccuracy: {accuracy:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, rf_pred, zero_division=0))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, rf_pred)
print(cm)

print("\nConfusion Matrix Meaning:")
print("[[Correct Stay, Wrong Churn Alert],")
print(" [Missed Churn, Correct Churn]]")

print("\nFor your output:")
print("Top-left     = Actual Stay, Predicted Stay")
print("Top-right    = Actual Stay, Predicted Churn")
print("Bottom-left  = Actual Churn, Predicted Stay")
print("Bottom-right = Actual Churn, Predicted Churn")

print("\nAccuracy Calculation:")
print("Accuracy = Correct predictions / Total predictions")
print("Correct predictions = Top-left + Bottom-right")

wait_for_user()


# ------------------------------------------------------------
# Step 12: Feature Importance
# ------------------------------------------------------------

print("\nSTEP 12: Finding important churn factors...")

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

feature_importance["Importance_Percentage"] = (
    feature_importance["Importance"] * 100
).round(2)

print("\nImportant factors for churn:")
print(feature_importance)

print("\nMeaning:")
print("Higher importance means that column helped more in predicting churn")
print("Random Forest calculates this by checking which columns reduce prediction errors across many trees")

wait_for_user()


# ------------------------------------------------------------
# Step 13: Predict One Sample Customer
# ------------------------------------------------------------

print("\nSTEP 13: Predicting one sample customer...")

sample_customer = X_test.iloc[[0]]

print("\nSample Customer Details:")
print(sample_customer)

prediction = rf_model.predict(sample_customer)[0]
prediction_probability = rf_model.predict_proba(sample_customer)[0]

stay_probability = prediction_probability[0] * 100
churn_probability = prediction_probability[1] * 100

print("\nPrediction Result:")

if prediction == 1:
    print("Prediction: This customer may CHURN")
else:
    print("Prediction: This customer may STAY")

print(f"Stay Probability  : {stay_probability:.2f}%")
print(f"Churn Probability : {churn_probability:.2f}%")

wait_for_user()


# ------------------------------------------------------------
# Step 14: Final Summary
# ------------------------------------------------------------

print("\nSTEP 14: Final Summary")

print("""
This Random Forest program completed the following:

1. Loaded the customer churn dataset
2. Checked columns, data types and missing values
3. Cleaned duplicate and missing data
4. Converted churn column into 0 and 1
5. Converted text columns into numbers
6. Split data into training and testing
7. Trained Random Forest model
8. Predicted churn customers
9. Evaluated model accuracy
10. Displayed confusion matrix
11. Displayed important churn factors
12. Predicted one sample customer
""")

print("Program completed successfully")