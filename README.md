chatbot-telegram/
├── src/
│   ├── handlers/             # Funções Lambda
│   │   ├── webhook_handler.py
│   │   ├── lex_handler.py
│   │   ├── rekognition_handler.py
│   │   ├── transcribe_handler.py
│   └── services/             # Lógica de negócio para AWS
│       ├── telegram_api.py
│       ├── lex_service.py
│       ├── rekognition_service.py
│       ├── transcribe_service.py
│       └── user_profile_service.py
├── tests/                    # Testes
│   ├── test_handlers.py
│   └── test_services.py
├── serverless.yml            # Configuração do Serverless Framework
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação
└── .env                      # Variáveis de ambiente
