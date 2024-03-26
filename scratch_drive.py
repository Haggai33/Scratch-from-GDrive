from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import os
import re

# נתיב לקובץ האימות של ה-service account
KEY_PATH = "C:/Aum.music/aum-scratch-photo-7a9af6401878.json"

# נתיב לתיקיית ההורדות במחשב שלך
DOWNLOAD_PATH = "C:/Users/User/Downloads/Aum scratch"

# פרטי היוזר והתיקייה
user_email = "chagai33@gmail.com"
folder_id = "1elTc3Dq2jd5GghwFsSUIVcJPwl2IQYif"

try:
    # יצירת אימות ל-Google Drive API
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    service = build('drive', 'v3', credentials=credentials)
    print("התחברות ל-Google Drive הצליחה.")
except Exception as e:
    print(f"שגיאה בהתחברות ל-Google Drive: {e}")
    exit(1)

# פונקציה לחיפוש תיקיות
def search_folders(service, query):
    try:
        results = service.files().list(q=query, fields="files(id, name, mimeType, modifiedTime)").execute()
        return results.get('files', [])
    except Exception as e:
        print(f"שגיאה בחיפוש תיקיות: {e}")
        return []

# השגת רשימת התיקיות
folders = search_folders(service, f"'1elTc3Dq2jd5GghwFsSUIVcJPwl2IQYif' in parents")
if folders:
    print(f"נמצאו {len(folders)} תיקיות.")
else:
    print("לא נמצאו תיקיות.")
    exit(1)

# חיפוש תיקיות עם "#" בתחילת השם ומספר בין 101 ל-200
matching_folders = [folder for folder in folders if folder['name'].startswith("#") and re.search(r"\b(1[0-9]{2}|200)\b", folder['name'])]
if matching_folders:
    print(f"נמצאו {len(matching_folders)} תיקיות מתאימות.")
else:
    print("לא נמצאו תיקיות מתאימות.")
    exit(1)

# פונקציה לחיפוש והורדת קובץ התמונה האחרון
def download_latest_image(service, folder_id):
    try:
        images = search_folders(service, f"mimeType contains 'image/' and '{folder_id}' in parents")
        if images:
            latest_image = max(images, key=lambda x: x['modifiedTime'])
            request = service.files().get_media(fileId=latest_image['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            fh.seek(0)
            with open(os.path.join(DOWNLOAD_PATH, latest_image['name']), 'wb') as file_out:
                file_out.write(fh.read())
            print(f"הורדה: {latest_image['name']}")
        else:
            print("לא נמצאו תמונות בתיקייה.")
    except Exception as e:
        print(f"שגיאה בהורדת קובץ:{e}")

# הורדת תמונת העריכה האחרונה מכל תיקייה מתאימה
for folder in matching_folders:
    print(f"מעבד תיקייה: {folder['name']}")
    download_latest_image(service, folder['id'])

print("הורדה הושלמה!")
