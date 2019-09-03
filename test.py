# test script to pull data from website
import src.scrape_data as src_sd

# pro-football reference site
NFL_URL = 'https://www.pro-football-reference.com/years/2018/games.htm'

# generate data frame
data_table = src_sd.get_first_table(NFL_URL) # this will select the table on the site
column_names = src_sd.list_of_headers(data_table)
final_data_frame = src_sd.create_df(soup_table=data_table, list_of_column_names=column_names)

# output website dataframe
final_data_frame.to_csv('data/raw/test_data_pull.csv', sep='|')