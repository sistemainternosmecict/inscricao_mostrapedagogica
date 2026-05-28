from modules.gide import Gide
from datetime import datetime
from dotenv import load_dotenv
import os

def main():
    load_dotenv() # Load environment variables from .env file

    gide_instance = Gide()
    if gide_instance.service and gide_instance.docs_service:
        # --- Test for criar_pasta ---
        # Replace 'YOUR_SHARED_FOLDER_ID' with the actual ID of your shared folder
        shared_folder_id = os.getenv("SHARED_FOLDER_ID")  # <--- IMPORTANT: Read from .env

        if shared_folder_id == "YOUR_SHARED_FOLDER_ID":
            print("""
WARNING: Please replace 'YOUR_SHARED_FOLDER_ID' in app.py with your actual shared folder ID.""")
            print("Cannot proceed without a valid shared folder ID.")
            return

        # Example for creating a new subfolder if it doesn't exist
        subfolder_name_for_docs = "Documentos Gerados"
        print(f"""
Attempting to find or create subfolder '{subfolder_name_for_docs}'...""")
        docs_subfolder_id = gide_instance._find_folder_id(subfolder_name_for_docs, shared_folder_id)
        
        if not docs_subfolder_id:
            print(f"Subfolder '{subfolder_name_for_docs}' not found, creating it...")
            docs_subfolder_id = gide_instance.criar_pasta(subfolder_name_for_docs, shared_folder_id)
            if not docs_subfolder_id:
                print(f"Failed to create subfolder '{subfolder_name_for_docs}'. Exiting.")
                return
            else:
                print(f"Successfully created subfolder '{subfolder_name_for_docs}' with ID: {docs_subfolder_id}")
        else:
            print(f"Subfolder '{subfolder_name_for_docs}' found with ID: {docs_subfolder_id}")


        # --- Test for criar_arquivo_docs ---
        doc_data = {
            "unidade_escolar": "Escola Modelo de Teste",
            "email_principal": "teste@escolamodelo.com",
            "categoria": "Ensino Fundamental"
        }
        doc_name = f"Inscricao_{doc_data['unidade_escolar'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        print(f"""
Attempting to create Google Doc '{doc_name}' with data: {doc_data}""")
        created_doc_id = gide_instance.criar_arquivo_docs(doc_name, doc_data, shared_folder_id, subfolder_name_for_docs)

        if created_doc_id:
            print(f"App.py: Successfully created Google Doc: {doc_name} (ID: {created_doc_id})")
        else:
            print(f"App.py: Failed to create Google Doc: {doc_name}")

    else:
        print("App.py: Gide service(s) not initialized. Check credentials and network.")

if __name__ == '__main__':
    main()
