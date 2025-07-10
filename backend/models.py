from django.db import models

# Create your models here.
# model.py (in your Django project folder)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_fitness_model():
    # Load the dataset
    df = pd.read_csv("final_dataset.xlsx.csv")

    # Encode categorical columns
    le_gender = LabelEncoder()
    le_bmicase = LabelEncoder()
    df['Gender'] = le_gender.fit_transform(df['Gender'])
    df['BMIcase'] = le_bmicase.fit_transform(df['BMIcase'])

    # Features and target
    X = df[['Weight', 'Height', 'BMI', 'Gender', 'Age', 'BMIcase']]
    y = df['Exercise Recommendation Plan']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Create a folder to save model files if it doesn't exist
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)

    # Save the model and encoders
    joblib.dump(model, os.path.join(model_dir, 'fitness_model.pkl'))
    joblib.dump(le_gender, os.path.join(model_dir, 'gender_encoder.pkl'))
    joblib.dump(le_bmicase, os.path.join(model_dir, 'bmicase_encoder.pkl'))

    print("✅ Model trained and saved successfully.")

if __name__ == "__main__":
    train_fitness_model()
    
   # from django.db import models

class WorkoutPlan(models.Model):
    weight = models.FloatField(help_text="Weight in kg")
    height = models.FloatField(help_text="Height in cm")
    age = models.IntegerField(help_text="Age in years")
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    plan_details = models.TextField(blank=True, help_text="Recommended workout plan details")

    def __str__(self):
        return f"{self.gender} - {self.age} years"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"