from client_requests import *
import os

commands_list = """0.) 0 | cls | clear
1.) 1 | exit
2.) 2 | get_commands | help
3.) 3 | get_all_orders
4.) 4 | get_order_by_id
5.) 5 | create_order
6.) 6 | delete_all_orders
7.) 7 | delete_order_by_id
8.) 8 | complete_an_order"""

def main():
    print("WELCOME TO PRINTAPI TERMINAL")
    print("----------------------------------------------------------------------")
    print("Below are the lists of commands to access the PrintAPI endpoint:")
    print(commands_list)
    print("----------------------------------------------------------------------")

    while True:
        try:
            endpoint_command = input("Enter a PrintAPI command: ").lower().strip()

            if endpoint_command in ("0", "cls", "clear"):
                if os.name == "nt":
                    os.system("cls")
                else:
                    os.system("clear")

            elif endpoint_command in ("1", "exit"):
                print("Exiting the PrintAPI terminal...")
                break

            elif endpoint_command in ("2", "get_commands", "help"):
                print("Displaying all commands...")
                print("----------------------------------------------------------------------")
                print(f"{commands_list}")
                print("----------------------------------------------------------------------\n")

            elif endpoint_command in ("3", "get_all_orders"):
                print("Displaying all print orders...\n")
                getAllOrders()

            elif endpoint_command in ("4", "get_order_by_id"):
                order_id = input("Enter order ID: ")
                print(f"Displaying print order {order_id}...\n")
                getOrderByID(order_id)

            elif endpoint_command in ("5", "create_order"):
                print("===== Enter Order Details =====")
                
                customer_name = input("Customer Name: ")
                document_name = input("Document Name: ")
                
                try:
                    number_of_pages = int(input("Number of Pages: "))
                    copies_per_page = int(input("Copies per Page: "))

                    if number_of_pages and copies_per_page <= 0:
                        print(f"Invalid input. Input must not be equal or below 0.\n")
                        continue
                except ValueError:
                    print(f"Invalid input. Please input an integer for number and copies for pages.\n")
                    continue

                page_type = input("Page Types\n[1. black_and_white, 2. colored, 3. photo_paper]: ").lower()

                if page_type in ("1", "black_and_white"):
                    page_type = "black_and_white"
                elif page_type in ("2", "colored"):
                    page_type = "colored"
                elif page_type in ("3", "photo_paper"):
                    page_type = "photo_paper"
                else:
                    print("Invalid page type.\n")
                    continue
                
                createOrder(customer_name, document_name, number_of_pages, copies_per_page, page_type)
            
            elif endpoint_command in ("6", "delete_all_orders"):
                print("Deleting all print orders...\n")
                deleteAllOrders()

            elif endpoint_command in ("7", "delete_order_by_id"):
                order_id = input("Enter order ID: ")
                print(f"Deleting print order {order_id}...\n")
                deleteOrderByID(order_id)
            
            elif endpoint_command in ("8", "complete_an_order"):
                order_id = input("Enter order ID: ")
                print(f"Completing a print order {order_id}...\n")
                completeAnOrder(order_id)

            else:
                print("Uknown command.\n")
        except KeyboardInterrupt:
            print("\nExiting because of keyboard interruption.")
            break

if __name__ == "__main__":
    main()