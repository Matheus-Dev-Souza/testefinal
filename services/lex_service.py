import os
import boto3

class LexService:
    def __init__(self):
        self.lex_client = boto3.client('lexv2-runtime')

    def process_message(self, chat_id, text):
        response = self.lex_client.recognize_text(
            botId=os.environ['BOT_ID'],
            botAliasId=os.environ['BOT_ALIAS_ID'],
            localeId=os.environ['LOCALE_ID'],
            sessionId=str(chat_id),
            text=text
        )
        return response.get('messages', [{}])[0].get('content', 'Desculpe, não entendi.')
