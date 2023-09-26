class Transaction:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, manufacturer, distributor, client, amount=None):
        transaction_data = {
            "manufacturer": manufacturer,
            "distributor": distributor,
            "client": client,
            "amount": amount,
            "timestamp_get_from_manufacturer": None,
            "timestamp_dispatched": None,
            "timestamp_received": None,
        }
        self.transactions.append(transaction_data)

    def set_timestamp_get_from_manufacturer(self, index, timestamp):
        if 0 <= index < len(self.transactions):
            self.transactions[index]["timestamp_get_from_manufacturer"] = timestamp

    def set_timestamp_dispatched(self, index, timestamp):
        if 0 <= index < len(self.transactions):
            self.transactions[index]["timestamp_dispatched"] = timestamp

    def set_timestamp_received(self, index, timestamp):
        if 0 <= index < len(self.transactions):
            self.transactions[index]["timestamp_received"] = timestamp

# Create Transaction object
block1 = Transaction()

# Add transactions
block1.add_transaction("Manufacturer1", "Distributor1", "Client1", 100)
block1.add_transaction("Manufacturer2", "Distributor2", "Client2", 150)

# Set timestamps for different stages
block1.set_timestamp_get_from_manufacturer(0, "Timestamp1")
block1.set_timestamp_dispatched(0, "Timestamp2")
block1.set_timestamp_received(0, "Timestamp3")

# Access and print the transactions
for transaction in block1.transactions:
    print("Manufacturer:", transaction["manufacturer"])
    print("Distributor:", transaction["distributor"])
    print("Client:", transaction["client"])
    print("Amount:", transaction["amount"])
    print("Timestamp - Get from Manufacturer:", transaction["timestamp_get_from_manufacturer"])
    print("Timestamp - Dispatched:", transaction["timestamp_dispatched"])
    print("Timestamp - Received:", transaction["timestamp_received"])
    print()