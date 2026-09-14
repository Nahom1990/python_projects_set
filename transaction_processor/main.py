transactions = [
    {
        "id": 1,
        "user": " Nahom ",
        "type": "income",
        "amount": "1500",
        "status": "completed",
    },
    {
        "id": 2,
        "user": " Nahom ",
        "type": "expense",
        "amount": "200",
        "status": "completed",
    },
    {
        "id": 3,
        "user": " Abel ",
        "type": "income",
        "amount": "800",
        "status": "pending",
    },
    {
        "id": 4,
        "user": " Abel ",
        "type": "expense",
        "amount": "100",
        "status": "completed",
    },
    {
        "id": 5,
        "user": " Nahom ",
        "type": "income",
        "amount": "500",
        "status": "failed",
    },
]


VALID_TYPES = {"income", "expense"}
VALID_STATUSES = {"completed", "pending", "failed"}


def parse_and_validate(raw_tx: dict) -> tuple[bool, dict | str]:
    # 1. Check required keys
    required_keys = {"id", "user", "type", "amount", "status"}
    if not required_keys.issubset(raw_tx.keys()):
        missing = required_keys - raw_tx.keys()
        return False, f"Missing required fields: {missing}"

    # 2. Normalize user string
    user = str(raw_tx["user"]).strip()
    if not user:
        return False, "User name cannot be empty"

    # 3. Parse amount safely
    try:
        amount = float(raw_tx["amount"])
    except (ValueError, TypeError):
        return False, f"Invalid numeric amount: '{raw_tx['amount']}'"

    # 4. Enforce domain rules
    if amount <= 0:
        return False, f"Amount must be positive, got: {amount}"

    tx_type = str(raw_tx["type"]).strip().lower()
    if tx_type not in VALID_TYPES:
        return False, f"Invalid type: '{tx_type}'. Must be 'income' or 'expense'"

    status = str(raw_tx["status"]).strip().lower()
    if status not in VALID_STATUSES:
        return (
            False,
            f"Invalid status: '{status}'. Must be 'completed', 'pending', or 'failed'",
        )

    # 5. Return fresh, clean dictionary payload
    cleaned_tx = {
        "id": raw_tx["id"],
        "user": user,
        "type": tx_type,
        "amount": amount,
        "status": status,
    }
    return True, cleaned_tx

def aggregate_user_metrics(valid_transactions: list[dict]) -> dict:
    users = {}

    for tx in valid_transactions:
        # Ignore pending/failed for financial calculations
        if tx["status"] != "completed":
            continue

        user = tx["user"]

        # Initialize user state if first time seen
        if user not in users:
            users[user] = {
                "total_income": 0.0,
                "total_expense": 0.0,
                "balance": 0.0,
                "number_of_transactions": 0,
            }

        # Update metrics locally
        stats = users[user]
        stats["number_of_transactions"] += 1

        if tx["type"] == "income":
            stats["total_income"] += tx["amount"]
            stats["balance"] += tx["amount"]
        elif tx["type"] == "expense":
            stats["total_expense"] += tx["amount"]
            stats["balance"] -= tx["amount"]

    return users

def process_transaction_batch(raw_transactions: list[dict]) -> dict:
    valid_records = []
    invalid_records = []

    for raw_tx in raw_transactions:
        is_valid, result = parse_and_validate(raw_tx)

        if is_valid:
            valid_records.append(result)
        else:
            invalid_records.append({"raw": raw_tx, "reason": result})

    # Aggregation step
    user_summary = aggregate_user_metrics(valid_records)

    # Return structured state payload
    return {
        "processed_count": len(valid_records),
        "invalid_count": len(invalid_records),
        "invalid_records": invalid_records,
        "users": user_summary,
    }

def format_text_report(report_data: dict) -> str:
    lines = []
    lines.append("=== FINANCIAL TRANSACTION REPORT ===")
    lines.append(f"Processed transactions: {report_data['processed_count']}")
    lines.append(f"Invalid transactions:   {report_data['invalid_count']}")
    lines.append("")

    lines.append("Users Summary:")
    lines.append("-----------------------------------")

    users = report_data["users"]
    if not users:
        lines.append("No completed transaction data available.")

    for user, stats in users.items():
        lines.append(f"User: {user}")
        lines.append(f"  Income:       ${stats['total_income']:,.2f}")
        lines.append(f"  Expenses:     ${stats['total_expense']:,.2f}")
        lines.append(f"  Balance:      ${stats['balance']:,.2f}")
        lines.append(f"  Transactions: {stats['number_of_transactions']}")
        lines.append("")

    if report_data["invalid_records"]:
        lines.append("Invalid Record Details:")
        lines.append("-----------------------------------")
        for inv in report_data["invalid_records"]:
            lines.append(
                f"  - ID {inv['raw'].get('id', 'Unknown')}: {inv['reason']}"
            )

    return "\n".join(lines)

report_data = process_transaction_batch(transactions)
formatted_report = format_text_report(report_data)

print(formatted_report)