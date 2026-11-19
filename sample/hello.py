event_name='Tech Conference'
is_premium_member = False
ticket_price=0 if is_premium_member  else 1500
available_tickets=10
status = 'Available' if available_tickets > 0 else 'Sold out'
print(f"Event: {event_name}\nTicket price: {ticket_price}\nStatus: {status}\nCost for 2 tickets: {ticket_price*2}")

# for i in range(1,6):
#     print(f"Processing ticket {i}")

events = ["Tech Conference", "Music Festival", "Food Expo"]
# for event in events:
#     print(event)
# for i in range(len(events)):
#     print(f"{i+1}: {events[i]}")
# for index, event in enumerate(events,start=1):
#     print(f"{index}: {event}")
def get_event_price(event):
    print(event.get('price',0))
event = {
    "name": "Tech Conference",
    "price": 1500,
    "available_tickets": 10,
    "address":{
        "postalcode":123456
    }
}
get_event_price(event)

# print(event.get('address',{}).get('postalcode'))
events = [
    {"name": "Tech Conference", "price": 1500},
    {"name": "Music Festival", "price": 800},
    {"name": "Food Expo", "price": 500}
]

# for event in events:
#     # print(f"{event["name"]} {event["price"]}")
#     print(event.get("name"), event.get("price"))




