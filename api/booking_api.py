import requests
    
def get_booking(booking_id):
      try:
            return requests.get(f"https://restful-booker.herokuapp.com/booking/{booking_id}",timeout=10)
      except requests.exceptions.RequestException:
            return None