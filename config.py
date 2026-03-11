import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ODPT_API_KEY = os.getenv('ODPT_API_KEY')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 5))
    USE_SQLITE = os.getenv('USE_SQLITE', 'False').lower() == 'true'

    @classmethod
    def validate(cls):
        required = ['ODPT_API_KEY', 'EMAIL_SENDER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENT']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")