import json
from src.services.lex_service import LexService

lex_service = LexService()

def handle_lex_event(event, context):
    """
    Processa mensagens recebidas do Telegram e encaminha para o Amazon Lex.
    """
    try:
        body = json.loads(event["body"])
        chat_id = body["message"]["chat"]["id"]
        user_message = body["message"]["text"]

        response = lex_service.process_message(chat_id, user_message)

        return {
            "statusCode": 200,
            "body": json.dumps({"response": response})
        }
    except Exception as e:
        print(f"Erro ao processar evento no Lex: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro interno ao processar mensagem no Lex"})
        }
