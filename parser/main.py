raw_events = [
    {
        "event_id": "ev_101",
        "user_id": "  user_nahom  ",
        "event_type": "view_item",
        "timestamp": "2026-03-01T10:00:00Z",
        "metadata": {"item_id": "item_99", "price": "120.00"},
    },
    {
        "event_id": "ev_102",
        "user_id": "user_nahom",
        "event_type": "add_to_cart",
        "timestamp": "2026-03-01T10:02:00Z",
        "metadata": {"item_id": "item_99", "price": "120.00"},
    },
    {
        "event_id": "ev_103",
        "user_id": "  user_abel ",
        "event_type": "purchase",
        "timestamp": "2026-03-01T10:05:00Z",
        "metadata": {"item_id": "item_42", "price": "50.00", "quantity": "2"},
    },
    {
        "event_id": "ev_104",
        "user_id": "user_nahom",
        "event_type": "purchase",
        "timestamp": "2026-03-01T10:10:00Z",
        "metadata": {"item_id": "item_99", "price": "120.00", "quantity": "1"},
    },
    {
        "event_id": "ev_105",
        "user_id": "user_ghost",
        "event_type": "purchase",
        "timestamp": "2026-03-01T10:15:00Z",
        "metadata": {"item_id": "item_10", "price": "invalid_price"},
    },
]
REQUIERD_KEYS={"event_id","user_id","event_type","timestamp","metadata"}
EVENT_TYPES=["purchase","add_to_cart","view_item"]

def clean_and_parse(event):
    if not REQUIERD_KEYS.issubset(event.keys()):
        return (False,"missing keys")
        

    user_name=event["user_id"].strip()
    try:
        price=float(event["metadata"]["price"])
    except Exception:
        return (False,"invalid price")

    if event["event_type"] not in EVENT_TYPES:
        return (False,"invalid event type")
    
    if "quantity" in event["metadata"]:
        try:
            quantity=int(event["metadata"]["quantity"])
        except Exception:
            return (False,"invalid quantity")
    else:
        quantity=1

    return (True,{
        "event_id": event["event_id"],
        "user_id": user_name,
        "event_type": event["event_type"],
        "price": price,
        "quantity": quantity
    })






def process(cleaned_events):
    user_metrics={}
    for event in cleaned_events:
        if event["user_id"] not in user_metrics:
            user_metrics[event["user_id"]]={
                "total_views": 0,
                "total_cart_additions": 0,
                "total_purchases": 0,
                "total_spent": 0.0
            }


        spent=user_metrics[event["user_id"]]["total_spent"]
        if event["event_type"]=="purchase":

            user_metrics[event["user_id"]]["total_purchases"]=user_metrics[event["user_id"]]["total_purchases"]+1
            user_metrics[event["user_id"]]["total_spent"]=spent+event["price"]*event["quantity"]
        elif event["event_type"]=="add_to_cart":
            user_metrics[event["user_id"]]["total_cart_additions"]=user_metrics[event["user_id"]]["total_cart_additions"]+1
        elif event["event_type"]=="view_item":
            user_metrics[event["user_id"]]["total_views"]=user_metrics[event["user_id"]]["total_views"]+1

        
    return user_metrics


def process_event_logs(raw_events):
    cleaned_events=[]
    invalid_events=[]

    for raw in raw_events:
        is_valid,result=clean_and_parse(raw)

        if is_valid:
            cleaned_events.append(result)
        else:
            invalid_events.append(result)

    user_metrics=process(cleaned_events)

    return {
        "metrics": user_metrics,
        "invalid_events": invalid_events,
    }


print(process_event_logs(raw_events)["metrics"])

