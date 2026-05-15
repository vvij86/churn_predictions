import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# Load dataset
data = pd.read_csv("superannuation_customers.csv")

# Convert text columns into numbers
le = LabelEncoder()

data['Account_Type'] = le.fit_transform(data['Account_Type'])
data['Email_Engagement'] = le.fit_transform(data['Email_Engagement'])
data['Churn'] = le.fit_transform(data['Churn'])

# Features and target
X = data[['Age', 'Balance', 'Contribution',
          'Account_Type', 'Complaints',
          'Login_Frequency', 'Email_Engagement',
          'Support_Calls']]

y = data['Churn']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred) * 100

print("\n===== CUSTOMER CHURN MODEL RESULTS =====\n")
print(f"Overall Accuracy : {accuracy:.2f}%")

# Classification report
report = classification_report(
    y_test,
    y_pred,
    output_dict=True
)

# Convert report into dataframe
report_df = pd.DataFrame(report).transpose()

# Convert metrics into percentage
for col in ['precision', 'recall', 'f1-score']:
    report_df[col] = report_df[col] * 100

# Round values
report_df = report_df.round(2)

print("\n===== CLASSIFICATION REPORT TABLE =====\n")

print(report_df)