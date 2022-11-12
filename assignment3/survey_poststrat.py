"""This code was written by
        Eva Batelaan <batelaan@stanford.edu>
        Thomas Brink <tbrink@stanford.edu>
        Michelle Lahrkamp <ml17270@stanford.edu>
    Assignment 3

    Fits a multinomial logistic regression models that predict
    survey responses as a function of the respondent’s demographics.

    Use:
    python3 csurvey_poststrat.py
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

if __name__ == "__main__":
    # Combine survey data
    og_survey_df = pd.read_csv('comma-survey.csv', index_col='RespondentID')
    new_survey_df = pd.read_csv('new_comma_survey.csv', index_col='RespondentID')
    survey_df = pd.concat([og_survey_df, new_survey_df])
    
    # Extract question and demographics columns
    question_cols = list(survey_df.columns)[:7]
    demographic_cols = list(survey_df.columns)[7:11]
    
    # Encode demographic responses
    demographics = survey_df[demographic_cols].to_numpy()
    # Define the ordinal features pipeline
    enc = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OrdinalEncoder()),
        ('scaler', StandardScaler())
    ])
    enc.fit(demographics)
    X_demographics = enc.transform(demographics)
    
    # Fit encoders of question responses
    labelEncoders = []
    for q in question_cols:
        y_vals = survey_df[q].to_numpy()
        le = preprocessing.LabelEncoder()
        le.fit(y_vals)
        labelEncoders.append(le)
        
    # Fit models
    lr = LogisticRegression(multi_class='multinomial')
    models = []
    for idx, q in enumerate(question_cols):
        y_vals = survey_df[q].to_numpy()
        Y_vals = labelEncoders[idx].transform(y_vals)
        model = lr.fit(X_demographics, Y_vals)
        models.append(model)
    