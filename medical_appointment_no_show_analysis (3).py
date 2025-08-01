# -*- coding: utf-8 -*-
"""Medical Appointment No-Show Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V3Hae1npUH5O-bUYtH4QJVOOao5cymtH

This project analyzes real-world medical appointment data from hospitals in Brazil, focusing on why patients miss their scheduled appointments.

Dataset: 110k+ medical appointments
Target Variable: No-show (whether a patient showed up or not)
Features: Gender, Age, SMS reminders, Scheduled/Appointment dates, Neighbourhood, Scholarship program, etc.
The main goal is to discover the factors influencing patient no-shows and visualize key insights from the data.

**Key Insights**
* Patients who received an SMS reminder were less likely to miss their
appointments.
* Younger patients had higher no-show rates compared to older patients.
* Longer waiting times between scheduling and appointment increased no-show likelihood.

*Machine Learing descrebtion *
# Absenteeism Prediction Model (Random Forest Classifier)

This project aims to predict employee absenteeism using a Random Forest Classifier.  
The dataset includes features such as age, distance to work, waiting time for appointments, and gender.  
The model is trained and optimized with GridSearchCV, and its performance is evaluated using confusion matrix and classification report.

**Key Steps:**
- Data cleaning and binary encoding (e.g., 'Gender', 'No-show')
- Train/test split using stratified sampling
- Model training and hyperparameter tuning
- Evaluation via precision, recall, F1-score, and confusion matrix
- Final visualization for interpretability

This model can help HR departments or healthcare clinics to identify individuals more likely to miss appointments or shifts, enabling targeted interventions.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# uploading the data
df= pd.read_csv('KaggleV2-May-2016.csv')

#abstarct of the data set
print(df.head())
print(df.shape)

# data set info
df.info()

# describtion of data set
df.describe()

#duplicates, empties,...

print(df.isnull().sum())
print(df.duplicated().sum())
print(df['PatientId'].nunique(), '/', df['PatientId'].count())

# changing into datetime

df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'], errors='coerce')

# watting time/ new coulmn
df['WaitingDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days

df = df[df['Age'] >= 0]

# visualizition

#show or no show
sns.countplot(data=df, x='No-show')
plt.title('Show vs No-show')
plt.show()

#impact of sms
sns.countplot(data=df, x='SMS_received', hue='No-show')
plt.title('Effect of SMS on No-show')
plt.show()

#histogram
plt.figure(figsize=(10,5))
sns.histplot(data=df, x='Age', hue='No-show', bins=30, kde=True)
plt.title('Age Distribution and No-show')
plt.show()

# watting time and no show
plt.figure(figsize=(10,5))
sns.histplot(data=df, x='WaitingDays', hue='No-show', bins=30, kde=True)
plt.title('Waiting Days and No-show')
plt.show()

#No-show
df['No-show'] = df['No-show'].map({'No': 0, 'Yes': 1})
df['Gender'] = df['Gender'].map({'F': 0, 'M': 1})

sns.countplot(x='No-show', data=df)
plt.title("Distribution of Show/No-show")
plt.show()

print(df['No-show'].value_counts(normalize=True))

sns.countplot(x='No-show', data=df)
plt.title("Distribution of Show/No-show")
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

print(df.columns)

features = ['Age', 'Gender', 'Scholarship', 'Hipertension', 'Diabetes',
            'Alcoholism', 'Handcap', 'SMS_received', 'WaitingDays']

X = df[features]
y = df['No-show']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

#model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.show()

model = RandomForestClassifier(class_weight='balanced', random_state=42)

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X_train, y_train)

model = RandomForestClassifier(random_state=42)
model.fit(X_resampled, y_resampled)

from sklearn.metrics import classification_report, confusion_matrix
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
plt.title("Confusion Matrix After SMOTE")
plt.show()

importances = model.feature_importances_
feat_names = X.columns

plt.figure(figsize=(8,5))
sns.barplot(x=importances, y=feat_names)
plt.title("Feature Importance")
plt.show()

from sklearn.metrics import roc_auc_score

y_pred_proba = model.predict_proba(X_test)[:, 1]
roc_auc_score(y_test, y_pred_proba)

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

from sklearn.model_selection import GridSearchCV

params = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
}

grid = GridSearchCV(RandomForestClassifier(class_weight='balanced', random_state=42),
                    param_grid=params,
                    scoring='recall',
                    cv=3,
                    n_jobs=-1)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

importances = best_model.feature_importances_
feat_names = X.columns
sns.barplot(x=importances, y=feat_names)
plt.title("Feature Importances")
plt.show()

from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=3,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_resampled, y_resampled)

best_model = grid_search.best_estimator_


y_pred = best_model.predict(X_test)
print(classification_report(y_test, y_pred))

print("Best Parameters:", grid_search.best_params_)
print("Best Score:", grid_search.best_score_)

best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)

from sklearn.metrics import classification_report, confusion_matrix

y_pred = best_model.predict(X_test)

print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Show', 'No-show'], yticklabels=['Show', 'No-show'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

report_dict = classification_report(y_test, y_pred, output_dict=True)
df_report = pd.DataFrame(report_dict).transpose()

df_report.iloc[:2, :3].plot(kind='bar', figsize=(8,5), colormap='Set2')
plt.title('Precision, Recall, F1-score by Class')
plt.xticks(rotation=0)
plt.ylabel('Score')
plt.ylim(0, 1)
plt.grid(axis='y')
plt.show()

#example
sample = X_test.iloc[[10]]
real = y_test.iloc[10]
pred = best_model.predict(sample)[0]

print(" ویژگی‌ها:", sample.to_dict())
print(f"پیش‌بینی مدل: {'No-show' if pred==1 else 'Show'}")
print(f"وضعیت واقعی: {'No-show' if real==1 else 'Show'}")