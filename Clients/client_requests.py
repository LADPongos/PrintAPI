import requests

url = "http://127.0.0.1:8000"

# ===== GET METHOD: View Order Functions =====
def getAllOrders():
    response = requests.get(f"{url}/orders")
    data = response.json()

    if response.status_code == 200:
        orders = data.get("orders", [])
        if not orders:
            print("No orders found.\n")
            return

        print(f"===== All Orders ({len(orders)}) =====\n")
        for index, order in enumerate(orders, start=1):
            print(f"Index: {index}")
            print(f"Order ID: {order['order_id']}")
            print(f"Customer Name: {order['customer_name']}")
            for item in order["items"]:
                print(f"Document Name: {item['document_name']}")
                print(f"No. of Pages: {item['number_of_pages']}")
                print(f"Copies per Page: {item['copies_per_page']}")
                print(f"Page Type: {item['page_type']}")
            print(f"Total Cost: {order['total_cost']:.2f}")
            print(f"Status: {order['status']}\n")
    else:
        print(f"Error: {data.get('detail', 'Unknown error.')}\n")

def getOrderByID(orderID: int):
    response = requests.get(f"{url}/orders/{orderID}")
    data = response.json()

    if response.status_code == 200:
        order = data['order']

        print(f"Order ID: {order['order_id']}")
        print(f"Customer Name: {order['customer_name']}")
        for idx, item in enumerate(order['items'], start=1):
            print(f"Document Name: {item['document_name']}")
            print(f"No. of Pages: {item['number_of_pages']}")
            print(f"Copies per Page: {item['copies_per_page']}")
            print(f"Page Type: {item['page_type']}")
        print(f"Total Cost: {order['total_cost']:.2f}")
        print(f"Status: {data['order']['status']}\n")
    else:
        print(f"{data['detail']}\n")

# ===== POST METHOD: Create Order Functions =====
def createOrder(customerName: str, documentName: str, numberOfPages: int, copiesPerPage: int, pageType: str):
    order_data = {
        "customer_name": customerName,
        "items": [
            {
                "document_name": documentName,
                "number_of_pages": numberOfPages,
                "copies_per_page": copiesPerPage,
                "page_type": pageType
            }
        ]
    }

    response = requests.post(f"{url}/orders", json=order_data)
    data = response.json()

    if response.status_code == 201:
        print(f"{data['message']}\nTotal Cost: {data['order']['total_cost']:.2f}\n")
    else:
        print(f"{data['detail']}\n")

# ===== DELETE METHOD: Delete Order Functions =====
def deleteAllOrders():
    response = requests.delete(f"{url}/orders")
    data = response.json()

    print(f"{data['message']}\n")

def deleteOrderByID(orderID: int):
    response = requests.delete(f"{url}/orders/{orderID}")
    data = response.json()

    if response.status_code == 200:
        print(f"{data['message']}\n")
    else:
        print(f"{data['detail']}\n")

# ===== PUT METHOD: Complete an Order Function =====
def completeAnOrder(orderID: int):
    response = requests.put(f"{url}/orders/{orderID}/complete")
    data = response.json()

    if response.status_code == 200:
        print(f"{data['message']}\n")
    else:
        print(f"{data['detail']}\n")