import json
from src.services.telegram_api import TelegramAPI
from src.services.lex_service import LexService
from src.services.transcribe_service import TranscribeService
from src.services.rekognition_service import RekognitionService

telegram_api = TelegramAPI()
lex_service = LexService()
transcribe_service = TranscribeService()
rekognition_service = RekognitionService()

def handle_telegram_event(event, context):
    try:
        body = json.loads(event["body"])
        chat_id = body["message"]["chat"]["id"]

        if "text" in body["message"]:
            user_message = body["message"]["text"]
            lex_response = lex_service.process_message(chat_id, user_message)
            telegram_api.send_message(chat_id, lex_response)

        elif "voice" in body["message"]:
            voice_file_id = body["message"]["voice"]["file_id"]
            transcription = transcribe_service.process_audio(voice_file_id)
            lex_response = lex_service.process_message(chat_id, transcription)
            telegram_api.send_message(chat_id, lex_response)

        elif "photo" in body["message"]:
            photo_file_id = body["message"]["photo"][-1]["file_id"]
            rekognition_result = rekognition_service.analyze_image(photo_file_id)
            telegram_api.send_message(chat_id, rekognition_result)

        return {"statusCode": 200, "body": json.dumps({"message": "Success"})}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal Server Error"})}
