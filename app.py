import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from collections import defaultdict

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Function to get credentials with the defined scopes
def get_credentials():
    creds_info = st.secrets["gcp_service_account"]
    return Credentials.from_service_account_info(creds_info, scopes=SCOPES)

# Initialize credentials and client
creds = get_credentials()
client = gspread.authorize(creds)

# Open the Google Sheet and fetch data
sheet = client.open('Phi Pledge Submission (Responses)').sheet1  # Use your actual sheet name
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Fetch the submission password from Streamlit secrets
submission_password = st.secrets["application_secrets"]["submission_password"]

# Process and display data
marks = defaultdict(lambda: {'white': 0, 'black': 0})

for _, row in df.iterrows():
    # Convert the sheet password to string and lowercase for comparison
    sheet_password = str(row.get('Submission Password', '')).lower().strip()
    
    # Check if the password matches and the submission is approved
    if sheet_password == submission_password.lower().strip() and row.get('Approved?', '').lower() == 'yes':
        names = row['Which pledge is this for?'].split(', ')
        mark_type = 'white' if row['What type of mark?'] == 'White' else 'black'
        
        # Ensure 'How many?' is treated as an integer
        try:
            num_marks = int(row['How many?'])
        except ValueError:
            num_marks = 0  # Default to 0 if conversion fails
        
        for name in names:
            marks[name.strip()][mark_type] += num_marks

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
    # Adjusted filter logic for detailed info based on the selected name
    detailed_info = df[df.apply(lambda row: selected_name.lower().strip() in [name.lower().strip() for name in row['Which pledge is this for?'].split(', ')] and 
                                str(row['Submission Password']).strip().lower() == submission_password.strip().lower() and
                                row.get('Approved?', '').lower() == 'yes', axis=1)]
    detailed_info.index = ["" for _ in detailed_info.index]
    st.dataframe(detailed_info[['Timestamp', 'Which brother is submitting this?', 'Description', 'What type of mark?', 'How many?']])