from fastapi import APIRouter, Depends, HTTPException, Request, status
import pandas as pd
from app.auth import get_current_user
from app.models import User
from app.schemas import PredictionRequest, PredictionResponse
from app.utils import hash_transaction_id, normalize_bank_name

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictionResponse)
def predict(
    request: Request, 
    body: PredictionRequest, 
    current_user: User = Depends(get_current_user)
):
    """
    Protected prediction API. Preprocesses features, runs inference,
    and returns whether the transaction is Fraud or Legitimate with confidence probability.
    """
    # Retrieve preloaded model from app state
    model = getattr(request.app.state, "model", None)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Machine learning model is not loaded on startup."
        )
        
    try:
        # Robustly parse transaction_time using pandas to_datetime
        dt = pd.to_datetime(body.transaction_time.replace('T', ' '))
        
        # Extract features
        hour = dt.hour
        day_of_week = dt.weekday()  # Monday = 0, Sunday = 6
        is_night_time = 1 if (hour >= 22 or hour < 6) else 0
        
        # Preprocess features
        processed_id = hash_transaction_id(body.transaction_id)
        normalized_bank = normalize_bank_name(body.bank_name)
        
        # Form DataFrame matching the training feature names and order exactly
        input_data = pd.DataFrame([{
            'TransactionID': processed_id,
            'Amount': body.amount,
            'Hour': hour,
            'DayOfWeek': day_of_week,
            'IsNightTime': is_night_time,
            'TransactionType': body.transaction_type,
            'BankName': normalized_bank
        }])
        
        # Perform inference
        prediction_val = int(model.predict(input_data)[0])
        probabilities = model.predict_proba(input_data)[0]
        
        # Interpret class: 1 = Fraud, 0 = Legitimate
        if prediction_val == 1:
            prediction_label = "Fraud"
            fraud_bool = True
            confidence_score = float(probabilities[1]) * 100
        else:
            prediction_label = "Legitimate"
            fraud_bool = False
            confidence_score = float(probabilities[0]) * 100
            
        return {
            "prediction": prediction_label,
            "fraud": fraud_bool,
            "confidence": round(confidence_score, 2)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error preprocessing or predicting transaction: {str(e)}"
        )
