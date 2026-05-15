# ============================================================
# Superannuation - Customer Churn Prediction
# ============================================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


# ------------------------------------------------------------
# Step 1: Load Dataset
# ------------------------------------------------------------

print("\nSTEP 1: Loading dataset...")

data = pd.read_csv("superannuation_churn_dataset.csv")

print("Dataset loaded successfully")
print("Total rows and columns:", data.shape)
print("\nFirst 5 rows:")
print(data.head())


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
    print("member_id column removed")

for col in data.columns:
    if pd.api.types.is_numeric_dtype(data[col]):
        if data[col].isnull().any():
            data[col] = data[col].fillna(data[col].median())
            print(f"Filled missing numeric values in {col}")
    else:
        if data[col].isnull().any():
            mode_val = data[col].mode()
            if len(mode_val) > 0:
                data[col] = data[col].fillna(mode_val[0])
                print(f"Filled missing text values in {col}")

print("Missing values handled successfully")


# ------------------------------------------------------------
# Step 4: Validate Target Column
# ------------------------------------------------------------

print("\nSTEP 4: Validating target column...")

if "churn" not in data.columns:
    raise ValueError("churn column not found in dataset")

print("churn column found")


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


# ------------------------------------------------------------
# Step 7: Split Input and Output
# ------------------------------------------------------------

print("\nSTEP 7: Splitting features and target...")

X = data.drop("churn", axis=1)
y = data["churn"]

print("Input columns used for prediction:")
print(X.columns.tolist())

print("\nTarget column: churn")
print("Churn value count:")
print(y.value_counts())


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


# ------------------------------------------------------------
# Step 9: Feature Scaling for Logistic Regression
# ------------------------------------------------------------

print("\nSTEP 9: Scaling data for Logistic Regression...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Scaling completed")


# ------------------------------------------------------------
# Step 10: Train Random Forest Model
# ------------------------------------------------------------

print("\nSTEP 10: Training Random Forest model...")

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

print("Random Forest training completed")


# ------------------------------------------------------------
# Step 11: Train Logistic Regression Model
# ------------------------------------------------------------

print("\nSTEP 11: Training Logistic Regression model...")

lr_model = LogisticRegression(max_iter=1000)

lr_model.fit(X_train_scaled, y_train)

print("Logistic Regression training completed")


# ------------------------------------------------------------
# Step 12: Evaluation Function
# ------------------------------------------------------------

def evaluate_model(model_name, y_test, y_pred):
    print("\n===================================================")
    print(f"{model_name} MODEL RESULTS")
    print("===================================================")

    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"\nAccuracy: {accuracy:.2f}%")

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report).transpose()

    for col in ["precision", "recall", "f1-score"]:
        report_df[col] = report_df[col] * 100

    report_df = report_df.round(2)

    print("\nClassification Report in Percentage:")
    print(report_df)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nMeaning:")
    print("0 = Customer will stay")
    print("1 = Customer may churn")


# ------------------------------------------------------------
# Step 13: Predict and Evaluate Random Forest
# ------------------------------------------------------------

print("\nSTEP 13: Predicting using Random Forest...")

rf_pred = rf_model.predict(X_test)

evaluate_model("Random Forest", y_test, rf_pred)


# ------------------------------------------------------------
# Step 14: Predict and Evaluate Logistic Regression
# ------------------------------------------------------------

print("\nSTEP 14: Predicting using Logistic Regression...")

lr_pred = lr_model.predict(X_test_scaled)

evaluate_model("Logistic Regression", y_test, lr_pred)


# ------------------------------------------------------------
# Step 15: Feature Importance from Random Forest
# ------------------------------------------------------------

print("\nSTEP 15: Finding important churn factors...")

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

print("\nTop important factors for churn:")
print(feature_importance)


# ------------------------------------------------------------
# Step 16: Predict One Customer Example
# ------------------------------------------------------------

# ------------------------------------------------------------
# Step 16: Predict One Customer Example
# ------------------------------------------------------------

print("\nSTEP 16: Predicting one sample customer...")

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

print("\nProgram completed successfully")