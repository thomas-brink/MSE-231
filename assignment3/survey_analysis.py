"""This code was written by
        Eva Batelaan <batelaan@stanford.edu>
        Thomas Brink <tbrink@stanford.edu>
        Michelle Lahrkamp <ml17270@stanford.edu>
    Assignment 3

    Explores the original survey dataset.

    Use:
    python3 survey_analysis.py
    
    NOTE: Can optionally redirect output into 
    survey_analysis_results.txt
"""
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap


def create_categories(survey_df: pd.DataFrame):
    '''Create Categories for sorting'''
    survey_df[question_cols[2]] = pd.Categorical(survey_df[question_cols[2]],
                                                 ['A lot',
                                                  'Some',
                                                  'Not much',
                                                  'Not at all'])
    survey_df[question_cols[5]] = pd.Categorical(survey_df[question_cols[5]],
                                                 ['A lot',
                                                  'Some',
                                                  'Not much',
                                                  'Not at all'])
    survey_df[question_cols[6]] = pd.Categorical(survey_df[question_cols[6]],
                                                 ['Very important',
                                                  'Somewhat important',
                                                  'Neither important nor unimportant (neutral)',
                                                  'Somewhat unimportant',
                                                  'Very unimportant'])
    survey_df['Age'] = pd.Categorical(survey_df['Age'],
                                      ['> 60',
                                      '45-60',
                                       '30-44',
                                       '18-29'])
    survey_df['Education'] = pd.Categorical(survey_df['Education'],
                                            ['Graduate degree',
                                             'Bachelor degree',
                                             'Some college or Associate degree',
                                             'High school degree',
                                             'Less than high school degree'])
    survey_df['Household Income'] = pd.Categorical(survey_df['Household Income'],
                                                   ['$150,000+',
                                                    '$100,000 - $149,999',
                                                    '$50,000 - $99,999',
                                                    '$25,000 - $49,999',
                                                    '$0 - $24,999'
                                                    ])


def missing_data_overall(survey_df: pd.DataFrame, n_obs: int, n_features: int):
    '''Computes NaN statistics.'''
    # Count rows where at least one question is not answered
    one_na_all_questions = survey_df.isna().any(axis=1).sum()
    # Count rows where at least one of the substantive questions is not answered
    one_na_susbstantive = survey_df[question_cols].isna().any(axis=1).sum()
    # Count rows where all the demographic questions were unanswered
    all_na_demographic = survey_df[demographic_cols].isna().all(axis=1).sum()
    # Count rows where at least one of the substantive questions is unanswered but a demographic question is answered
    na_substantive_demographic = survey_df[survey_df[question_cols].isna().any(
        axis=1)].iloc[:, 7:11].notnull().any(axis=1).sum()
    # Column with the most missing values
    most_missing = survey_df.count().idxmin()
    most_missing_count = survey_df[most_missing].isna().sum()

    print('Number of rows with any question unanswered: {} ({} of all observations)'.format(
        one_na_all_questions, '{:,.2%}'.format(one_na_all_questions/n_obs)))
    print()
    print('Column with the most missing values: {}, {} missing values ({} of all observations)'.format(
        most_missing, most_missing_count, '{:,.2%}'.format(most_missing_count/n_obs)))
    print()
    print('Number of rows with at least one substantive question unanswered: {} ({} of all observations)'.format(
        one_na_susbstantive, '{:,.2%}'.format(one_na_susbstantive/n_obs)))
    print('Number of the {} aforementioned rows with at least one demographic question answered: {} ({})'.format(
        one_na_susbstantive, na_substantive_demographic, '{:,.2%}'.format(na_substantive_demographic/one_na_susbstantive)))
    print()
    print('Number of rows where all demographic questions are unanswered: {} ({}% of observations)'.format(
        all_na_demographic, '{:,.2%}'.format(all_na_demographic/n_obs)))
    print()


def in_depth_column_analysis(survey_df: pd.DataFrame, n_obs: int, n_features: int):
    '''Creates a distribution table and graph for each column.
       Generates some bivariate graphs as well.
    '''
    '''DEMOGRAPHIC DATA'''
    # Gender
    col_7 = survey_df.iloc[:, 7].value_counts(dropna=False)
    sustantive_vs_7 = survey_df[survey_df[question_cols].isna().any(
        axis=1)].iloc[:, 7].isna().sum()
    print(col_7.name, 'Distribution:')
    print(col_7.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('{} respondents did not disclose {}'.format(
        survey_df.iloc[:, 7].isna().sum(), col_7.name))
    print('{} of those respondents also did not answer at least one of the substantive questions'.format(
        sustantive_vs_7))
    plt_7 = col_7.plot.bar(
        title=col_7.name + ' Distribution', ylabel="Count", rot=0)
    for container in plt_7.containers:
        plt_7.bar_label(container)
    plt_7.figure.savefig('{}_Distribution.png'.format(col_7.name))
    print()
    plt.close()

    # Age
    survey_df.sort_values('Age')
    col_8 = survey_df.iloc[:, 8].value_counts(dropna=False, sort=False)
    print(col_8.name, 'Distribution:')
    print(col_8.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('{} respondents did not disclose {}'.format(
        survey_df.iloc[:, 8].isna().sum(), col_8.name))
    print('{} respondents who did not disclose {} disclosed {}'.format(
        survey_df[survey_df.iloc[:, 7].isna()].iloc[:, 8].notnull().sum(), col_7.name, col_8.name))
    plt_8 = col_8.plot.bar(
        title=col_8.name + ' Distribution', ylabel="Count", rot=0)
    for container in plt_8.containers:
        plt_8.bar_label(container)
    plt_8.figure.savefig('{}_Distribution.png'.format(col_8.name))
    print()
    plt.close()
    
    # Household Income
    survey_df.sort_values('Household Income')
    col_9 = survey_df.iloc[:, 9].value_counts(dropna=False, sort=False)
    print(col_9.name, 'Distribution:')
    print(col_9.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('{} respondents did not disclose {}'.format(
        survey_df.iloc[:, 9].isna().sum(), col_9.name))
    col_9.rename(index={'$0 - $24,999': '$\$0 - \$24,999$',
                        '$25,000 - $49,999': '$\$25,000 - \$49,999$',
                        '$50,000 - $99,999': '$\$50,000 - \$99,999$',
                        '$100,000 - $149,999': '$\$100,000 - \$149,999$'}, inplace=True)
    plt_9 = col_9.plot.bar(title=col_9.name + ' Distribution', ylabel="Count")
    for container in plt_9.containers:
        plt_9.bar_label(container)
    plt_9.figure.savefig('{}_Distribution.png'.format(
        col_9.name.replace(' ', '_')))
    print()
    plt.close()

    # Education
    survey_df.sort_values('Education')
    col_10 = survey_df.iloc[:, 10].value_counts(dropna=False, sort=False)
    print(col_10.name, 'Distribution:')
    print(col_10.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('{} respondents did not disclose {}'.format(
        survey_df.iloc[:, 10].isna().sum(), col_10.name))
    plt_10 = col_10.plot.bar(
        title=col_10.name + ' Distribution', ylabel="Count")
    for container in plt_10.containers:
        plt_10.bar_label(container)
    plt_10.figure.savefig('{}_Distribution.png'.format(col_10.name))
    print()
    plt.close()

    # Location
    col_11 = survey_df.iloc[:, 11].value_counts(dropna=False, sort=False)
    print(col_11.name, 'Distribution:')
    print(col_11.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('{} respondents did not disclose {}'.format(
        survey_df.iloc[:, 11].isna().sum(), col_11.name))
    print('{} respondents who did not disclose {} disclosed {}'.format(
        survey_df[survey_df.iloc[:, 10].isna()].iloc[:, 11].notnull().sum(), col_10.name, col_11.name))
    print('{} respondents who did not disclose {} disclosed {}'.format(
        survey_df[survey_df.iloc[:, 11].isna()].iloc[:, 10].notnull().sum(), col_11.name, col_10.name))

    plt_11 = col_11.plot.bar(
        title=col_11.name + ' Distribution', ylabel="Count")
    for container in plt_11.containers:
        plt_11.bar_label(container)
    plt_11.figure.savefig('{}_Distribution.png'.format(
        col_11.name.replace(' ', '_')))
    print()
    plt.close()

    # Bivariate Plots
    # Education and Sex
    survey_df.sort_values('Education')
    edu_sex_plt = survey_df.groupby(['Education', 'Gender']).size().unstack(fill_value=0).plot(
        kind='bar', title='Distribution of Education Level across Sex', ylabel='Count', xlabel='Education Level')
    edu_sex_plt.figure.savefig('Education_and_Sex.png')
    plt.close()
    
    # Location and Income
    survey_df.sort_values('Household Income')
    loc_hi = survey_df.groupby(
        ['Location (Census Region)', 'Household Income']).size().unstack(fill_value=0)
    loc_hi.rename(columns={'$0 - $24,999': '$\$0 - \$24,999$',
                           '$25,000 - $49,999': '$\$25,000 - \$49,999$',
                           '$50,000 - $99,999': '$\$50,000 - \$99,999$',
                           '$100,000 - $149,999': '$\$100,000 - \$149,999$'}, inplace=True)
    loc_hi_plt = loc_hi.plot(kind='bar', title='Distribution of Household Income across Regions', ylabel='Count',
                             xlabel='Region').legend(title='Household Income', loc='center left', bbox_to_anchor=(1.0, 0.5))
    loc_hi_plt.figure.savefig('Location_and_Income.png', bbox_inches='tight')
    plt.close()

    '''SUBSTANTIVE QUESTION DATA'''
    # Questions 1-3: Oxford Comma
    # Question 1: Oxford comma sentence example
    col_0 = survey_df.iloc[:, 0].value_counts(dropna=False)
    print('Q1:', col_0.name)
    print(col_0.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('Q1 has {} missing values'.format(survey_df.iloc[:, 0].isna().sum()))
    col_0.rename(index={'It\'s important for a person to be honest, kind, and loyal.': 'With Oxford Comma',
                        'It\'s important for a person to be honest, kind and loyal.': 'Without Oxford Comma'},
                 inplace=True)
    plt_0 = col_0.plot.bar(title='\n'.join(
        wrap('Count Distribution for Q1: ' + col_0.name, 50)), ylabel="Count", rot=0)
    for container in plt_0.containers:
        plt_0.bar_label(container)
    plt_0.figure.savefig('Question1_Distribution.png')
    print()
    plt.close()

    # Prior knowledge of Oxford comma
    col_1 = survey_df.iloc[:, 1].value_counts(dropna=False)
    print('Q2:', col_1.name)
    print(col_1.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('Q2 has {} missing values'.format(survey_df.iloc[:, 1].isna().sum()))
    plt_1 = col_1.plot.bar(title='\n'.join(
        wrap('Count Distribution for Q2: ' + col_1.name, 50)), ylabel="Count", rot=0)
    for container in plt_1.containers:
        plt_1.bar_label(container)
    plt_1.figure.savefig('Question2_Distribution.png')
    print()
    plt.close()

    # Question 3: Level of investment in usage of the Oxford comma
    col_2 = survey_df.iloc[:, 2].value_counts(sort=False, dropna=False)
    print('Q3:', col_2.name)
    print(col_2.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('Q3 has {} missing values'.format(survey_df.iloc[:, 2].isna().sum()))
    plt_2 = col_2.plot.bar(title='\n'.join(
        wrap('Count Distribution for Q3: ' + col_2.name, 50)), ylabel="Count", rot=0)
    for container in plt_2.containers:
        plt_2.bar_label(container)
    plt_2.figure.savefig('Question3_Distribution.png')
    print()
    plt.close()

    # Q1-3 Bivariate Plots
    # Question 1 and 2: Use of the Oxford comma given prior knowledge
    # Table
    col_0_given_1 = survey_df[question_cols[:2]].groupby(
        question_cols[1], dropna=False).value_counts(normalize=True)
    print('Response distribution for Q1 given if the person previously knew of the Oxford comma or not')
    print(col_0_given_1.to_frame().to_string(header=False,
          index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_0g1 = survey_df[question_cols[:2]].groupby(
        question_cols[1], dropna=False).value_counts()
    plt_01 = col_0g1.unstack().plot.bar(
        title='Count of Use of the Oxford Comma Given Prior Knowledge', rot=0)
    plt_01.legend(title=col_0.name, loc='center left',
                  bbox_to_anchor=(0, -0.3))
    for container in plt_01.containers:
        plt_01.bar_label(container)
    plt_01.figure.savefig('Question1_Given_2_Distribution.png', bbox_inches='tight')
    print()
    plt.close()

    # Question 2 and 3: Level of investment in usage of the Oxford comma given prior knowledge
    answered_Q3_not_Q2 = survey_df[survey_df.iloc[:,
                                                  2].isna()].iloc[:, 1].value_counts()
    print('{} respondents who did not answer question Q3 answered Q2\n'.format(
        len(answered_Q3_not_Q2)))
    # Table
    col_2_given_1 = survey_df[question_cols[1:3]].groupby(
        question_cols[1]).value_counts(normalize=True)
    print('Response distribution for Q3 given if the person previously knew of the Oxford comma or not')
    print(col_2_given_1.to_frame().sort_values(question_cols[1:3]).to_string(
        header=False, index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_2g1 = survey_df[question_cols[1:3]].groupby(
        question_cols[1]).value_counts()
    plt_21 = col_2g1.unstack().plot.bar(title='\n'.join(wrap(
        'Count of Level of Investment in Usage of the Oxford Comma Given Prior Knowledge', 50)), rot=0)
    plt_21.legend(title='\n'.join(wrap(col_2.name, 30)),
                  loc='center left', bbox_to_anchor=(1.0, 0.5))
    for container in plt_21.containers:
        plt_21.bar_label(container)
    plt_21.figure.savefig('Question3_Given_2_Distribution.png', bbox_inches='tight')
    print()
    plt.close()

    # Questions 1 and 3: Level of investment in usage of the Oxford Comma given whether the respondent used it
    col_02 = [question_cols[0], question_cols[2]]
    # Table
    col_2_given_0 = survey_df[col_02].groupby(
        question_cols[0]).value_counts(normalize=True, dropna=False)
    print('Response distribution for Q3 given if the person used the Oxford comma')
    print(col_2_given_0.to_frame().sort_values(col_02).to_string(
        header=False, index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_2g0 = survey_df.groupby(col_02).size().unstack(fill_value=0)
    col_2g0.rename(index={'It\'s important for a person to be honest, kind, and loyal.': 'With Oxford Comma',
                          'It\'s important for a person to be honest, kind and loyal.': 'Without Oxford Comma'},
                   inplace=True)
    plt_20 = col_2g0.plot.bar(title='\n'.join(wrap(
        'Count of Level of Investment in Usage of the Oxford Comma Given Whether the Respondent Used It', 50)), rot=0)
    plt_20.legend(title='\n'.join(wrap(col_2.name, 30)),
                  loc='center left', bbox_to_anchor=(1.0, 0.5))
    for container in plt_20.containers:
        plt_20.bar_label(container)
    plt_20.figure.savefig('Question3_Given_1_Distribution.png', bbox_inches='tight')
    print()
    plt.close()

    # Questions 4-6: Plurality of 'data'
    # Question 4: Plurality of 'data' sentence example
    # Table
    col_3 = survey_df.iloc[:, 3].value_counts(dropna=False)
    print('Q4:', col_3.name)
    print(col_3.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('Q4 has {} missing values'.format(survey_df.iloc[:, 3].isna().sum()))
    # Plot
    col_3.rename(index={
        'Some experts say it\'s important to drink milk, but the data is inconclusive.': 'data is',
        'Some experts say it\'s important to drink milk, but the data are inconclusive.': 'data are'
    }, inplace=True)
    plt_3 = col_3.plot.bar(title='\n'.join(wrap('Count Distribution for Q4: ' + col_3.name, 50)),
                           ylabel="Count", rot=0)
    for container in plt_3.containers:
        plt_3.bar_label(container)
    plt_3.figure.savefig('Question4_Distribution.png')
    print()
    plt.close()

    # Question 5: Prior consideration of the plurality of 'data'
    # Table
    col_4 = survey_df.iloc[:, 4].value_counts(dropna=False)
    print('Q5:', col_4.name)
    print(col_4.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('Q5 has {} missing values'.format(survey_df.iloc[:, 4].isna().sum()))
    # Plot
    plt_4 = col_4.plot.bar(title='\n'.join(wrap('Count Distribution for Q5: ' + col_4.name, 50)),
                           ylabel="Count", rot=0)
    for container in plt_4.containers:
        plt_4.bar_label(container)
    plt_4.figure.savefig('Question5_Distribution.png')
    print()
    plt.close()

    # Question 6: Level of investment in the plurality of 'data'
    # Table
    col_5 = survey_df.iloc[:, 5].value_counts(sort=False, dropna=False)
    print('Q6:', col_5.name)
    print(col_5.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('Q6 has {} missing values'.format(survey_df.iloc[:, 5].isna().sum()))
    # Plot
    plt_5 = col_5.plot.bar(title='\n'.join(wrap('Count Distribution for Q6: ' + col_5.name, 50)),
                           ylabel="Count", rot=0)
    for container in plt_5.containers:
        plt_5.bar_label(container)
    plt_5.figure.savefig('Question6_Distribution.png')
    print()
    plt.close()

    # Q4-6 Bivariate Plots
    # Question 4 and 5: Plurality of 'data' given prior consideration
    # Table
    col_3_given_4 = survey_df[question_cols[3:5]].groupby(
        question_cols[4]).value_counts(normalize=True)
    print('Response distribution for Q5 given if the person previously considered the plurality of \'data\'')
    print(col_3_given_4.to_frame().to_string(header=False,
          index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_3g4 = survey_df[question_cols[3:5]].groupby(
        question_cols[4]).value_counts()
    plt_34 = col_3g4.unstack().plot.bar(title='Count of use of \'data\' as Plural Given Prior Consideration',
                                        rot=0, xlabel='\n'.join(wrap(col_4.name, 80)))
    plt_34.legend(title=col_3.name, loc='center left',
                  bbox_to_anchor=(-0.15, -0.35))
    for container in plt_34.containers:
        plt_34.bar_label(container)
    plt_34.figure.savefig('Question5_Given_4_Distribution.png', bbox_inches='tight')
    print()
    plt.close()

    # Question 5 and 6: Level of investment in the plurality of 'data' given prior consideration
    answered_Q6_not_Q5 = survey_df[survey_df.iloc[:,
                                                  5].isna()].iloc[:, 4].value_counts()
    print('{} respondents who did not answer question Q6 answered Q5\n'.format(
        len(answered_Q6_not_Q5)))
    # Table
    col_5_given_4 = survey_df[question_cols[4:6]].groupby(
        question_cols[4]).value_counts(normalize=True)
    print('Response distribution for Q6 given if the person previously considered the plurality of \'data\'')
    print(col_5_given_4.to_frame().sort_values(question_cols[4:6]).to_string(
        header=False, index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_5g4 = survey_df[question_cols[4:6]].groupby(
        question_cols[4]).value_counts()
    plt_54 = col_5g4.unstack().plot.bar(title='\n'.join(wrap(
        'Count of Level of Investment in Usage of the Oxford Comma Given Prior Knowledge', 50)),
        rot=0, xlabel='\n'.join(wrap(col_4.name, 70)))
    plt_54.legend(title='\n'.join(wrap(col_5.name, 30)),
                  loc='center left', bbox_to_anchor=(1.0, 0.5))
    for container in plt_54.containers:
        plt_54.bar_label(container)
    plt_54.figure.savefig('Question6_Given_5_Distribution.png', bbox_inches='tight')
    print()
    plt.close()

    # Questions 4 and 6: Level of investment in plurality of 'data' given whether the respondent used the plural
    col_35 = [question_cols[3], question_cols[5]]
    # Table
    col_5_given_3 = survey_df[col_35].groupby(
        question_cols[3]).value_counts(normalize=True, dropna=False)
    print('Response distribution for Q6 given if the person previously considered the plurality of \'data\'')
    print(col_5_given_3.to_frame().sort_values(col_35).to_string(
        header=False, index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_5g3 = survey_df.groupby(col_35).size().unstack(fill_value=0)
    col_5g3.rename(index={'Some experts say it\'s important to drink milk, but the data are inconclusive.': 'data are',
                          'Some experts say it\'s important to drink milk, but the data is inconclusive.': 'data is'},
                   inplace=True)
    plt_53 = col_5g3.plot.bar(title='\n'.join(wrap(
        'Count of Level of Investment in Plurality of \'data\' Given Whether the Respondent Used the Plural', 50)), rot=0)
    plt_53.legend(title='\n'.join(wrap(col_5.name, 30)),
                  loc='center left', bbox_to_anchor=(1.0, 0.5))
    for container in plt_53.containers:
        plt_53.bar_label(container)
    plt_53.figure.savefig('Question6_Given_4_Distribution.png', bbox_inches='tight')
    print()
    plt.close()

    # Question 7: Importance of Grammar
    # Table
    col_6 = survey_df.iloc[:, 6].value_counts(dropna=False, sort=False)
    print('Q7:', col_6.name)
    print(col_6.div(n_obs).to_string(
        header=False, float_format='{:,.2%}'.format))
    print('Q7 has {} missing values'.format(survey_df.iloc[:, 6].isna().sum()))
    # Plot
    col_6.rename(index={'Neither important nor unimportant (neutral)': 'Neutral'},
                 inplace=True)
    plt_6 = col_6.plot.bar(title='\n'.join(
        wrap('Count Distribution for Q7: ' + col_6.name, 50)), ylabel="Count")
    for container in plt_6.containers:
        plt_6.bar_label(container)
    plt_6.figure.savefig('Question7_Distribution.png')
    print()
    plt.close()

    # Q7 Bivariate Plots
    # Questions 3 and 7: Level of investment in proper grammer given level of investment in the use of the Oxford Comma
    col_26 = [question_cols[2], question_cols[6]]
    # Table
    col_6_given_2 = survey_df[col_26].groupby(
        question_cols[2]).value_counts(normalize=True, dropna=False)
    print('Response distribution for Q7 given level of investment in the use of the Oxford Comma')
    print(col_6_given_2.to_frame().sort_values(col_26).to_string(
        header=False, index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_6g2 = survey_df.groupby(col_26).size().unstack(fill_value=0)
    # col_5g3.rename(index={'Some experts say it\'s important to drink milk, but the data are inconclusive.': 'Plural',
    #                       'Some experts say it\'s important to drink milk, but the data is inconclusive.': 'Singular'},
    #              inplace=True)
    plt_62 = col_6g2.plot.bar(title='\n'.join(wrap(
        'Count of Importance of Proper Grammar Given Level of Investment in the Use of the Oxford Comma', 50)),
        rot=0, xlabel='\n'.join(wrap(col_2.name, 70)))
    plt_62.legend(title='\n'.join(wrap(col_6.name, 50)),
                  loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt_62.figure.savefig('Question7_Given_3_Distribution.png', bbox_inches='tight')
    print()
    plt.close()

    # Questions 6 and 7: Level of investment in proper grammer given level of investment in the plurality of 'data'
    # Table
    col_6_given_5 = survey_df[question_cols[5:7]].groupby(
        question_cols[5]).value_counts(normalize=True)
    print('Response distribution for Q7 given level of investment in the plurality of \'data\'')
    print(col_6_given_5.to_frame().sort_values(question_cols[5:7]).to_string(
        header=False, index_names=False, float_format='{:,.2%}'.format))
    # Plot
    col_6g5 = survey_df[question_cols[5:7]].groupby(
        question_cols[5]).value_counts()
    plt_65 = col_6g5.unstack().plot.bar(title='\n'.join(wrap(
        'Count of Importance of Proper Grammar Given Level of Investment in the Plurality of \'data\'', 50)),
        rot=0, xlabel='\n'.join(wrap(col_5.name, 70)))
    plt_65.legend(title='\n'.join(wrap(col_6.name, 50)),
                  loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt_65.figure.savefig('Question7_Given_6_Distribution.png', bbox_inches='tight')
    print()
    plt.close()


if __name__ == "__main__":
    # Load in data
    survey_df = pd.read_csv('comma-survey.csv', index_col='RespondentID')

    # Extract question and demographics columns
    question_cols = list(survey_df.columns)[:7]
    demographic_cols = list(survey_df.columns)[7:]

    create_categories(survey_df)

    # Compute Descriptive Statistics
    n_obs = len(survey_df)
    n_features = len(survey_df.columns)
    print('The data set has {} observations and {} features'.format(n_obs, n_features))

    # Missing data overall
    missing_data_overall(survey_df, n_obs, n_features)

    # Demographic Distributions
    # Which groups are present in the data
    demographic_options = []
    for d in demographic_cols:
        demographic_options.append(survey_df[d].unique())
    demographic_options = [list(x) for x in demographic_options]
    print('Demographic groups present in the data:',
          *demographic_options, sep='\n')

    in_depth_column_analysis(survey_df, n_obs, n_features)
