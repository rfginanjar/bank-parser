from fastapi import HTTPException

def validate_transaction(transaction_id: int, action: str) -> dict:
    # check transaction, update status based on action ('approve'/'reject')
    # log action, maybe move to final table
    return {'status': 'success'}
    raise HTTPException(400, 'Invalid action')
