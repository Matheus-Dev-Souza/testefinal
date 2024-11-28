import json
from src.services.transcribe_service import TranscribeService

transcribe_service = TranscribeService()

def handle_transcribe_event(event, context):
    """
    Processa áudios recebidos do Telegram para transcrição pelo Transcribe.
    """
    try:
        body = json.loads(event["body"])
        file_id = body["message"]["voice"]["file_id"]

        transcription_result = transcribe_service.process_audio(file_id)

        return {
            "statusCode": 200,
            "body": json.dumps({"transcription": transcription_result})
        }
    except Exception as e:
        print(f"Erro ao processar áudio no Transcribe: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro interno ao processar áudio"})
        }
