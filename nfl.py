import requests
from bs4 import BeautifulSoup
import model
import pandas as pd
from datetime import date

# Create a Response object called r
r_passing = requests.get(
    'https://www.nfl.com/stats/team-stats/offense/passing/2023/reg/all', timeout=10.0)

r_receiving = requests.get(
    'https://www.nfl.com/stats/team-stats/offense/receiving/2023/reg/all', timeout=10.0)

r_rushing = requests.get(
    'https://www.nfl.com/stats/team-stats/offense/rushing/2023/reg/all', timeout=10.0)

# Create a Beautiful Soup object called soup
soup_passing = BeautifulSoup(r_passing.text, 'html.parser')
soup_receiving = BeautifulSoup(r_receiving.text, 'html.parser')
soup_rushing = BeautifulSoup(r_rushing.text, 'html.parser')

# Get the table
passing_table_in_html = soup_passing.find('table')
receiving_table_in_html = soup_receiving.find('table')
rushing_table_in_html = soup_rushing.find('table')

# Get data from the table head and table body
passing_table_head = model.get_table_head_fields_as_list(passing_table_in_html)
receiving_table_head = model.get_table_head_fields_as_list(receiving_table_in_html)
rushing_table_head = model.get_table_head_fields_as_list(rushing_table_in_html)

passing_table_body = model.get_table_body_as_lists(passing_table_in_html)
receiving_table_body = model.get_table_body_as_lists(receiving_table_in_html)
rushing_table_body = model.get_table_body_as_lists(rushing_table_in_html)

# Join the table head data and table body data
passing_table_data = [passing_table_head] + passing_table_body
receiving_table_data = [receiving_table_head] + receiving_table_body
rushing_table_data = [rushing_table_head] + rushing_table_body

# Create a Pandas DataFrame
passing_df = pd.DataFrame(data=passing_table_data)
receiving_df = pd.DataFrame(data=receiving_table_data)
rushing_df = pd.DataFrame(data=rushing_table_data)

# Make the first row the column names
passing_columns = passing_df.iloc[0]
receiving_columns = receiving_df.iloc[0]
rushing_columns = rushing_df.iloc[0]

passing_df = passing_df[1:]
receiving_df = receiving_df[1:]
rushing_df = rushing_df[1:]

passing_df.columns = passing_columns
receiving_df.columns = receiving_columns
rushing_df.columns = rushing_columns

# Clean up the Team column to include only the Team name
passing_df['Team'] = passing_df['Team'].str.split("\n").str.get(0)
receiving_df['Team'] = receiving_df['Team'].str.split("\n").str.get(0)
rushing_df['Team'] = rushing_df['Team'].str.split("\n").str.get(0)

# Rename the columns to be more easily understood, since there are common fields across files
passing_df_renamed = passing_df.rename(
    columns={
        "Att": "Passing Attempts",
        "Cmp": "Passing Completions",
        "Cmp %": "Passing Completion %",
        "Yds/Att": "Passing Yards/Attempt",
        "TD": "Passing TDs",
        "INT": "Passing Interceptions",
        "Rate": "Passing Rate",
        "1st": "Passing 1st Downs",
        "1st%": "Passing 1st Down %",
        "20+": "Passing 20+",
        "40+": "Passing 40+",
        "Lng": "Passing Longest",
        "Sck": "Passing Sacks",
        "SckY": "Passing Sack Yards",
    }
)

receiving_df_renamed = receiving_df.rename(
    columns={
        "Rec": "Receiving Receptions",
        "Yds": "Receiving Yards",
        "Yds/Rec": "Receiving Yards/Reception",
        "TD": "Receiving TDs",
        "20+": "Receiving 20+",
        "40+": "Receiving 40+",
        "Lng": "Receiving Longest",
        "Rec 1st": "Receiving 1st Downs",
        "Rec 1st%": "Receiving 1st Down %",
        "Rec FUM": "Receiving Fumbles",
    }
)

rushing_df_renamed = rushing_df.rename(
    columns={
        "Att": "Rushing Attempts",
        "Rush Yds": "Rushing Yards",
        "YPC": "Rushing Yards/Carry",
        "TD": "Rushing TDs",
        "20+": "Rushing 20+",
        "40+": "Rushing 40+",
        "Lng": "Rushing Longest",
        "Rush 1st": "Rushing 1st Downs",
        "Rush 1st%": "Rushing 1st Down %",
        "Rush FUM": "Rushing Fumbles",
    }
)

# Merge the 3 renamed DataFrames into one
passing_receiving_df = pd.merge(passing_df_renamed, receiving_df_renamed, on="Team", how="inner")
passing_receiving_rushing_df = pd.merge(passing_receiving_df, rushing_df_renamed, on="Team", how="inner")

# Grab todays date and format it for the csv file
today = date.today()
d1 = today.strftime("%m-%d-%y")

# Export the Pandas df to a csv file
passing_receiving_rushing_df.to_csv(f"data/team_stats{d1}.csv", index=False)