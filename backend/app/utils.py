import hashlib

def hash_transaction_id(txn_id: str) -> float:
    """
    Converts a transaction ID string to a 12-digit float.
    
    If the transaction ID is already numeric and has 10 to 15 digits, we parse it
    directly. Otherwise, we hash it using MD5 and scale it into the range
    [10^11, 10^12 - 1] matching the uniform distribution of the scaler.
    """
    clean_id = ''.join(c for c in txn_id if c.isdigit())
    if clean_id and 10 <= len(clean_id) <= 15:
        try:
            return float(clean_id[:12])
        except ValueError:
            pass
            
    # MD5 Hashing to map into the range [10^11, 10^12 - 1]
    h = int(hashlib.md5(txn_id.encode()).hexdigest(), 16)
    val = 10**11 + (h % (9 * 10**11))
    return float(val)

def normalize_bank_name(bank_name: str) -> str:
    """
    Standardizes bank name entries to match categories trained in the OneHotEncoder:
    - Axis Bank
    - Bank of Baroda
    - HDFC Bank
    - ICICI Bank
    - Kotak Mahindra Bank
    - State Bank of India
    """
    bank_name_lower = bank_name.lower().strip()
    if "axis" in bank_name_lower:
        return "Axis Bank"
    elif "baroda" in bank_name_lower or "bob" in bank_name_lower:
        return "Bank of Baroda"
    elif "hdfc" in bank_name_lower:
        return "HDFC Bank"
    elif "icici" in bank_name_lower:
        return "ICICI Bank"
    elif "kotak" in bank_name_lower:
        return "Kotak Mahindra Bank"
    elif "state bank" in bank_name_lower or "sbi" in bank_name_lower:
        return "State Bank of India"
    else:
        # OneHotEncoder will ignore unknown names gracefully
        return bank_name.strip()
