import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Load the dataset
data = pd.read_csv(StringIO("""Weight,Height,BMI,Gender,Age,BMIcase,Exercise Recommendation Plan
92.0851902,1.760249514,29.71948799,Female,59,over weight,5
61.08912444,1.595498708,23.99777555,Female,25,normal,4
82.45403663,1.816538313,24.98749946,Female,50,normal,4
101.7133061,1.790696455,31.72004707,Female,62,obese,6
99.60952716,1.969725632,25.67375577,Male,57,over weight,5
..."""))  # Truncated for brevity; assumes full dataset is loaded

# Preprocessing
# Encode categorical variables
le_gender = LabelEncoder()
data['Gender'] = le_gender.fit_transform(data['Gender'])

# One-hot encode BMIcase
data = pd.get_dummies(data, columns=['BMIcase'], prefix='BMIcase')

# Define features and target
features = ['Weight', 'Height', 'BMI', 'Gender', 'Age'] + [col for col in data.columns if col.startswith('BMIcase_')]
X = data[features]
y = data['Exercise Recommendation Plan']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize models
models = {
    'SVM': SVC(kernel='linear', random_state=42),
    'Logistic Regression': LogisticRegression(multi_class='multinomial', max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Linear Regression': LinearRegression()
}

# Evaluate models
results = []
confusion_matrices = {}
feature_importances = {}

for name, model in models.items():
    if name == 'Linear Regression':
        # Train and predict with Linear Regression
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_pred_rounded = np.round(y_pred).astype(int)  # Round predictions to nearest integer
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred_rounded)
        precision = precision_score(y_test, y_pred_rounded, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred_rounded, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred_rounded, average='weighted', zero_division=0)
        results.append({
            'Model': name,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1,
            'MSE': mse,
            'R2': r2
        })
    else:
        # Train and predict with classification models
        model.fit(X_train_scaled if name in ['SVM', 'Logistic Regression'] else X_train, y_train)
        y_pred = model.predict(X_test_scaled if name in ['SVM', 'Logistic Regression'] else X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        results.append({
            'Model': name,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1,
            'MSE': None,
            'R2': None
        })
        # Store confusion matrix
        confusion_matrices[name] = confusion_matrix(y_test, y_pred)
        # Store feature importance for tree-based models
        if name in ['Random Forest', 'Decision Tree']:
            feature_importances[name] = model.feature_importances_

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Plot model performance comparison
plt.figure(figsize=(10, 6))
sns.barplot(x='Model', y='Accuracy', data=results_df)
plt.title('Model Accuracy Comparison')
plt.ylabel('Accuracy')
plt.xlabel('Model')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('model_comparison.png')
plt.close()

# Plot confusion matrices
for name, cm in confusion_matrices.items():
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix for {name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(f'confusion_matrix_{name.lower().replace(" ", "_")}.png')
    plt.close()

# Plot feature importance for Random Forest and Decision Tree
for name, importances in feature_importances.items():
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances, y=features)
    plt.title(f'Feature Importance for {name}')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.savefig(f'feature_importance_{name.lower().replace(" ", "_")}.png')
    plt.close()

# Print results
print("Model Performance Summary:")
print(results_df)