from flask import Flask, request, jsonify
from flask_cors import CORS
from pprint import pprint
import os
from modules.gide import Gide # Import the Gide class
import re

app = Flask(__name__)
CORS(app)

GOOGLE_DRIVE_ROOT_FOLDER_ID = "15UaJIAtDxLd7qGYr_JZ6DscqAkWejxgX"
gide_instance = Gide()
url_pattern = re.compile(r"https?://[^\s]+")


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
    # Limit processing to a maximum of 10 participants, as specified by the user
    max_participants = min(num_participants, 10)
    for i in range(1, max_participants + 1):
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

            doc_content_lines = []
            url_fields_to_move = []

            for key, value in doc_data.items():
                if key == "participantes" and isinstance(value, list):
                    if value: # Only add participants section if there are participants
                        doc_content_lines.append(f"{key.replace('-', ' ').title()}:")
                        for i, participant in enumerate(value):
                            nome = participant.get("nome_completo", "N/A")
                            matricula = participant.get("matricula", "N/A")
                            cpf = participant.get("cpf", "N/A")
                            doc_content_lines.append(f"  Participante {i+1} - {nome} / {matricula} / {cpf}")
                elif isinstance(value, str) and url_pattern.search(value):
                    url_fields_to_move.append(f"{key.replace('-', ' ').title()}: {value}")
                else:
                    # Exclude the "numero-participantes" field from the main display
                    if key != "numero-participantes":
                        doc_content_lines.append(f"{key.replace('-', ' ').title()}: {value}")

            doc_content = "\n".join(doc_content_lines)

            # Append URL fields at the bottom, separated by a horizontal bar
            if url_fields_to_move:
                doc_content += "\n\n----------------------------------------------------\n\n"
                doc_content += "Links Relacionados:\n"
                doc_content += "\n".join(url_fields_to_move)

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
