# UPI Fraud Detection System Backend

This repository contains a production-ready, modular FastAPI backend integrated with a PostgreSQL database and a pre-trained RandomForest model (`upi_fraud_model.pkl`) to predict fraudulent UPI transactions in real-time.

## Tech Stack
- **FastAPI**: Modern, high-performance web framework for Python.
- **PostgreSQL**: Relational database for storing user registrations.
- **SQLAlchemy ORM**: Database object-relational mapping.
- **JWT (python-jose)**: Token-based secure user authentication (60-minute expiration).
- **Passlib (bcrypt)**: Secure password hashing.
- **Scikit-Learn (1.6.1)**: Loaded pipeline model wrapper for real-time predictions.
- **Pandas & NumPy**: Dynamic data manipulation for model inputs.

## Preprocessing Details
The model expects specific features and scales that were configured during training:
1. **TransactionID**: Scaled in training as a 12-digit number (mean $\approx 5.5\times 10^{11}$, scale $\approx 2.59\times 10^{11}$). Alphanumeric IDs (e.g. `TXN9F4A82K71P`) are hashed via MD5 and mapped to the range $[10^{11}, 10^{12} - 1]$ to match this uniform distribution.
2. **Transaction Time**: Automatically parses the date and extracts `Hour` (0-23), `DayOfWeek` (0-6, where Monday=0), and `IsNightTime` (1 if hour $\ge 22$ or $< 6$, else 0).
3. **Bank Name**: Normalizes colloquial entries (e.g., `sbi` -> `State Bank of India`, `hdfc` -> `HDFC Bank`) to match the OneHotEncoder's training categories. Other inputs are handled gracefully using `handle_unknown='ignore'`.

---

## Installation & Setup

### 1. Database Setup
Ensure that PostgreSQL is installed and running on your local machine. Create the target database:
```sql
CREATE DATABASE upi_fraud_detection;
```

### 2. Environment Configurations
Create a `.env` file in the root `backend/` directory (a pre-configured `.env` is already available) and customize your credentials:
```env
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/upi_fraud_detection
SECRET_KEY=8f1a14a38be98f123d463e261f9dfa052e4f014e7a83d7890f9c2d667c458a2d
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
MODEL_PATH=app/ml/upi_fraud_model.pkl
```

### 3. Setup Virtual Environment and Install Dependencies
From the `backend/` directory, run:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (Command Prompt)
.venv\Scripts\activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI application server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

- **API Documentation**: Interactive documentation is available at `http://127.0.0.1:8000/docs` (Swagger UI) or `/redoc`.
- **CORS Setup**: By default, CORS is enabled for `http://127.0.0.1:5500` and `http://localhost:5500` (VS Code Live Server). Make sure your frontend is running on this port.
