import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from collections import defaultdict

# Use credentials from Streamlit secrets
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = gspread.authorize(creds)

# Open the Google Sheet and fetch data
sheet = client.open('Upsilon Pledge Submission (Responses)').sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Process and display data
marks = defaultdict(lambda: {'white': 0, 'black': 0})
for _, row in df.iterrows():
    if row.get('Submission Password', '').lower() == 'patience' and row.get('Approved?', '').lower() == 'yes':
        names = row['Which pledge is this for?'].split(', ')
        mark_type = 'white' if row['What type of mark?'] == 'White' else 'black'
        for name in names:
            marks[name.strip()][mark_type] += row['How many?']

# Convert processed data to DataFrame for display
display_data = [[name, mark['white'], mark['black']] for name, mark in marks.items()]
display_df = pd.DataFrame(display_data, columns=['Name', 'White Marks', 'Black Marks'])

# Set the DataFrame index to False
display_df.index = ["" for _ in display_df.index]

# Streamlit app main view
st.title("Pledge Mark Tracker")
st.dataframe(display_df, use_container_width=True)

# Interactive selection for detailed view
selected_name = st.selectbox('Select a name to view details', [''] + list(marks.keys()))
if selected_name:
    detailed_info = df[(df['Which pledge is this for?'].str.contains(selected_name, case=False)) & 
                       (df['Submission Password'].str.lower() == 'patience')]
    detailed_info.index = ["" for _ in detailed_info.index]
    st.dataframe(detailed_info[['Timestamp', 'Which brother is submitting this?', 'Description', 'What type of mark?', 'How many?']])
