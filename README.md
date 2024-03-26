Playlist Image Organizer Script
Overview
This Python script automates the task of organizing and presenting photos for 100 playlists in a personal project. It was developed to facilitate the creation of a collage for the celebratory 200th playlist.

Challenge
The challenge involved managing and selecting images from folders in Google Drive, where each playlist folder contained multiple image types (raw, edited, and publish-ready), along with text and CSV files.

Solution
The script navigates through each folder in Google Drive, identifies the most recently updated image relevant to each playlist, and saves it to a predefined directory on a personal computer. This automation saved considerable time and minimized potential manual errors.

Results
Efficiently, the script retrieved and saved 95 out of 100 target images in under half an hour, significantly advancing the logistical aspect of the project.

Features
Automated Folder Navigation: Traverses through specified Google Drive folders.
Image Filtering and Selection: Identifies and selects the latest updated image from each folder.
Local File Saving: Automates the saving of images to a designated local directory.
Technical Details
Language & Libraries: Python, with google-api-python-client and google-auth for Google Drive API interaction.
Authentication: Employs a service account for secure Google Drive access.
Customization: Adaptable to various folder structures and file selection criteria.
Usage
Install Python 3 and the required libraries.
Set the KEY_PATH to your service account key file.
Define the DOWNLOAD_PATH for saving images.
Run the script to start the image organization process.
