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
    og_survey_df = pd.read_csv('comma-survey.csv', index_col='RespondentID')
    new_survey_df = pd.read_csv('new_comma_survey.csv', index_col='RespondentID')
    survey_df = pd.concat([og_survey_df, new_survey_df])