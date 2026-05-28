from flask import Flask, request, jsonify
from flask_cors import CORS
from pprint import pprint
import os
from modules.gide import Gide # Import the Gide class

app = Flask(__name__)
CORS(app)

GOOGLE_DRIVE_ROOT_FOLDER_ID = "15UaJIAtDxLd7qGYr_JZ6DscqAkWejxgX"
gide_instance = Gide()


def mask_matricula(matricula):
    if not matricula or len(matricula) < 2:
        return matricula
    return matricula[0] + 'X' * (len(matricula) - 2) + matricula[-1]

def mask_cpf(cpf):
    if not cpf or len(cpf) < 5:
        return cpf
    return cpf[:3] + 'X' * (len(cpf) - 5) + cpf[-2:]

def process_participants(data, num_participants):
    participants = []
    for i in range(1, num_participants + 1):
        p_prefix = f"{i}p-"
        participant_data = {}
        found_participant_data = False
        for key, value in data.items():
            if key.startswith(p_prefix):
                new_key = key[len(p_prefix):] # Remove prefix
                if "matricula" in new_key and value:
                    participant_data[new_key] = mask_matricula(value)
                elif "cpf" in new_key and value:
                    participant_data[new_key] = mask_cpf(value)
                else:
                    participant_data[new_key] = value
                found_participant_data = True
        if found_participant_data:
            participants.append(participant_data)
    return participants


@app.route("/")
def index():
    return "API online"

@app.route("/inscricao_entrada", methods=["POST"])
def inscricao_entrada():
    if request.is_json:
        data = request.get_json()
        print("--- dados passados via api ---")
        pprint(data)
        print("-----------------------------")

        try:
            # Extract main fields
            telefone = data.get("telefone", "")
            eixo_tematico = data.get("eixo-tematico", "")
            inst_diag_integra_tec = data.get("inst-diag-integra-tec", "")
            autorizacao_imagem_item_edital = data.get("autorizacao-imagem-item-edital", "")
            email = data.get("email", "")
            categoria = data.get("categoria", "")
            ue = data.get("ue", "")
            projeto = data.get("projeto", "")
            resumo = data.get("resumo", "")
            fichasDeInscricao = data.get("fichasDeInscricao", "")
            projetoIntegra = data.get("projetoIntegra", "")
            videoProjeto = data.get("videoProjeto", "")
            arquivosComplementares = data.get("arquivosComplementares", "")
            direitoDeImagem = data.get("direitoDeImagem", "")
            numero_participantes = int(data.get("numero-participantes", 0))

            # Process participants
            processed_participants = process_participants(data, numero_participantes)
            
            # Prepare data for Gide
            doc_data = {
                "telefone": telefone,
                "eixo-tematico": eixo_tematico,
                "inst-diag-integra-tec": inst_diag_integra_tec,
                "autorizacao-imagem-item-edital": autorizacao_imagem_item_edital,
                "email": email,
                "categoria": categoria,
                "ue": ue,
                "projeto": projeto,
                "resumo": resumo,
                "fichasDeInscricao": fichasDeInscricao,
                "projetoIntegra": projetoIntegra,
                "videoProjeto": videoProjeto,
                "arquivosComplementares": arquivosComplementares,
                "direitoDeImagem": direitoDeImagem,
                "numero-participantes": numero_participantes,
                "participantes": processed_participants
            }

            # --- Gide Integration ---
            if not gide_instance.service:
                return jsonify({"error": "Google Drive service not initialized."}), 500

            # 1. Create/Get Categoria and UE Folders
            ue_folder_id = gide_instance.criar_estrutura_categoria_unidade(categoria, ue, GOOGLE_DRIVE_ROOT_FOLDER_ID)
            if not ue_folder_id:
                return jsonify({"error": f"Failed to create or find folder structure for Category: {categoria}, UE: {ue}"}), 500
            
            # 2. Create/Get Projeto Folder inside UE Folder
            projeto_folder_id = gide_instance.criar_pasta(projeto, ue_folder_id)
            if not projeto_folder_id:
                projeto_folder_id = gide_instance._find_folder_id(projeto, ue_folder_id)
                if not projeto_folder_id:
                    return jsonify({"error": f"Failed to create or find Project folder: {projeto}"}), 500

            # 3. Create Google Doc with processed data
            doc_name = f"Inscricao_{projeto}_{telefone}"
            
            # Convert doc_data to a formatted string for the Google Doc
            doc_content = ""
            for key, value in doc_data.items():
                if isinstance(value, list): # For participants
                    doc_content += f"{key.replace('-', ' ').title()}:\n"
                    for i, participant in enumerate(value):
                        doc_content += f"  Participante {i+1}:\n"
                        for p_key, p_value in participant.items():
                            doc_content += f"    {p_key.replace('-', ' ').title()}: {p_value}\n"
                else:
                    doc_content += f"{key.replace('-', ' ').title()}: {value}\n"


            # The `criar_arquivo_docs` function in gide.py expects `data` to be a dict
            # and extracts specific keys for the initial insert.
            # I will need to modify `gide.py` to accept the full formatted string,
            # or modify this section to fit `gide.py`'s current behavior
            # Let's adjust gide.py to accept a full string for content
            # For now, I will pass the doc_data directly, but recognize that
            # gide.py will only use a few hardcoded fields.
            # A better approach: modify gide.py's `criar_arquivo_docs` to accept a `content_string` parameter
            # For this iteration, I'll pass a simplified dict to match `gide.py`'s current content handling.
            # Then I'll refine `gide.py` if needed.

            document_id = gide_instance.criar_arquivo_docs(doc_name, doc_content, ue_folder_id, projeto)

            if not document_id:
                return jsonify({"error": "Failed to create Google Doc."}), 500


            return jsonify({"message": "Dados recebidos e processados com sucesso!", "document_id": document_id}), 200
        except KeyError as e:
            return jsonify({"error": f"Missing key in JSON data: {e}"}), 400
        except ValueError as e:
            return jsonify({"error": f"Invalid value: {e}"}), 400
        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == "__main__":
    app.run()
