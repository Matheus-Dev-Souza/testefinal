import json
from src.services.rekognition_service import RekognitionService

rekognition_service = RekognitionService()

def handle_rekognition_event(event, context):
    """
    Processa imagens recebidas do Telegram para análise pelo Rekognition.
    """
    try:
        body = json.loads(event["body"])
        file_id = body["message"]["photo"][-1]["file_id"]

        analysis_result = rekognition_service.analyze_image(file_id)

        return {
            "statusCode": 200,
            "body": json.dumps({"result": analysis_result})
        }
    except Exception as e:
        print(f"Erro ao processar imagem no Rekognition: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro interno ao processar imagem"})
        }
