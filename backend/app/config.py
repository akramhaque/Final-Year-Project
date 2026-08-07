import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/upi_fraud_detection"
    )
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "8f1a14a38be98f123d463e261f9dfa052e4f014e7a83d7890f9c2d667c458a2d"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/ml/upi_fraud_model.pkl")

settings = Settings()
