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

valid_requests=[]
invalid_requests=[]
COUNTRIES=["US","ET","UK"]
REQURED_FIELDS={"order_id", "customer", "shipping_address", "items", "payment_status"}
for request in raw_fulfillment_requests:
    if not REQURED_FIELDS.issubset(request.keys()):
        invalid_requests.append(request)
        continue
    if request["payment_status"]!="PAID":
        invalid_requests.append(request)
        continue
    if request["shipping_address"]["country"] not in COUNTRIES:
        invalid_requests.append(request)
        continue

    try:
        for item in request["items"]:
            item["price"]=float(item["price"])
            item["weight_kg"]=float(item["weight_kg"])
            item["qty"]=int(item["qty"])
    except Exception:
        invalid_requests.append(request)
        continue

    street=request["shipping_address"]["street"].strip()

    cleaned_request={
        "order_id": request["order_id"],
        "customer": request["customer"],
        "shipping_address": {**request["shipping_address"],"street":street},
        "items": request["items"],
        "payment_status": request["payment_status"]}

    valid_requests.append(cleaned_request)

#print(valid_requests)

shipping_metrics={}
country_rates={"US" :5.00 ,"ET":8.00 ,"UK" :6.50} 
for request in valid_requests:
    if request["order_id"] not in shipping_metrics:
        shipping_metrics[request["order_id"]]={
            "subtotal":0,
            "total_weight":0,
            "base_shipping_cost":0,
            "total_cost":0,
            "tier":request["customer"]["tier"]
        }

    subtotal=sum([item["price"]*item["qty"] for item in request["items"]])
    total_weight=sum([item["weight_kg"]*item["qty"] for item in request["items"]])
    base_shipping_cost=country_rates[request["shipping_address"]["country"]]*total_weight
    express=15 if request["shipping_address"]["express"] else 0

    total_order=subtotal+base_shipping_cost+express

    shipping_metrics[request["order_id"]]={
        "subtotal":shipping_metrics[request["order_id"]]["subtotal"]+subtotal,
                    "total_weight":shipping_metrics[request["order_id"]]["total_weight"]+total_weight,
                    "base_shipping_cost":shipping_metrics[request["order_id"]]["base_shipping_cost"]+base_shipping_cost,
                    "total_cost":shipping_metrics[request["order_id"]]["total_cost"]+total_order,
                    "tier":request["customer"]["tier"],
                    "express":request["shipping_address"]["express"]
                }



tier_info={"standard":0,"gold":10,"vip":20}
for order, summary in shipping_metrics.items():
    express=15 if summary["express"] else 0
    priority_score=tier_info[summary["tier"]]+express+10
    shipping_metrics[order]={**shipping_metrics[order],"priority_score":priority_score}

print(shipping_metrics)