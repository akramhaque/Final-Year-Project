from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=1, description="Full Name")
    email: EmailStr = Field(..., description="Email address")
    mobile_number: str = Field(..., description="10-digit mobile number")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")

    @field_validator('mobile_number')
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        v_clean = v.strip()
        if not re.match(r'^[6-9]\d{9}$', v_clean):
            raise ValueError('Mobile number must be a valid 10-digit Indian mobile number.')
        return v_clean

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    mobile_number: str

    class Config:
        from_attributes = True   # Pydantic v2

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class PredictionRequest(BaseModel):
    transaction_id: str = Field(..., min_length=10)
    amount: float = Field(..., gt=0)
    transaction_time: str
    transaction_type: str
    bank_name: str

class PredictionResponse(BaseModel):
    prediction: str
    fraud: bool
    confidence: float
