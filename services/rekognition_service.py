import boto3
import requests
import os

class RekognitionService:
    def __init__(self):
        self.rekognition = boto3.client('rekognition')
        self.s3 = boto3.client('s3')

    def analyze_image(self, file_id):
        """
        Analisa a imagem para verificar se há uma pessoa e, se sim, identificar o gênero.
        """
        try:
            # Fazer download da imagem do Telegram e armazenar temporariamente
            file_url = self.get_telegram_file_url(file_id)
            image_data = requests.get(file_url).content

            # Enviar imagem para análise no Rekognition
            response = self.rekognition.detect_faces(
                Image={"Bytes": image_data},
                Attributes=["ALL"]
            )

            if not response["FaceDetails"]:
                return "Nenhuma pessoa foi identificada na imagem."

            # Iterar pelas faces detectadas
            result = []
            for face in response["FaceDetails"]:
                gender = face["Gender"]["Value"]
                confidence = face["Gender"]["Confidence"]
                result.append(f"Detectado: {gender} com confiança de {confidence:.2f}%.")

            return "\n".join(result)

        except Exception as e:
            print(f"Erro ao analisar imagem: {e}")
            return "Erro ao processar a imagem."

    def get_telegram_file_url(self, file_id):
        """
        Obtém a URL do arquivo de imagem do Telegram.
        """
        base_url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}"
        file_info = requests.get(f"{base_url}/getFile?file_id={file_id}").json()
        file_path = file_info["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{os.environ['TELEGRAM_TOKEN']}/{file_path}"
