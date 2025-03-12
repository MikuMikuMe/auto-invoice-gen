Creating an automated system for generating and managing invoices for freelancers and small businesses involves several features including adding clients, creating invoices, and managing payment records. Below is a simple Python program that demonstrates how you might implement such a system. This example focuses on a command-line interface for simplicity, but it can be expanded into a full GUI application if needed.

```python
import json
import datetime

class InvoiceGenerator:
    def __init__(self, data_file='invoice_data.json'):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {'clients': {}, 'invoices': []}
        except json.JSONDecodeError:
            print("Error: Corrupted data file. Initializing new data store.")
            self.data = {'clients': {}, 'invoices': []}

    def save_data(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.data, file, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_client(self, client_id, name, email):
        if client_id in self.data['clients']:
            print("Error: Client ID already exists.")
            return

        self.data['clients'][client_id] = {'name': name, 'email': email}
        self.save_data()
        print(f"Client '{name}' added successfully.")

    def generate_invoice(self, client_id, items):
        if client_id not in self.data['clients']:
            print("Error: Client ID does not exist.")
            return

        invoice_id = len(self.data['invoices']) + 1
        date = datetime.datetime.now().date().isoformat()
        total_amount = sum(item['price'] * item['quantity'] for item in items)

        invoice = {
            'id': invoice_id,
            'client_id': client_id,
            'date': date,
            'items': items,
            'total': total_amount,
            'paid': False
        }

        self.data['invoices'].append(invoice)
        self.save_data()
        print(f"Invoice #{invoice_id} generated successfully with total amount ${total_amount}.")

    def mark_invoice_as_paid(self, invoice_id):
        for invoice in self.data['invoices']:
            if invoice['id'] == invoice_id:
                invoice['paid'] = True
                self.save_data()
                print(f"Invoice #{invoice_id} marked as paid.")
                return

        print("Error: Invoice ID does not exist.")

    def list_invoices(self):
        if not self.data['invoices']:
            print("No invoices found.")
            return

        print("Invoices:")
        for invoice in self.data['invoices']:
            client = self.data['clients'][invoice['client_id']]
            print(f"Invoice #{invoice['id']}: {invoice['total']} {'(PAID)' if invoice['paid'] else ''}")
            print(f"  Client: {client['name']} ({client['email']})")
            print(f"  Date: {invoice['date']}")

def main():
    gen = InvoiceGenerator()
    while True:
        print("\nInvoice Management System")
        print("1. Add Client")
        print("2. Generate Invoice")
        print("3. List Invoices")
        print("4. Mark Invoice as Paid")
        print("5. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            client_id = input("Enter Client ID: ")
            name = input("Enter Client Name: ")
            email = input("Enter Client Email: ")
            gen.add_client(client_id, name, email)
        elif choice == 2:
            client_id = input("Enter Client ID: ")

            items = []
            while True:
                item_name = input("Enter Item Name (or 'done' to finish): ")
                if item_name.lower() == 'done':
                    break
                try:
                    price = float(input("Enter Item Price: "))
                    quantity = int(input("Enter Quantity: "))
                except ValueError:
                    print("Invalid input for price or quantity. Try again.")
                    continue
                
                items.append({'name': item_name, 'price': price, 'quantity': quantity})
            
            gen.generate_invoice(client_id, items)
        elif choice == 3:
            gen.list_invoices()
        elif choice == 4:
            try:
                invoice_id = int(input("Enter Invoice ID to mark as paid: "))
                gen.mark_invoice_as_paid(invoice_id)
            except ValueError:
                print("Invalid input. Please enter a valid invoice ID.")
        elif choice == 5:
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
```

### Key Features

- **Data Storage**: Uses JSON for simplicity and ease of manipulation.
- **Error Handling**: Provides basic error handling for JSON decoding and input errors.
- **Command-Line Interface**: A simple text-based interface allowing interaction with the system.
- **Client and Invoice Management**: Capabilities to add clients, generate invoices, and mark invoices as paid.

### How to Expand

- **Persistent Database**: Upgrade to a database system such as SQLite or MySQL for more robust data storage.
- **User Interface**: Implement a GUI using libraries such as Tkinter or PyQt.
- **Reporting**: Add capabilities to generate reports based on client or date.
- **Email Integration**: Implement features to email invoices directly to clients.

This code is a starting point for anyone looking to build a simple automated invoice system.