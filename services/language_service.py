import boto3
import json

class LanguageService:
    def __init__(self):
        self.bedrock = boto3.client('bedrock')

    def translate_text(self, text, source_lang, target_lang):
        """
        Traduz texto utilizando o modelo de linguagem Amazon Titan.
        """
        try:
            prompt = f"Traduza o seguinte texto de {source_lang} para {target_lang}: '{text}'"
            
            # Corpo da requisição
            request_body = json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 4096,
                    "stopSequences": [],
                    "temperature": 0.2,  # Ajuste a temperatura conforme necessário
                    "topP": 0.9
                }
            })

            response = self.bedrock.invoke_model(
                modelId="amazon.titan-text",
                contentType="application/json",
                accept="application/json",
                body=request_body
            )

            result = json.loads(response['body'])
            translated_text = result.get('outputText', 'Tradução não disponível.')
            return translated_text

        except Exception as e:
            print(f"Erro ao traduzir texto: {e}")
            return "Erro ao traduzir o texto."

    def get_language_tips(self, language):
        """
        Gera dicas úteis para aprendizado de idiomas utilizando o Amazon Titan.
        """
        try:
            prompt = (
                f"Eu sou um assistente de idiomas. Por favor, forneça dicas práticas, motivadoras e úteis para "
                f"aprender o idioma {language}. Certifique-se de incluir exemplos claros."
            )
            
            # Corpo da requisição
            request_body = json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 4096,
                    "stopSequences": [],
                    "temperature": 0.2,  # Ajuste a temperatura conforme necessário
                    "topP": 0.9
                }
            })

            response = self.bedrock.invoke_model(
                modelId="amazon.titan-text",
                contentType="application/json",
                accept="application/json",
                body=request_body
            )

            result = json.loads(response['body'])
            language_tips = result.get('outputText', 'Dicas não disponíveis.')
            return language_tips

        except Exception as e:
            print(f"Erro ao gerar dicas de idioma: {e}")
            return f"Erro ao gerar dicas para o idioma {language}."

    def summarize_text(self, text):
        """
        Resume um texto fornecido usando o Amazon Titan.
        """
        try:
            prompt = f"Resuma o seguinte texto de forma clara e concisa: '{text}'"
            
            # Corpo da requisição
            request_body = json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 4096,
                    "stopSequences": [],
                    "temperature": 0.2,  # Ajuste a temperatura conforme necessário
                    "topP": 0.9
                }
            })

            response = self.bedrock.invoke_model(
                modelId="amazon.titan-text",
                contentType="application/json",
                accept="application/json",
                body=request_body
            )

            result = json.loads(response['body'])
            summary = result.get('outputText', 'Resumo não disponível.')
            return summary

        except Exception as e:
            print(f"Erro ao resumir texto: {e}")
            return "Erro ao resumir o texto."
