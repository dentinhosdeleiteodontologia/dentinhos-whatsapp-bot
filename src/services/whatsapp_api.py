import requests
import os

class WhatsAppAPI:
    def __init__(self):
        self.PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
        self.ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
        self.API_URL = f"https://graph.facebook.com/v19.0/{self.PHONE_NUMBER_ID}/messages"

    def send_whatsapp_message(self, to_number, message_body ):
        headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message_body
            }
        }
        try:
            response = requests.post(self.API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            print(f"Mensagem enviada com sucesso para {to_number}: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar mensagem para {to_number}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Detalhes do erro: {e.response.text}")
            return None
