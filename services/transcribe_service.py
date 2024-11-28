import os
import boto3
import requests
import time

class TranscribeService:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.transcribe = boto3.client('transcribe')

    def process_audio(self, file_id):
        """
        Processa o áudio, salvando no S3, iniciando e recuperando a transcrição.
        """
        try:
            # 1. Fazer download do áudio do Telegram
            audio_url = self.get_telegram_file_url(file_id)
            audio_data = requests.get(audio_url).content

            # 2. Enviar áudio para o S3
            bucket_name = os.environ['BUCKET_NAME']
            audio_key = f"audio/{file_id}.ogg"
            self.s3.put_object(Bucket=bucket_name, Key=audio_key, Body=audio_data)

            # 3. Iniciar o job de transcrição
            job_name = f"transcription-{file_id}"
            audio_s3_uri = f"s3://{bucket_name}/{audio_key}"
            self.transcribe.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': audio_s3_uri},
                MediaFormat='ogg',
                LanguageCode='en-US'  # Substitua pelo idioma desejado
            )

            # 4. Aguardar conclusão e obter o resultado
            return self.wait_for_transcription(job_name)
        except Exception as e:
            print(f"Erro ao processar áudio: {e}")
            return "Erro ao processar o áudio."

    def wait_for_transcription(self, job_name):
        """
        Aguarda a conclusão do job de transcrição e retorna o texto transcrito.
        """
        while True:
            response = self.transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']

            if status == 'COMPLETED':
                # Fazer download da transcrição
                transcript_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                transcript_data = requests.get(transcript_url).json()
                return transcript_data['results']['transcripts'][0]['transcript']

            if status == 'FAILED':
                return "Falha na transcrição do áudio."

            # Aguardar 5 segundos antes de verificar novamente
            time.sleep(5)

    def get_telegram_file_url(self, file_id):
        """
        Obtém a URL do arquivo de áudio do Telegram.
        """
        base_url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}"
        file_info = requests.get(f"{base_url}/getFile?file_id={file_id}").json()
        file_path = file_info["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{os.environ['TELEGRAM_TOKEN']}/{file_path}"
