import re
from datetime import datetime
import re
from datetime import datetime
from typing import List, Dict, Optional


def parse_transactions(text: str) -> List[Dict]:
    """
    Parse raw OCR text into a list of transaction dictionaries.
    Supports line-based statements with dates at the start of each line.
    Handles multi-line descriptions by buffering continuation lines.
    """
    lines = text.splitlines()
    transactions = []
    current = None

    # Regex patterns
    date_re = re.compile(r'^(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})')
    amount_re = re.compile(r'[-+]?\d+[,.]?\d{2}')  # matches -1234,56 or 1234.56 etc.

    def extract_amount(s: str) -> Optional[float]:
        # clean commas, convert
        s = s.replace(',', '.').replace(' ', '')
        try:
            return float(s)
        except:
            return None

    def parse_date(date_str: str) -> Optional[datetime]:
        for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        # Check if line starts with a date pattern
        date_match = date_re.match(line)
        if date_match:
            # Save previous transaction
            if current:
                transactions.append(current)

            # Extract date string (matches at start)
            date_str = date_match.group(1)
            rest = line[len(date_str):].strip()

            # Find amounts in rest
            amount_matches = amount_re.findall(rest)
            # Usually last two numbers are amount and balance
            amount_str = None
            balance_str = None
            if len(amount_matches) >= 2:
                amount_str = amount_matches[-2]
                balance_str = amount_matches[-1]
                # Remove the amount and balance from rest to get description
                # Partition by amount_str?
                # Simpler: take all tokens except the last two numeric tokens
                tokens = rest.split()
                # Remove trailing numeric tokens equivalent to amount_str and balance_str (consider formatting)
                # We'll reconstruct description: join all tokens that are not amount or balance
                desc_tokens = []
                skip = 0
                for token in reversed(tokens):
                    if skip < 2 and (amount_re.fullmatch(token) or token.replace(',', '.').replace(' ', '') == amount_str or token.replace(',', '.').replace(' ', '') == balance_str):
                        skip += 1
                        continue
                    desc_tokens.insert(0, token)
                description = " ".join(desc_tokens).strip()
            else:
                # Not enough amounts; fallback: treat whole rest as description
                description = rest
                amount_str = "0"
                balance_str = "0"

            amount_val = extract_amount(amount_str) or 0.0
            balance_val = extract_amount(balance_str) or 0.0
            trans_date = parse_date(date_str) or datetime.utcnow().date()

            # Determine type based on sign (assuming negative=debit)
            type_ = "Debit" if amount_val < 0 else "Credit"
            mutation_amount = abs(amount_val)

            current = {
                "date": trans_date,
                "description": description,
                "mutation_amount": mutation_amount,
                "type": type_,
                "balance": balance_val,
            }
        else:
            # Continuation line: append to description buffer
            if current:
                current["description"] += " " + line

    if current:
        transactions.append(current)
    return transactions
