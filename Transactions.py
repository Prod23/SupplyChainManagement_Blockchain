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