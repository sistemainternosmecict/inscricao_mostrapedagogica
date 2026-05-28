from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import re

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
CREDS_FILE = 'creds.json'

class Gide:
    def __init__(self):
        try:
            creds = service_account.Credentials.from_service_account_file(
                CREDS_FILE, scopes=SCOPES)
            self.service = build('drive', 'v3', credentials=creds)
            self.docs_service = build('docs', 'v1', credentials=creds)
            print("Google Drive and Docs services initialized successfully.")
        except Exception as e:
            print(f"Error initializing Google Drive or Docs services: {e}")
            self.service = None

    def criar_pasta(self, folder_name, parent_folder_id=None):
        if not self.service:
            print("Service not initialized. Cannot create folder.")
            return None

        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        try:
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            print(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
            return folder.get('id')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def _find_folder_id(self, folder_name, parent_folder_id):
        if not self.service:
            print("Service not initialized. Cannot find folder.")
            return None
        
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_folder_id}' in parents and trashed=false"
        try:
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print(f"No folder found with name '{folder_name}' in parent '{parent_folder_id}'.")
                return None
            return items[0]['id']
        except HttpError as error:
            print(f"An error occurred while finding folder: {error}")
            return None

    def _build_docs_insert_requests(self, content_string):
        requests = []
        current_index = 1 # Google Docs API uses 1-based indexing for content
        
        # Regex to find URLs
        url_pattern = r"https?://[^\s]+" 

        last_match_end = 0
        for match in re.finditer(url_pattern, content_string):
            # Add text before the URL
            pre_url_text = content_string[last_match_end:match.start()]
            if pre_url_text:
                requests.append({
                    'insertText': {
                        'location': {'segmentId': '', 'index': current_index},
                        'text': pre_url_text
                    }
                })
                current_index += len(pre_url_text)

            # Add the URL as a clickable link
            url_text = match.group(0)
            requests.append({
                'insertText': {
                    'location': {'segmentId': '', 'index': current_index},
                    'text': url_text
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {
                        'segmentId': '',
                        'startIndex': current_index,
                        'endIndex': current_index + len(url_text)
                    },
                    'textStyle': {
                        'link': {
                            'url': url_text
                        }
                    },
                    'fields': 'link'
                }
            })
            current_index += len(url_text)
            last_match_end = match.end()

        # Add any remaining text after the last URL
        remaining_text = content_string[last_match_end:]
        if remaining_text:
            requests.append({
                'insertText': {
                    'location': {'segmentId': '', 'index': current_index},
                    'text': remaining_text
                }
            })
            current_index += len(remaining_text)
        
        return requests

    def criar_arquivo_docs(self, doc_name, content_to_insert, shared_folder_id, subfolder_name):
        if not self.service or not self.docs_service:
            print("Drive or Docs service not initialized. Cannot create document.")
            return None

        # 1. Find the subfolder ID
        subfolder_id = self._find_folder_id(subfolder_name, shared_folder_id)
        if not subfolder_id:
            print(f"Subfolder '{subfolder_name}' not found within shared folder ID '{shared_folder_id}'. Cannot create document.")
            return None

        # 2. Create the Docs file
        document_body = {'title': doc_name}
        try:
            doc = self.docs_service.documents().create(body=document_body).execute()
            document_id = doc.get('documentId')
            print(f"Google Doc '{doc_name}' created with ID: {document_id}")
        except HttpError as error:
            print(f"An error occurred while creating document: {error}")
            return None

        # 3. Insert content into the Docs file
        requests = self._build_docs_insert_requests(content_to_insert)
        
        if requests: # Only batch update if there are requests
            try:
                self.docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
                print(f"Content added to document {document_id}.")
            except HttpError as error:
                print(f"An error occurred while inserting content: {error}")
                # If content insertion fails, we should still try to move the document
                # or handle it appropriately. For now, just print error.

        # 4. Move the Docs file to the subfolder
        try:
            # First remove from root (or wherever it was created by default)
            self.service.files().update(fileId=document_id,
                                        removeParents='root', # Assuming it's created in root
                                        addParents=subfolder_id,
                                        fields='id, parents').execute()
            print(f"Document '{doc_name}' moved to folder ID: {subfolder_id}")
            return document_id
        except HttpError as error:
            print(f"An error occurred while moving document: {error}")
            return None

    def criar_estrutura_categoria_unidade(self, categoria_name, ue_name, root_folder_id):
        if not self.service:
            print("Service not initialized. Cannot create folder structure.")
            return None

        # 1. Find or Create Categoria Folder
        categoria_folder_id = self._find_folder_id(categoria_name, root_folder_id)
        if not categoria_folder_id:
            # If not found, try to create it
            categoria_folder_id = self.criar_pasta(categoria_name, root_folder_id)
            if not categoria_folder_id:
                print(f"Failed to create Category folder: {categoria_name}")
                return None
        
        # 2. Find or Create UE Folder inside Categoria Folder
        ue_folder_id = self._find_folder_id(ue_name, categoria_folder_id)
        if not ue_folder_id:
            # If not found, try to create it
            ue_folder_id = self.criar_pasta(ue_name, categoria_folder_id)
            if not ue_folder_id:
                print(f"Failed to create UE folder: {ue_name}")
                return None
        
        return ue_folder_id


if __name__ == '__main__':
    # This block is for local testing of the Gide class
    # Replace 'YOUR_PARENT_FOLDER_ID' with the actual ID of your shared folder
    # You can get this ID from the URL when you open the shared folder in Google Drive
    gide_instance = Gide()
    if gide_instance.service:
        # Example: Create a folder named 'Test Folder from Gide' in the root of the drive
        # If you want to create it in a specific shared folder, provide its ID
        parent_id = input("Enter the ID of the parent folder where you want to create the new folder (leave empty for root): ").strip()
        new_folder_name = input("Enter the name of the new folder to create: ").strip()

        if new_folder_name:
            created_folder_id = gide_instance.criar_pasta(new_folder_name, parent_id if parent_id else None)
            if created_folder_id:
                print(f"Successfully created folder: {new_folder_name} (ID: {created_folder_id})")
            else:
                print(f"Failed to create folder: {new_folder_name}")
        else:
            print("Folder name cannot be empty.")
