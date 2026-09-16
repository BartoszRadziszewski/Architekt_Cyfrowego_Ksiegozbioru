import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import src.config as config

class DriveService:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_file(
            config.GOOGLE_APPLICATION_CREDENTIALS, scopes=scopes)
        self.service = build('drive', 'v3', credentials=creds)

    def list_files_in_folder(self, folder_id):
        """Pobiera listę plików i folderów z pojedynczego katalogu."""
        results = []
        page_token = None
        while True:
            query = f"'{folder_id}' in parents and trashed=false"
            response = self.service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)',
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            results.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return results

    def list_files_and_folders_recursive(self, parent_folder_id, ignore_folder_ids=None):
        """Przeszukuje całe drzewo katalogów na Dowolną głębokość zagnieżdżenia."""
        if ignore_folder_ids is None:
            ignore_folder_ids = []
            
        all_files = []
        all_folders = []
        folders_to_scan = [parent_folder_id]
        
        while folders_to_scan:
            current_folder = folders_to_scan.pop(0)
            if current_folder in ignore_folder_ids:
                continue
                
            items = self.list_files_in_folder(current_folder)
            for item in items:
                if item.get('mimeType') == 'application/vnd.google-apps.folder':
                    if item['id'] not in ignore_folder_ids:
                        folders_to_scan.append(item['id'])
                        all_folders.append(item)
                else:
                    all_files.append(item)
                    
        return all_files, all_folders

    def find_file_by_name(self, folder_id, filename):
        """Wyszukuje plik o konkretnej nazwie w folderze."""
        query = f"'{folder_id}' in parents and name='{filename}' and trashed=false"
        response = self.service.files().list(
            q=query, 
            spaces='drive', 
            fields='files(id, name)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        files = response.get('files', [])
        return files[0] if files else None

    def download_file(self, file_id):
        """Pobiera zawartość tekstową pliku."""
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return fh.getvalue().decode('utf-8')

    def upload_file(self, filename, content, parent_folder_id, mime_type='text/plain'):
        """Przesyła nowy plik lub aktualizuje istniejący."""
        existing = self.find_file_by_name(parent_folder_id, filename)
        
        file_metadata = {'name': filename}
        media = MediaIoBaseUpload(io.BytesIO(content.encode('utf-8')), mimetype=mime_type, resumable=True)
        
        if existing:
            return self.service.files().update(
                fileId=existing['id'], 
                media_body=media,
                supportsAllDrives=True
            ).execute()
        else:
            file_metadata['parents'] = [parent_folder_id]
            return self.service.files().create(
                body=file_metadata, 
                media_body=media, 
                fields='id',
                supportsAllDrives=True
            ).execute()

    def rename_file(self, file_id, new_name):
        """Zmienia nazwę pliku lub folderu fizycznie na Dysku Google."""
        body = {'name': new_name}
        return self.service.files().update(
            fileId=file_id,
            body=body,
            supportsAllDrives=True
        ).execute()

    def move_file(self, file_id, current_parent_id, new_parent_id):
        """Przenosi plik do innego folderu (np. do archiwum)."""
        return self.service.files().update(
            fileId=file_id,
            addParents=new_parent_id,
            removeParents=current_parent_id,
            supportsAllDrives=True
        ).execute()
