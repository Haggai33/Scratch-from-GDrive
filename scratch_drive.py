from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import os
import re

# Path to the service account authentication file
KEY_PATH = "*********************"

# Path to the download directory on your computer
DOWNLOAD_PATH = "C:/Users/User/Downloads/Aum scratch"

# User and folder details
user_email = "***********"
folder_id = "************"

try:
    # Authenticate with Google Drive API
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    service = build('drive', 'v3', credentials=credentials)
    print("Successfully connected to Google Drive.")
except Exception as e:
    print(f"Error connecting to Google Drive: {e}")
    exit(1)

# Function to search for folders
def search_folders(service, query):
    try:
        results = service.files().list(q=query, fields="files(id, name, mimeType, modifiedTime)").execute()
        return results.get('files', [])
    except Exception as e:
        print(f"Error searching folders: {e}")
        return []

# Get a list of folders
folders = search_folders(service, f"'1elTc3Dq2jd5GghwFsSUIVcJPwl2IQYif' in parents")
if folders:
    print(f"Found {len(folders)} folders.")
else:
    print("No folders found.")
    exit(1)

# Search for folders with "#" at the beginning of the name and a number between 101 and 200
matching_folders = [folder for folder in folders if folder['name'].startswith("#") and re.search(r"\b(1[0-9]{2}|200)\b", folder['name'])]
if matching_folders:
    print(f"Found {len(matching_folders)} matching folders.")
else:
    print("No matching folders found.")
    exit(1)

# Function to search and download the latest image file
def download_latest_image(service, folder_id):
    try:
        images = search_folders(service, f"mimeType contains 'image/' and '{folder_id}' in parents")
        if images:
            latest_image = max(images, key=lambda x: x['modifiedTime'])
            request = service.files().get_media(fileId=latest_image['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            with open(os.path.join(DOWNLOAD_PATH, latest_image['name']), 'wb') as file_out:
                file_out.write(fh.read())
            print(f"Downloaded: {latest_image['name']}")
        else:
            print("No images found in folder.")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Download the latest edited image from each matching folder
for folder in matching_folders:
    print(f"Processing folder: {folder['name']}")
    download_latest_image(service, folder['id'])

print("Download completed!")
