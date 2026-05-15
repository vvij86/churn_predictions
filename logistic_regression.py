# ============================================================
# Superannuation - Customer Churn Prediction
# Logistic Regression Only - Step by Step Learning Program
# ============================================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression


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
print("Training data is used to teach the model")
print("Testing data is used to check how well the model learned")

wait_for_user()


# ------------------------------------------------------------
# Step 9: Feature Scaling
# ------------------------------------------------------------

print("\nSTEP 9: Scaling data for Logistic Regression...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Scaling completed")

print("\nWhy scaling?")
print("Logistic Regression works better when all input columns are in similar scale")
print("Example: salary may be 50000, age may be 35, so scaling balances them")

wait_for_user()


# ------------------------------------------------------------
# Step 10: Train Logistic Regression Model
# ------------------------------------------------------------

print("\nSTEP 10: Training Logistic Regression model...")

lr_model = LogisticRegression(max_iter=1000)

lr_model.fit(X_train_scaled, y_train)

print("Logistic Regression training completed")

print("\nMeaning:")
print("The model has learned patterns from customer data")
print("It learned which factors may increase churn possibility")

wait_for_user()


# ------------------------------------------------------------
# Step 11: Predict Using Logistic Regression
# ------------------------------------------------------------

print("\nSTEP 11: Predicting using Logistic Regression...")

lr_pred = lr_model.predict(X_test_scaled)

print("Prediction completed")
print("\nFirst 10 predictions:")
print(lr_pred[:10])

wait_for_user()


# ------------------------------------------------------------
# Step 12: Evaluate Model
# ------------------------------------------------------------

print("\nSTEP 12: Evaluating Logistic Regression model...")

accuracy = accuracy_score(y_test, lr_pred) * 100

print(f"\nAccuracy: {accuracy:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, lr_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, lr_pred))

print("\nMeaning:")
print("Accuracy tells overall correct predictions")
print("Precision tells how many predicted churn customers are actually churn")
print("Recall tells how many actual churn customers were correctly found")
print("Confusion matrix shows correct and wrong predictions")

wait_for_user()


# ------------------------------------------------------------
# Step 13: Show Logistic Regression Coefficients
# ------------------------------------------------------------

print("\nSTEP 13: Showing important factors from Logistic Regression...")

coefficients = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": lr_model.coef_[0]
})

coefficients["Absolute_Impact"] = coefficients["Coefficient"].abs()

coefficients = coefficients.sort_values(
    by="Absolute_Impact",
    ascending=False
)

print("\nImportant factors based on Logistic Regression:")
print(coefficients)

print("\nMeaning:")
print("Positive coefficient means it increases churn possibility")
print("Negative coefficient means it reduces churn possibility")
print("Higher absolute value means stronger impact")

wait_for_user()


# ------------------------------------------------------------
# Step 14: Predict One Sample Customer
# ------------------------------------------------------------

print("\nSTEP 14: Predicting one sample customer...")

sample_customer = X_test.iloc[[0]]

print("\nSample Customer Details:")
print(sample_customer)

sample_customer_scaled = scaler.transform(sample_customer)

prediction = lr_model.predict(sample_customer_scaled)[0]
prediction_probability = lr_model.predict_proba(sample_customer_scaled)[0]

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
# Step 15: Final Summary
# ------------------------------------------------------------

print("\nSTEP 15: Final Summary")

print("""
This program completed the following:

1. Loaded the customer churn dataset
2. Checked columns, data types and missing values
3. Cleaned duplicate and missing data
4. Converted churn column into 0 and 1
5. Converted text columns into numbers
6. Split data into training and testing
7. Scaled input data
8. Trained Logistic Regression model
9. Predicted churn customers
10. Evaluated model accuracy
11. Showed important churn factors
12. Predicted one sample customer
""")

print("Program completed successfully")