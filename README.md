# [Pledge Mark Tracker App](https://spdslo-pledgev2.streamlit.app/)

## Overview

This app is designed to track and display marks (white and black) for members of an organization. It utilizes Streamlit for web deployment, Google Sheets for data storage, and a Google Cloud Service Account for secure access to the Google Sheets data.

## How It Works

### The App
- The Pledge Mark Tracker app is a web application built using Streamlit, a Python library that simplifies the creation of web apps.
- It interfaces with a Google Sheet to retrieve, process, and display data about the marks awarded to organization members.

### Google Cloud Services and Service Account
- The app uses Google Sheets API, enabled through Google Cloud Services, to interact with the Google Sheets data.
- A service account created in Google Cloud Platform (GCP) provides the necessary credentials for the app to access Google Sheets securely.
- The service account acts as a standalone user with permissions specifically granted to access required resources.

### Streamlit
- Streamlit provides an easy-to-use platform to deploy Python apps as interactive web applications.
- It hosts the app and renders the Python code into web elements.
- Streamlit Sharing is used for deployment, offering an easy way to share the app via a URL.

## Instructions for Streamlit App Use

### Changing to a Different Google Sheet
To adapt the app to a different Google Sheet, follow these steps:

1. **Create or Choose a New Google Sheet**:
   - Ensure the new sheet has the same column structure as the original. Specifically, it should have columns for names, mark counts, mark types, approval status, and any other columns used by the app.

2. **Share the Sheet with the Service Account**:
   - The Google Sheet must be shared with the service account email. This gives the service account the necessary permissions to access the sheet.

3. **Update the Sheet Name in the App**:
   - In the app's Python code, update the sheet name to match the new Google Sheet. This is typically done in the line where the sheet is opened:
     ```python
     sheet = client.open('New Sheet Name').sheet1
     ```

4. **Maintain Column Formatting**:
   - The new sheet must maintain identical column formatting to ensure the app functions correctly. This includes the same column titles and data formats.

5. **Test the App Locally**:
   - Before deploying, test the app locally to ensure it correctly interacts with the new Google Sheet.

6. **Deploy Changes**:
   - Once confirmed working locally, push the changes to your GitHub repository and update the deployment on Streamlit Sharing.
     
7. **A Note on requirements.txt**:
   - Streamlit Sharing requires a list of dependencies in order to deploy the webapp. Here is a list of needed dependencies:
     + streamlit
     + gspread
     + pandas
     + google-auth
     + python-dotenv (optional unless using .env file for local testing)

## Navigating Google Cloud Console

The [Google Cloud Console](https://console.cloud.google.com/) is integral for managing the Google Cloud resources and services your app interacts with. Here's a guide on navigating key aspects of the Google Cloud Console relevant to our app:

### Creating a Service Account
1. **Create a Service Account for Authentication**:
   - Within your Google Cloud project, navigate to "IAM & Admin" > "Service Accounts".
   - Click "Create Service Account" and provide a name and description.
   - Grant the service account necessary roles. For Google Sheets interaction, typically "Editor" role is sufficient.
   - Create a key for the service account in JSON format and securely download it. This key is used in your app for authentication.
   - **NOTE**, this app already has a service account generated, if a new JSON key is generated ensure to change in Streamlit App Advanced Settings
     in the secret section. This must be in toml formatt. 

### Enabling APIs
2. **Enable Required APIs**:
   - Go to "APIs & Services" > "Dashboard".
   - Click "+ ENABLE APIS AND SERVICES" to find and enable necessary APIs for your project.
   - For this app, ensure that the "Google Sheets API" and "Google Drive API" are enabled.

### Sharing Google Sheets with the Service Account
3. **Configure Google Sheets Access**:
   - The Google Sheets used by the app must be shared with the service account.
   - Share the sheet with the email address of the service account, granting "Editor" access.

### Managing API Credentials
4. **Manage API Credentials**:
   - Navigate to "APIs & Services" > "Credentials".
   - Here, you can view and manage the credentials associated with your service account.
   - Ensure your service account's JSON key file is kept secure and private.

### Monitoring and Logging
5. **Use Monitoring and Logging Tools**:
   - Utilize "Logging" and "Monitoring" in the Google Cloud Console to troubleshoot and monitor the API usage and activities.

### Best Practices
- **Least Privilege**: Always follow the principle of least privilege. Grant only the permissions necessary for the service account to function.
- **Security**: Keep your service account's JSON key secure. Do not share it or commit it to public repositories.
- **Cost Management**: Monitor your API usage and understand the [pricing](https://cloud.google.com/pricing) to manage costs effectively.

## Important Notes
- When working with sensitive data, always ensure that access is properly secured and limited.
- The service account should have the least privilege necessary to function, reducing potential security risks.

## Getting Started with Development
To contribute or modify this app, you'll need to set up a local development environment, clone the repository, and install the required dependencies listed in `requirements.txt`. Don't forget to configure your `.env` file or Streamlit secrets with the appropriate Google Cloud Service Account credentials for local testing or deployment.

For detailed instructions on setting up a local development environment, configuring secrets, and deploying the app, refer to the "Deployment" and "Local Development" sections of this document.

