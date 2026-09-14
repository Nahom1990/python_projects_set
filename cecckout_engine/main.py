from typing import Optional
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
]

VALID_COUNTRIES=["ET","US"]
VALID_COUPONSS:list[str]=["SAVE10","SAVE20","VIP30"]
def parse_and_validate(order:dict):
    required_fields={"id","customer","items","coupon"}
    if not required_fields.issubset(order.keys()):
        return (False,"there are some missing fields")
    
    username="_".join(order["customer"]["name"].split()).lower()

    if order["customer"]["country"] not in VALID_COUNTRIES:
        return (False,"invalid country")

    if order["coupon"] not in VALID_COUPONSS or order["coupon"] is  None:
        return (False,"invalid coupon")

    for item in order["items"]:
        try:
            price=float(item["price"])
        except Exception:
            return (False,"invalid price")

    for item in order["items"]:
        try:
            qty=int(item["quantity"])
        except Exception:
            return (False,"invalid quantity")

    return (True,{
            "id": order["id"],
            "customer": {
                "name": username,
                "country": order["customer"]["country"]
            },
            "items": [{"name":item["name"],
                       "price":float(item["price"]),
                       "quantity":int(item["quantity"])} for item in order["items"]
            ],
            "coupon": order["coupon"],
        })
