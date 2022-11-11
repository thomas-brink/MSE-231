"""This code was written by
        Eva Batelaan <batelaan@stanford.edu>
        Thomas Brink <tbrink@stanford.edu>
        Michelle Lahrkamp <ml17270@stanford.edu>
    Assignment 3

    Reformats google form survey results and exports to a new file.

    Use:
    python3 create_new_comma_survey.py

    The following flags are required:
        --survey_csv: google form survey results in a csv
            ex: drive_survey.csv
"""
import argparse
import pandas as pd
import numpy as np

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Reformat survey data and create new_comma_survey.csv"
    )
    parser.add_argument(
        "--survey_csv", help="csv of google form responses", required=True)
    flags = parser.parse_args()
    
    # Read csvs into dataframes
    survey_df = pd.read_csv(flags.survey_csv)
    og_survey_df = pd.read_csv('comma-survey.csv', index_col='RespondentID')
    
    # Rename columns of google form survey results
    survey_df = survey_df.drop(columns=['Tijdstempel'])
 
    mapper = {}
    og_survey_columns = list(og_survey_df.columns)
    survey_columns = list(survey_df.columns)
    for i in range(len(survey_columns)):
        mapper[survey_columns[i]] = og_survey_columns[i]

    survey_df = survey_df.rename(columns=mapper)
    
    # Export to new csv
    survey_df.to_csv('new_comma_survey.csv')