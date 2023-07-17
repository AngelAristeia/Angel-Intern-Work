# Note this must be installed in the command line using the following line: python -m pip install --index-url=https://bcms.bloomberg.com/pip/simple blpapi
import blpapi
import pandas as pd
# Download this pacakge using the following line of code:python -m pip install xbbg
from xbbg import blp
# The below packages are used to convert the positions script into a streamlit app for better usability
import streamlit as st

# For Streamlit, use this line to open the Google Chrome Page: python -m streamlit hello
# Now name the app that we build using streamlit

st.title('CEF Positional Change Tracker')

st.write(
    "Below, please input the ticker for a given CEF ETF in order to track the change in positional holdings for the most "
    "recent filing date. Said information is imported from Bloomberg, and is subject to their "
    "update schedule. While using this application, make sure to have Bloomberg open. Note, you can input any"
    " not just CEF's.")

ETF_Name = st.text_input('Enter the ETF Name', 'HYT')
Movement_Number = st.number_input('Enter the number of Largest Movements you would like displayed', 5)
ETF_Name = " ".join([ETF_Name,"US Equity"])

holders = blp.bds(ETF_Name, flds='All_Holders_Public_Filings', cache=True)
(holders.loc[:, ~holders.columns.str.contains(
        f'holder_id|portfolio_name|change|number|'
        f'metro|percent_of_portfolio|source'
    )]
    .rename(
        index=lambda tkr: tkr.replace(' Equity', ''),
        columns={
            'holder_name_': 'holder',
            'position_': 'position',
            'filing_date__': 'filing_dt',
            'percent_outstanding': 'pct_out',
            'insider_status_': 'insider',
        }
    )
)

select_columns = [1, 6]

holders_df = pd.DataFrame(holders)
holders_final = holders_df.iloc[:, select_columns]

def print_top_n_rows(df, column, n):
    top_n_rows = df.assign(abs_change=df[column].abs()).nlargest(n, 'abs_change')
    for _, row in top_n_rows.iterrows():
        row = row.drop('abs_change')  # Exclude the 'abs_change' column
        st.write(row)

if not holders_final.empty:
    column_name = str('position_change__')
    print_top_n_rows(holders_final, column_name, Movement_Number)
else:
    st.write("No data available for the selected ETF and Date.")
