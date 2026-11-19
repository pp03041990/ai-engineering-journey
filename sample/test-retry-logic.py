from retry import retry_operation

def fetch_data():
    print("data loading...")
    return "Data received"

# print(retry_operation(fetch_data))
retry_operation(lambda:print("Hello"))