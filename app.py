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

try:
    # Define expected headers based on your Google Sheet structure
    expected_headers = [
        'Timestamp',
        'Which brother is submitting this?',
        'Which pledge is this for?',
        'What type of mark?',
        'How many?',
        'Description',
        'Submission Password',
        'Approved?'
    ]

    # Open the Google Sheet and fetch data with expected headers
    sheet = client.open('Pledge Submission (Responses)').sheet1
    data = sheet.get_all_records(expected_headers=expected_headers)
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
    display_data = [[name, mark['white'], mark['black']] 
                   for name, mark in marks.items()]
    display_df = pd.DataFrame(display_data, columns=['Name', 'White Marks', 'Black Marks'])
    
    # Set the DataFrame index to empty strings
    display_df.index = [""] * len(display_df)

    # Streamlit app main view
    st.title("Pledge Mark Tracker")
    st.dataframe(display_df, use_container_width=True)

    # Interactive selection for detailed view
    selected_name = st.selectbox('Select a name to view details', 
                               [''] + list(marks.keys()))
    
    if selected_name:
        # Adjusted filter logic for detailed info based on the selected name
        detailed_info = df[
            df.apply(lambda row: 
                selected_name.lower().strip() in 
                [name.lower().strip() for name in row['Which pledge is this for?'].split(', ')] 
                and str(row['Submission Password']).strip().lower() == submission_password.strip().lower() 
                and row.get('Approved?', '').lower() == 'yes', 
                axis=1)
        ]
        
        detailed_info.index = [""] * len(detailed_info)
        st.dataframe(detailed_info[[
            'Timestamp', 
            'Which brother is submitting this?', 
            'Description', 
            'What type of mark?', 
            'How many?'
        ]])

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    # Add debugging information
    st.write("If you're seeing this error, please check that the column headers in your Google Sheet match exactly with the expected headers:")
    st.write(expected_headers)