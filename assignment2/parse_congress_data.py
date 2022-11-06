"""This code was written by
        Eva Batelaan <batelaan@stanford.edu>
        Thomas Brink <tbrink@stanford.edu>
        Michelle Lahrkamp <ml17270@stanford.edu>
    Assignment 2 Group 3

    Use:
    python3 parse_congress_data.py
    
    Requirements:
    Must have downloaded and saved the following files from 
    [congress-legislators](https://github.com/unitedstates/congress-legislators):
        'legislators-current.yaml'
        'legislators-social-media.yaml'
    
    Output:
    Creates a date-stamped file congress_df_YYYY-MM-DD.csv where YYYY-MM-DD
    is the date that the 'legislators-current.yaml' file was downloaded
"""
import numpy as np
import pandas as pd
import yaml
import datetime
import os

def read_yaml(filename):
    """Read in data safely from file.
    """
    with open(filename, 'r') as f:
        list_data = yaml.safe_load(f)
        return list_data

def get_party(terms, today):
    """Gets the legislator's current party affiliation based on their current term
    """
    for term in terms:
        start_date = datetime.datetime.strptime(term['start'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(term['end'], '%Y-%m-%d').date()

        if (start_date < today and end_date > today):
            return term['party']


def get_twitter_info(leg_soc, leg_bio_id):
    """Gets twitter_id,twitter_username for a given legislator
    """
    leg_soc_ids = np.array([leg_soc[i]['id']['bioguide'] for i in range(len(leg_soc))])
    try:
        index = np.where(leg_soc_ids == leg_bio_id)[0][0]
        return str(leg_soc[index]['social']['twitter_id']), leg_soc[index]['social']['twitter']
    except:
        return (None, None)


if __name__ == "__main__":
    leg_cur = read_yaml('legislators-current.yaml')
    leg_soc = read_yaml('legislators-social-media.yaml')

    congress_df = pd.DataFrame(columns=['twitter_id', 'twitter_username', 'party'])
    # Use file creation time (~ date it was downloaded) as current date
    creation_time = os.path.getctime('legislators-current.yaml')
    date = datetime.datetime.fromtimestamp(creation_time).date()

    for leg in leg_cur:
        party = get_party(leg['terms'], date)
        twitter_id, twitter_username = get_twitter_info(leg_soc, leg['id']['bioguide'])
        if twitter_id:
            # Only save the legislator if twitter account could be found
            congress_df = congress_df.append({'twitter_id': twitter_id, 'twitter_username': twitter_username,
                                              'party': party}, ignore_index = True)
    # Output to date-stamped csv file
    congress_df.to_csv('congress_df_{}.csv'.format(date.strftime("%Y-%m-%d")))
