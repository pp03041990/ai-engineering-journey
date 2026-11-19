# def get_available_tickets(event):
#     try:
#      return max(0,event.get("available_tickets",0))
#     except(ValueError,TypeError):
#        return 0

# print(get_available_tickets({"name":"Tech coneference","available_tickets":"0.5"}))

import json
new_event = {"name": "AI Summit", "price": 900}
with open("events.json","r") as file:
    events=json.load(file)
for event in events:
    price = event.get("price",0)
    if 0< price <1000:
        print(price)
events.append(new_event)
with open("events.json","w") as file:
    json.dump(events,file,indent=4)