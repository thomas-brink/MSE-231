import numpy as np
import pandas as pd
import yaml
import datetime
import os

def read_yaml(filename):
    with open(filename, 'r') as f:
        list_data = yaml.safe_load(f)

    return list_data

def get_party(terms, today):
    """ Blablabla
    """
    for term in leg['terms']:
        start_date = datetime.datetime.strptime(term['start'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(term['end'], '%Y-%m-%d').date()

        if (start_date < today and end_date > today):
            return term['party']


def get_twitter_info(leg_soc, leg_bio_id):
    """ Blablabla
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
            congress_df = congress_df.append({'twitter_id': twitter_id, 'twitter_username': twitter_username,
                                              'party': party}, ignore_index = True)

    congress_df.to_csv('congress_df_{}.csv'.format(date.strftime("%Y-%m-%d")))
