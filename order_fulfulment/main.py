raw_fulfillment_requests = [
    {
        "order_id": "ord_8801",
        "customer": {"id": "c_101", "tier": "gold"},
        "shipping_address": {
            "street": " 123 Main St ",
            "country": "US",
            "express": True,
        },
        "items": [
            {"sku": "SKU-LAPTOP", "price": "1200.00", "qty": 1, "weight_kg": "2.5"},
            {"sku": "SKU-MOUSE", "price": "25.00", "qty": "2", "weight_kg": "0.2"},
        ],
        "payment_status": "PAID",
    },
    {
        "order_id": "ord_8802",
        "customer": {"id": "c_102", "tier": "standard"},
        "shipping_address": {
            "street": "456 Bole Rd",
            "country": "ET",
            "express": False,
        },
        "items": [
            {"sku": "SKU-PHONE", "price": "600.00", "qty": 1, "weight_kg": "0.5"}
        ],
        "payment_status": "PAID",
    },
    {
        "order_id": "ord_8803",
        "customer": {"id": "c_103", "tier": "standard"},
        "shipping_address": {
            "street": "789 Oxford St",
            "country": "UK",
            "express": True,
        },
        "items": [
            {"sku": "SKU-BOOK", "price": "15.00", "qty": 3, "weight_kg": "0.4"}
        ],
        "payment_status": "UNPAID",
    },
    {
        "order_id": "ord_8804",
        "customer": {"id": "c_104", "tier": "vip"},
        "shipping_address": {
            "street": "101 Pier St",
            "country": "US",
            "express": False,
        },
        "items": [
            {"sku": "SKU-MONITOR", "price": "corrupted_price", "qty": 1, "weight_kg": "5.0"}
        ],
        "payment_status": "PAID",
    },
    {
        "order_id": "ord_8805",
        "customer": {"id": "c_105", "tier": "gold"},
        "shipping_address": {
            "street": " 55 Churchill Rd ",
            "country": "ET",
            "express": True,
        },
        "items": [
            {"sku": "SKU-TABLET", "price": "400.00", "qty": 2, "weight_kg": "0.8"}
        ],
        "payment_status": "PAID",
    },
]


COUNTRIES=["US","ET","UK"]
REQURED_FIELDS={"order_id", "customer", "shipping_address", "items", "payment_status"}

def parse_and_clean(request):

    if not REQURED_FIELDS.issubset(request.keys()):
        return (False,"missing required fields")
    
    if request["payment_status"]!="PAID":
        return (False,"payment status is not paid")
    
    shipping = request.get("shipping_address", {})
    if not isinstance(shipping, dict) or shipping.get("country") not in COUNTRIES:
        return False, f"Invalid or unsupported country: '{shipping.get('country')}'"

    items = request.get("items", [])
    if not isinstance(items, list) or len(items) == 0:
        return False, "Order must contain at least one item"

    cleaned_items = []
    try:
        for item in items:
            cleaned_items.append({
                "sku": item["sku"],
                "price": float(item["price"]),
                "weight_kg": float(item["weight_kg"]),
                "qty": int(item["qty"]),
            })
    except (ValueError, TypeError, KeyError):
        return False, "Invalid price, weight, or quantity format in items"
    

    street=request["shipping_address"]["street"].strip()

    cleaned_order = {
        "order_id": request["order_id"],
        "customer": request["customer"],
        "shipping_address": {
            "street": street,
            "country": shipping["country"],
            "express": bool(shipping.get("express", False)),
        },
        "items": cleaned_items,
        "payment_status": request["payment_status"],
    }
    return True, cleaned_order

TIER_SCORES = {"standard": 0, "gold": 10, "vip": 20}
COUNTRY_RATES={"US" :5.00 ,"ET":8.00 ,"UK" :6.50} 
def calculate_order_fulfilment(order):
    subtotal = sum(item["price"] * item["qty"] for item in order["items"])
    total_weight = sum(item["weight_kg"] * item["qty"] for item in order["items"])

    country = order["shipping_address"]["country"]
    base_shipping = COUNTRY_RATES[country] * total_weight
    
    is_express = order["shipping_address"]["express"]
    express_surcharge = 15.0 if is_express else 0.0
    
    total_cost = subtotal + base_shipping + express_surcharge

    tier = order["customer"].get("tier", "standard")


    priority_score = 10 + TIER_SCORES.get(tier, 0) + (15 if is_express else 0)

    return {
        "order_id": order["order_id"],
        "subtotal": subtotal,
        "total_weight_kg": total_weight,
        "base_shipping_cost": base_shipping,
        "express_surcharge": express_surcharge,
        "total_cost": total_cost,
        "priority_score": priority_score,
    }


def process_fulfillment_batch(raw_fulfillment):
    valid_metrics = []
    invalid_requests = []

    for request in raw_fulfillment:
        is_valid, result = parse_and_clean(request)
        if is_valid:
            metrics = calculate_order_fulfilment(result)
            valid_metrics.append(metrics)
        else:
            invalid_requests.append({"raw": request, "reason": result})

    # Sort valid orders by priority_score (highest priority first)
    valid_metrics.sort(key=lambda x: x["priority_score"], reverse=True)

    return {
        "valid": valid_metrics,
        "invalid": invalid_requests,
    }


print(process_fulfillment_batch(raw_fulfillment_requests)["valid"])






