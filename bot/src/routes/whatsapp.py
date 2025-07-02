from flask import Blueprint, request, jsonify
from src.models.conversation import db, Conversation, Appointment
from src.services.bot_logic import BotLogic
import json
import os

whatsapp_bp = Blueprint('whatsapp', __name__)
bot_logic = BotLogic()

@whatsapp_bp.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificação do webhook do WhatsApp Business API"""
    verify_token = os.environ.get('VERIFY_TOKEN', 'DENTINHOS_VERIFY_TOKEN')
    
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == verify_token:
            print("Webhook verificado com sucesso!")
            return challenge
        else:
            return "Token de verificação inválido", 403
    
    return "Parâmetros inválidos", 400

@whatsapp_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """Processa mensagens recebidas do WhatsApp"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "error", "message": "Dados inválidos"}), 400
        
        # Processa cada entrada de mensagem
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change.get('field') == 'messages':
                            process_message(change['value'])
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"Erro ao processar webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def process_message(message_data):
    """Processa uma mensagem individual"""
    try:
        if 'messages' in message_data:
            for message in message_data['messages']:
                phone_number = message['from']
                message_text = message.get('text', {}).get('body', '')
                message_id = message['id']
                
                # Salva a mensagem no banco de dados
                conversation = Conversation(
                    phone_number=phone_number,
                    message=message_text,
                    message_type='incoming',
                    status='received'
                )
                db.session.add(conversation)
                db.session.commit()
                
                # Processa a mensagem e gera resposta
                response = bot_logic.process_message(message_text, phone_number)
                
                if response:
                    # Atualiza a conversa com a resposta
                    conversation.response = response
                    conversation.status = 'processed'
                    db.session.commit()
                    
                    # Aqui você enviaria a resposta via WhatsApp Business API
                    # send_whatsapp_message(phone_number, response)
                    print(f"Resposta para {phone_number}: {response}")
                
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")

@whatsapp_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Retorna todas as conversas para a interface administrativa"""
    try:
        conversations = Conversation.query.order_by(Conversation.timestamp.desc()).all()
        return jsonify([conv.to_dict() for conv in conversations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@whatsapp_bp.route('/appointments', methods=['GET'])
def get_appointments():
    """Retorna todos os agendamentos para a interface administrativa"""
    try:
        appointments = Appointment.query.order_by(Appointment.timestamp.desc()).all()
        return jsonify([apt.to_dict() for apt in appointments])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@whatsapp_bp.route('/appointments/<int:appointment_id>/status', methods=['PUT'])
def update_appointment_status(appointment_id):
    """Atualiza o status de um agendamento"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        appointment = Appointment.query.get_or_404(appointment_id)
        appointment.status = new_status
        db.session.commit()
        
        return jsonify(appointment.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

