# test script to pull data from website
import src.scrape_data as src_sd
import src.transform_data as src_tr

# pro-football reference site
NFL_URL = 'https://www.pro-football-reference.com/years/2018/games.htm'

# generate data frame
data_table = src_sd.get_first_table(NFL_URL) # this will select the table on the site
column_names = src_sd.list_of_headers(data_table)
final_data_frame = src_sd.create_df(soup_table=data_table, list_of_column_names=column_names)

# output website dataframe
final_data_frame.to_csv('data/raw/test_data_pull.csv', sep='|', index=False)

# Transform data
cols = ['Winner/tie', 'Home/Away', 'Loser/tie'
        , 'PtsW', 'PtsL', 'YdsW', 'TOW', 'YdsL', 'TOL']
updated_df = src_tr.filter_df(final_data_frame, cols)

new_col_names = ['team_f', 'home/away', 'team_a', 'pts_f'
                 , 'pts_a', 'yds_f', 'to_f', 'yds_a', 'to_a']
updated_df = src_tr.update_cols(updated_df, new_col_names)

updated_df = src_tr.assign_home(updated_df
                                , 'home/away'
                                , 'home_f'
                                , {'x': ['', 1, 0]})

# transform scraped data into ML available data
ml_df = src_tr.create_dummies(updated_df, ['team_f', 'team_a'])

ml_df.drop(['team_f', 'team_a', '_f', '_a', 'home/away'], axis=1, inplace=True)
ml_df.to_csv('data/processed/ml_data_prep.csv', sep='|', index=False)

