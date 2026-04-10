from datetime import datetime, date
from typing import List, Dict, Any
import re

def validate_amount(value: Any) -> float:
    """Validate and convert to positive float."""
    try:
        val = float(value)
        if val <= 0:
            raise ValueError("Amount must be positive")
        return val
    except (TypeError, ValueError):
        raise ValueError("Invalid numeric amount")

def validate_date(date_str: str) -> date:
    """Parse ISO 8601 date string."""
    try:
        return datetime.fromisoformat(date_str).date()
    except (TypeError, ValueError):
        raise ValueError("Invalid date format, expected ISO 8601 (YYYY-MM-DD)")

def validate_transaction_data(data: Dict[str, Any]) -> Dict[str, Any]:
    required = ["date", "mutation_amount", "balance", "description", "type"]
    for field in required:
        if field not in data:
            raise ValueError(f"Missing field: {field}")
    validated = {}
    validated["date"] = validate_date(data["date"])
    validated["mutation_amount"] = validate_amount(data["mutation_amount"])
    validated["balance"] = validate_amount(data["balance"])
    if not isinstance(data["description"], str) or not data["description"].strip():
        raise ValueError("Invalid description")
    validated["description"] = data["description"].strip()
    if data["type"] not in ("Debit", "Credit"):
        raise ValueError("Invalid transaction type")
    validated["type"] = data["type"]
    validated["category"] = data.get("category")
    return validated

async def process_validation(updates: List[Dict]) -> Dict[str, List]:
    """Validate each update and return dict with validated and errors."""
    validated_list = []
    errors = []
    for i, item in enumerate(updates):
        try:
            validated = validate_transaction_data(item)
            validated_list.append(validated)
        except ValueError as e:
            errors.append({"index": i, "error": str(e)})
    return {"validated": validated_list, "errors": errors}