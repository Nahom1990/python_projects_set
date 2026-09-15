
VALID_COUNTRIES = {"ET", "US", "UK"}
KNOWN_COUPONS = {"SAVE10", "SAVE20", "VIP30"}


def parse_and_validate(order: dict) -> tuple[bool, dict | str]:
    # 1. Check top-level schema
    required_fields = {"id", "customer", "items", "coupon"}
    if not required_fields.issubset(order.keys()):
        missing = required_fields - order.keys()
        return False, f"Missing top-level fields: {missing}"

    # Check nested customer schema
    if not isinstance(order["customer"], dict) or not {
        "name",
        "country",
    }.issubset(order["customer"].keys()):
        return False, "Invalid or missing customer details"

    # 2. Clean customer name & validate country
    name = str(order["customer"]["name"]).strip()
    if not name:
        return False, "Customer name cannot be empty"

    country = str(order["customer"]["country"]).strip().upper()
    if country not in VALID_COUNTRIES:
        return False, f"Unsupported country: '{country}'"

    # 3. Clean and validate coupon
    # If coupon is unknown or None, default to None (0% discount) rather than rejecting the order
    raw_coupon = order.get("coupon")
    coupon = raw_coupon if raw_coupon in KNOWN_COUPONS else None

    # 4. Clean & validate items
    items = order.get("items")
    if not isinstance(items, list) or len(items) == 0:
        return False, "Order must contain at least one item"

    cleaned_items = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict) or not {"name", "price", "quantity"}.issubset(item.keys()):
            return False, f"Item at index {idx} is missing required fields"

        try:
            price = float(item["price"])
            quantity = int(item["quantity"])
        except (ValueError, TypeError):
            return False, f"Invalid price or quantity for item '{item.get('name')}'"

        if price <= 0 or quantity <= 0:
            return False, f"Price and quantity must be positive for item '{item.get('name')}'"

        cleaned_items.append({
            "name": str(item["name"]).strip(),
            "price": price,
            "quantity": quantity,
        })

    # 5. Return success signal + cleaned immutable-style dictionary
    cleaned_order = {
        "id": order["id"],
        "customer": {"name": name, "country": country},
        "items": cleaned_items,
        "coupon": coupon,
    }
    return True, cleaned_order



def create_discount_rule(min_subtotal=0, allowed_country=None, discount_pct=0.0):
    """
    Returns a closure (a function) tailored to specific criteria.
    The returned function takes an order and decides if the discount applies.
    """
    def discount_rule(order: dict, subtotal: float) -> float:
        # Check country condition (if set)
        if allowed_country and order["customer"]["country"] != allowed_country:
            return 0.0
        
        # Check minimum subtotal condition
        if subtotal < min_subtotal:
            return 0.0
            
        return discount_pct

    return discount_rule


# Rule 1: Ethiopian promo (> $500 gets 10%)
ethiopia_promo = create_discount_rule(min_subtotal=500, allowed_country="ET", discount_pct=0.10)

# Rule 2: Standard coupon lookup
COUPON_RULES = {
    "SAVE10": create_discount_rule(discount_pct=0.10),
    "SAVE20": create_discount_rule(discount_pct=0.20),
    "VIP30":  create_discount_rule(discount_pct=0.30),
}

def calculate_discount(order: dict, subtotal: float) -> float:
    coupon = order.get("coupon")
    
    # 1. Apply coupon rule if valid
    if coupon in COUPON_RULES:
        rule_closure = COUPON_RULES[coupon]
        return subtotal * rule_closure(order, subtotal)
        
    # 2. Check automatic promotional rule (e.g., Ethiopia promo)
    pct = ethiopia_promo(order, subtotal)
    return subtotal * pct

TAX_RATES = {"ET": 0.15, "US": 0.08, "UK": 0.20}

def get_tax_rate(country: str) -> float:
    return TAX_RATES.get(country, 0.0)

def calculate_subtotal(items:list[dict]):
    return sum(item["price"] * item["quantity"] for item in items)


def process_order(order: dict) -> dict:
    # 1. Calculate step-by-step
    subtotal = calculate_subtotal(order["items"])
    discount = calculate_discount(order, subtotal)
    taxable_amount = max(0.0, subtotal - discount)
    
    tax_rate = get_tax_rate(order["customer"]["country"])
    tax = taxable_amount * tax_rate
    
    total = taxable_amount + tax

    # 2. Return clean result payload (rounded to 2 decimal places for financial calculations)
    return {
        "order_id": order["id"],
        "customer": order["customer"]["name"],
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
    }

def process_orders(raw_orders: list[dict]) -> dict:
    processed_orders = []
    invalid_orders = []

    for raw_order in raw_orders:
        is_valid, result = parse_and_validate(raw_order)
        
        if is_valid:
            # Result is the cleaned order dict
            calculated_order = process_order(result)
            processed_orders.append(calculated_order)
        else:
            # Result is the error reason string
            invalid_orders.append({
                "raw_order": raw_order,
                "reason": result
            })

    return {
        "processed_orders": processed_orders,
        "invalid_orders": invalid_orders,
        "total_processed": len(processed_orders),
        "total_invalid": len(invalid_orders),
    }

# Sample Dataset
orders = [
    {
        "id": 101,
        "customer": {
            "name": "  Nahom Mekuria ",
            "country": "ET"
        },
        "items": [
            {"name": "Laptop", "price": "800", "quantity": 1},
            {"name": "Mouse", "price": "25", "quantity": 2},
        ],
        "coupon": "SAVE10",
    },
    {
        "id": 102,
        "customer": {
            "name": " Abel Tesfaye ",
            "country": "US"
        },
        "items": [
            {"name": "Keyboard", "price": "50", "quantity": 2},
            {"name": "Monitor", "price": "300", "quantity": 1},
        ],
        "coupon": None,
    },
    {
        "id": 103,
        "customer": {
            "name": " Bad Customer ",
            "country": "INVALID_COUNTRY"
        },
        "items": [
            {"name": "Desk", "price": "150", "quantity": 1}
        ],
        "coupon": None,
    }
]

# Run the system
summary = process_orders(orders)
print(summary)