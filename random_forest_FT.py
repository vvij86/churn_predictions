# ============================================================
# Superannuation - Customer Churn Prediction
# Improved Random Forest Only - Step by Step Learning Program
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
# Step 9: Train Improved Random Forest Model
# ------------------------------------------------------------

print("\nSTEP 9: Training Improved Random Forest model...")

rf_model = RandomForestClassifier(
    n_estimators=300,
    criterion="gini",
    max_depth=8,
    min_samples_split=10,
    min_samples_leaf=3,
    max_features="sqrt",
    class_weight="balanced",
    random_state=42
)

rf_model.fit(X_train, y_train)

print("Improved Random Forest training completed")

print("\nMeaning:")
print("n_estimators=300 means 300 decision trees are created")
print("max_depth=8 controls tree depth and reduces overfitting")
print("min_samples_split=10 means split only when enough records are available")
print("min_samples_leaf=3 avoids very tiny leaf decisions")
print("max_features='sqrt' makes each tree use different feature combinations")
print("class_weight='balanced' gives more importance to churn customers")

wait_for_user()


# ------------------------------------------------------------
# Step 10: Predict Using Probability Threshold
# ------------------------------------------------------------

print("\nSTEP 10: Predicting using Random Forest with custom threshold...")

rf_probabilities = rf_model.predict_proba(X_test)

# Probability of churn class 1
churn_probabilities = rf_probabilities[:, 1]

# Default threshold is 0.50
# Lower threshold catches more churn customers
threshold = 0.35

rf_pred = (churn_probabilities >= threshold).astype(int)

print("Prediction completed")

print("\nThreshold used:", threshold)
print("If churn probability is >= 35%, we classify customer as churn")

print("\nFirst 10 churn probabilities:")
print(churn_probabilities[:10])

print("\nFirst 10 predictions:")
print(rf_pred[:10])

print("\nMeaning:")
print("0 = Model predicted customer will stay")
print("1 = Model predicted customer may churn")

wait_for_user()


# ------------------------------------------------------------
# Step 11: Evaluate Improved Random Forest Model
# ------------------------------------------------------------

print("\nSTEP 11: Evaluating Improved Random Forest model...")

accuracy = accuracy_score(y_test, rf_pred) * 100

print(f"\nAccuracy: {accuracy:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, rf_pred, zero_division=0))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, rf_pred)
print(cm)

tn, fp, fn, tp = cm.ravel()

print("\nConfusion Matrix Meaning:")
print("[[Correct Stay, Wrong Churn Alert],")
print(" [Missed Churn, Correct Churn]]")

print("\nDetailed Meaning:")
print("Correct Stay        :", tn)
print("Wrong Churn Alert   :", fp)
print("Missed Churn        :", fn)
print("Correct Churn       :", tp)

print("\nAccuracy Calculation:")
print(f"Correct predictions = {tn} + {tp} = {tn + tp}")
print(f"Total predictions   = {tn} + {fp} + {fn} + {tp} = {tn + fp + fn + tp}")
print(f"Accuracy            = {(tn + tp)} / {(tn + fp + fn + tp)}")
print(f"Accuracy Percentage = {accuracy:.2f}%")

print("\nImportant for churn project:")
print("Try to reduce Missed Churn")
print("Try to increase Correct Churn")

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
print("Random Forest calculates this using many decision trees")

wait_for_user()


# ------------------------------------------------------------
# Step 13: Compare Different Thresholds
# ------------------------------------------------------------

print("\nSTEP 13: Comparing different threshold values...")

threshold_list = [0.50, 0.45, 0.40, 0.35, 0.30]

for th in threshold_list:
    temp_pred = (churn_probabilities >= th).astype(int)
    temp_cm = confusion_matrix(y_test, temp_pred)
    temp_tn, temp_fp, temp_fn, temp_tp = temp_cm.ravel()

    temp_accuracy = accuracy_score(y_test, temp_pred) * 100

    print("\n------------------------------------------")
    print("Threshold:", th)
    print("Accuracy:", round(temp_accuracy, 2), "%")
    print("Confusion Matrix:")
    print(temp_cm)
    print("Correct Stay      :", temp_tn)
    print("Wrong Churn Alert :", temp_fp)
    print("Missed Churn      :", temp_fn)
    print("Correct Churn     :", temp_tp)

print("\nMeaning:")
print("Threshold 0.50 gives fewer churn alerts")
print("Threshold 0.35 or 0.30 catches more churn customers")
print("But lower threshold may increase wrong churn alerts")

wait_for_user()


# ------------------------------------------------------------
# Step 14: Predict One Sample Customer
# ------------------------------------------------------------

print("\nSTEP 14: Predicting one sample customer...")

sample_customer = X_test.iloc[[0]]

print("\nSample Customer Details:")
print(sample_customer)

sample_probability = rf_model.predict_proba(sample_customer)[0]

stay_probability = sample_probability[0] * 100
churn_probability = sample_probability[1] * 100

print("\nPrediction Probability:")
print(f"Stay Probability  : {stay_probability:.2f}%")
print(f"Churn Probability : {churn_probability:.2f}%")

if churn_probability >= threshold * 100:
    print("\nPrediction: This customer may CHURN")
else:
    print("\nPrediction: This customer may STAY")

print("\nThreshold used for this decision:", threshold)

wait_for_user()


# ------------------------------------------------------------
# Step 15: Final Summary
# ------------------------------------------------------------

print("\nSTEP 15: Final Summary")

print("""
This Improved Random Forest program completed the following:

1. Loaded the customer churn dataset
2. Checked columns, data types and missing values
3. Cleaned duplicate and missing data
4. Converted churn column into 0 and 1
5. Converted text columns into numbers
6. Split data into training and testing
7. Trained improved Random Forest model
8. Used class_weight='balanced' for churn class importance
9. Used probability threshold instead of default prediction
10. Evaluated model accuracy
11. Displayed confusion matrix with detailed meaning
12. Displayed important churn factors
13. Compared multiple threshold values
14. Predicted one sample customer
""")

print("Program completed successfully")