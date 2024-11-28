import json
from services.lex_service import LexService
from services.recognition_service import RekognitionService
from services.transcribe_service import TranscribeService
from services.language_service import LanguageService

# Função de teste para verificar se o serviço está funcionando
def hello(event, context):
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!"
    }

    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

# Função para lidar com eventos do Lex (chatbot)
def lex_handler(event, context):
    lex_service = LexService()

    # Assumindo que o texto recebido é do usuário via webhook (no formato JSON)
    user_input = json.loads(event['body']).get('text')

    if not user_input:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Input text is required"})
        }

    # Processando a entrada no Lex
    lex_response = lex_service.process_lex(user_input)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": lex_response
        })
    }

# Função para lidar com análise de imagem usando Rekognition (identificar pessoa e gênero)
def rekognition_handler(event, context):
    rekognition_service = RekognitionService()

    # Supondo que a imagem seja enviada como um link S3
    image_url = json.loads(event['body']).get('image_url')

    if not image_url:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Image URL is required"})
        }

    # Analisando a imagem
    rekognition_response = rekognition_service.analyze_image(image_url)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": rekognition_response
        })
    }

# Função para lidar com a transcrição de áudio usando Transcribe
def transcribe_handler(event, context):
    transcribe_service = TranscribeService()

    # A URL do arquivo de áudio no S3
    audio_url = json.loads(event['body']).get('audio_url')

    if not audio_url:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Audio URL is required"})
        }

    # Processando o áudio
    transcribe_response = transcribe_service.process_audio(audio_url)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "transcription": transcribe_response
        })
    }

# Função para lidar com tradução e dicas de idioma
def language_handler(event, context):
    language_service = LanguageService()

    text_to_translate = json.loads(event['body']).get('text')
    source_lang = json.loads(event['body']).get('source_lang')
    target_lang = json.loads(event['body']).get('target_lang')

    if not text_to_translate or not source_lang or not target_lang:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Text, source language, and target language are required"})
        }

    # Traduzindo o texto
    translated_text = language_service.translate_text(text_to_translate, source_lang, target_lang)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "translated_text": translated_text
        })
    }
